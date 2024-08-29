use super::*;
use crate::config::*;
use anyhow::{bail, Result};
use num::Complex;

#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Clone, Copy, Debug, PartialEq)]
/// # A biquad is a second order recursive filter structure.
///
/// This implementation only allows for normalized coefficients (a_0 = 1). It
///  performs the following relation of output to input:
///
///  ```math
///  y[n] = - a_1 * y[n-1] - a_2 * y[n-2]
///       + b_0 * x[n] + b_1 * x[n-1] + b_2 * x[n-2]
///  ```
///
///  The coefficients can be generated for typical standard type of biquad
///  filters, such as low pass, high pass, bandpass (first order), low shelf,
///  high shelf, peaking and notch filters.
///
///  The transfer function is:
///
/// ```math
///          b_0 + b_1 z^-1 + b_2 * z^-2
///  H[z] = -----------------------------
///          1   + a_1 z^-1 + a_2 * z^-2
///  ```
///
///  And the frequency response can be found by filling in in above equation z =
///  exp(i*omega/fs), where fs is the sampling frequency and omega is the radian
///  frequency at which the transfer function is evaluated.
///  
/// ## Implementation details
///
/// The implementaion is so-called "Direct-form 2", see
/// [https://en.wikipedia.org/wiki/Digital_biquad_filter].
pub struct Biquad {
    // State parameters
    w1: Flt,
    w2: Flt,
    // Filter coefficients - forward
    b0: Flt,
    b1: Flt,
    b2: Flt,
    // Filter coefficients - recursive
    // a0: Flt, // a0 is assumed one, not used
    a1: Flt,
    a2: Flt,
}
#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl Biquad {
    #[new]
    /// Create new biquad filter. See [Biquad::new]
    ///
    pub fn new_py<'py>(coefs: PyArrayLike1<Flt>) -> PyResult<Self> {
        Ok(Biquad::new(coefs.as_slice()?)?)
    }
    #[pyo3(name = "unit")]
    #[staticmethod]
    /// See: [Biquad::unit()]
    pub fn unit_py() -> Biquad {
        Biquad::unit()
    }
    #[pyo3(name = "firstOrderHighPass")]
    #[staticmethod]
    /// See: [Biquad::firstOrderHighPass]
    pub fn firstOrderHighPass_py(fs: Flt, fc: Flt) -> PyResult<Biquad> {
        Ok(Biquad::firstOrderHighPass(fs, fc)?)
    }

    // Print biquad in Python
    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    /// See: [Biquad::firstOrderMovingAverage]
    #[pyo3(name = "firstOrderMovingAverage")]
    #[staticmethod]
    pub fn firstOrderMovingAverage_py(fs: Flt, fc: Flt) -> PyResult<Biquad> {
        Ok(Biquad::firstOrderMovingAverage(fs, fc)?)
    }

    /// See: [Biquad::tf]
    #[pyo3(name = "tf")]
    pub fn tf_py<'py>(
        &self,
        py: Python<'py>,
        fs: Flt,
        freq: PyArrayLike1<Flt>,
    ) -> PyResult<PyArr1Cflt<'py>> {
        let freq = freq.as_array();
        let res = PyArray1::from_array_bound(py, &self.tf(fs, freq));
        Ok(res)
    }

    /// See: [Biquad::filter()]
    #[pyo3(name = "filter")]
    pub fn filter_py<'py>(
        &mut self,
        py: Python<'py>,
        input: PyArrayLike1<Flt>,
    ) -> Result<PyArr1Flt<'py>> {
        Ok(PyArray1::from_vec_bound(py, self.filter(input.as_slice()?)))
    }
}
impl Biquad {
    /// Create new biquad filter from given filter coeficients
    ///
    /// # Args
    ///
    /// - coefs: Filter coefficients. Should be 6 in toal. First 3 coefficients
    ///   are numerator (forward) coefs. Last 3 are denominator (recursive)
    ///   coefficients. Note that `coefs[3]` should be equal to 1.0. Hence the
    ///   normalization is such that a0 equals 1.0. If this is not the case, an
    ///   error occurs.
    ///
    pub fn new(coefs: &[Flt]) -> Result<Self> {
        match coefs {
            &[b0, b1, b2, a0, a1, a2] => {
                if a0 != 1.0  {
                    bail!("Coefficient a0 should be equal to 1.0")
                }
                Ok(Biquad { w1: 0., w2: 0., b0, b1, b2, a1, a2})
            },
            _ => bail!("Could not initialize biquad. Please make sure that the coefficients contain 6 terms, see documentation for order.")
        }
    }

    /// Set the state as if the filter converged to the DC value `val`. Note
    /// that this only works for filters that do have a D.C. nonzero gain. If
    /// not, this method will do a kind of divide-by-zero.
    pub fn setToDCValue(&mut self, val: Flt) {
        // D.C. output is:
        // y[n] = b0*w[n] + b1*w[n-1] + b2*w[n-2]
        // and:
        // w[n] = x[n] - a1*w[n-1] -a2*w[n-2]

        // Assume w[n] = w[n-1] = w[n-2]:
        // We have:
        // w[n]*(1+a1+a2) = x
        // And:
        // y[n] = (b0+b1+b2) * wn
        // Hence:
        // y[n] = sum_b * w
        // So we should set w to val/sum_b
        let sumb = self.b0 + self.b1 + self.b2;
        let w = val / sumb;
        self.w1 = w;
        self.w2 = w;
    }

    /// Change the gain value such that it matches `val` at frequency `freq`.
    /// Does not change the phase at the given frequency.
    pub fn setGainAt(mut self, freq: Flt, required_gain: Flt) -> Biquad {
        assert!(required_gain > 0.);
        let freq = [freq];
        let cur_gain_at_freq = self.tf(-1.0, &freq)[0].abs();
        let gain_fac = required_gain / cur_gain_at_freq;
        self.b0 *= gain_fac;
        self.b1 *= gain_fac;
        self.b2 *= gain_fac;
        self
    }

    /// Construct a Biquad with 0 initial state from coefficients given as
    /// arguments.
    ///
    /// *CAREFUL*: No checks are don  on validity / stability of the created filter!
    fn fromCoefs(b0: Flt, b1: Flt, b2: Flt, a1: Flt, a2: Flt) -> Biquad {
        Biquad {
            w1: 0.,
            w2: 0.,
            b0,
            b1,
            b2,
            a1,
            a2,
        }
    }

    /// Create unit impulse response biquad filter. Input = output
    pub fn unit() -> Biquad {
        let filter_coefs = &[1., 0., 0., 1., 0., 0.];
        Biquad::new(filter_coefs).unwrap()
    }

    /// Initialize biquad as first order high pass filter. Pre-warps the
    /// bilinear transformation to set the -3 dB point exactly at the cut-on
    /// frequency.
    ///
    /// * fs: Sampling frequency in \[Hz\]
    /// * cuton_Hz: -3 dB cut-on frequency in \[Hz\]
    ///
    pub fn firstOrderHighPass(fs: Flt, cuton_Hz: Flt) -> Result<Biquad> {
        if fs <= 0. {
            bail!("Invalid sampling frequency: {} [Hz]", fs);
        }
        if cuton_Hz <= 0. {
            bail!("Invalid cuton frequency: {} [Hz]", cuton_Hz);
        }
        if cuton_Hz >= 0.98 * fs / 2. {
            bail!(
                "Invalid cuton frequency. We limit this to 0.98* fs / 2. Given value {} [Hz]",
                cuton_Hz
            );
        }
        let omgc = 2. * pi * cuton_Hz;
        let fwarp = Some(cuton_Hz);
        Ok(Biquad::bilinear(fs, &[0., 1., 0.], &[omgc, 1.0, 0.], fwarp))

        // let tau: Flt = 1. / (2. * pi * cuton_Hz);
        // let facnum = 2. * fs * tau / (1. + 2. * fs * tau);
        // let facden = (1. - 2. * fs * tau) / (1. + 2. * fs * tau);

        // Ok(Biquad::fromCoefs(
        //     facnum,  // b0
        //     -facnum, // b1
        //     0.,      // b2,
        //     facden,  // a1
        //     0.,      // a2
        // ))
    }

    /// First order low pass filter, which is a simple moving average (one pole in the real axis). No pre-warping
    /// correction done.
    ///
    /// * `fs` - Sampling frequency \[Hz\]
    /// * `fc` - Cut-off frequency (-3 dB point) \[Hz\]
    pub fn firstOrderMovingAverage(fs: Flt, fc: Flt) -> Result<Biquad> {
        if fc <= 0. {
            bail!("Cuton frequency, given: should be > 0")
        }
        if fc >= fs / 2. {
            bail!("Cuton frequency should be smaller than Nyquist frequency")
        }
        let b0 = pi * fc / (pi * fc + fs);
        let b1 = b0;
        let a1 = (pi * fc - fs) / (pi * fc + fs);

        Ok(Biquad::fromCoefs(b0, b1, 0., a1, 0.))
    }

    #[inline]
    /// Filter single sample, outputs by overwriting input sample.
    pub fn filter_inout_single(&mut self, sample: &mut Flt) {
        let w0 = *sample - self.a1 * self.w1 - self.a2 * self.w2;
        let yn = self.b0 * w0 + self.b1 * self.w1 + self.b2 * self.w2;
        self.w2 = self.w1;
        self.w1 = w0;
        *sample = yn;
    }

    /// Filter input signal, output by overwriting input slice.
    #[inline]
    pub fn filter_inout(&mut self, inout: &mut [Flt]) {
        for sample in inout.iter_mut() {
            self.filter_inout_single(sample);
        }
    }

    /// Create new biquad using bilinear transform. Optionally pre-warps the
    /// filter to correct for the mapping of infinite frequency to Nyquist
    /// frequency.
    ///
    /// The analog filter is defined as:
    ///
    /// ```math
    ///         b0 + b1*s + b2*s^2
    /// H(s) = --------------------
    ///         a0 + a1*s + a2*s^2
    /// ```
    ///
    /// # Args
    ///
    /// - `fs` - Sampling frequency in \[Hz\]
    /// - `b` - 3 Analog coefficients (numerator) of second order filter
    /// - `a` - 3 Analog coefficients of (denominator) second order
    ///   filter.
    /// - `fwarp` - Optional reference frequency for pre-warping in \[Hz\]
    ///
    /// # Panics
    ///
    /// - when a.len() or b.len() not equal to 3
    /// - when fref >= fs
    /// - when fs <= 0.
    ///
    pub fn bilinear(fs: Flt, b: &[Flt], a: &[Flt], fwarp: Option<Flt>) -> Biquad {
        assert!(b.len() == 3);
        assert!(a.len() == 3);
        assert!(fs > 0.);

        let T = 1. / fs;
        let (b0a, b1a, b2a, a0a, a1a, a2a) = (b[0], b[1], b[2], a[0], a[1], a[2]);

        // See: https://en.wikipedia.org/wiki/Bilinear_transform
        let K = if let Some(fref) = fwarp {
            assert!(fref < fs);
            let omg0 = fref * 2. * pi;
            omg0 / (omg0 * T / 2.).tan()
        } else {
            2. / T
        };
        let Ksq = K.powi(2);
        //
        let a0fac = a2a * Ksq + a1a * K + a0a;
        // Coefficient b0
        let b0 = (b2a * Ksq + b1a * K + b0a) / a0fac;
        // Coefficient b1
        let b1 = (2. * b0a - 2. * b2a * Ksq) / a0fac;
        // Coefficient b2
        let b2 = (b2a * Ksq - b1a * K + b0a) / a0fac;

        // Coefficient a1
        let a1 = (2. * a0a - 2. * a2a * Ksq) / a0fac;
        // Coefficient a2
        let a2 = (a2a * Ksq - a1a * K + a0a) / a0fac;

        Biquad::fromCoefs(b0, b1, b2, a1, a2)
    }

    /// Create biquad using bilinear transform (BLT) and given analogue zeros,
    /// poles and gain values. Can only deal with a maximum of two poles /
    /// zeros. This restriction is already enforced by only allowing
    /// [PoleOrZero] values as inputs.
    ///
    /// # Args
    ///
    /// - `fs`    - Sampling frequency in \[Hz\]
    /// - `z`     - Optional zero, or zero pair, units are \[rad/s\]
    /// - `p`     - Optional pole or pole pair, units are \[rad/s\]
    /// - `k`     - Gain value. Arbitrary units. If not given, uses value of 1.0.
    /// - `fwarp` - Warp point frequency. Used to correct for frequency warping
    ///   in BLT for pre-warping the transform.
    pub fn bilinear_zpk(
        fs: Flt,
        z: Option<PoleOrZero>,
        p: Option<PoleOrZero>,
        k: Option<Flt>,
        fwarp: Option<Flt>,
    ) -> Biquad {
        // k defaults to 1.0
        let k = if let Some(k) = k { k } else { 1.0 };

        // The zpk form:

        //          (s-z1)*(s-z2)...
        // H(s) = k ------------------
        //          (s-p1)*(s-p2)...

        // The nominal form:
        //         b0 + b1*s + b2*s^2
        // H(s) = ---------------------
        //         a0 + a1*s + a2*s^2

        // Note that here also we have one 'DOF' too much, in the sense that an
        // infinite number of models of the nominal form can fit a zpk form. We
        // restrict ourselve to the case that a0 = Π(-p_i), which is the
        // simplest.

        // If we have a single zero, the math says:
        // k*(s-z) = b0 + b1*s --> b1 = k, b0 = -k*z

        // If we have a set of two zeros, the math says:
        // k*(s-z1)*(s-z2) = b0 + b1*s + b2*s^2 -->
        //                            b0 = k*z1*z2
        //                            b1 = -k*(z1+z2)
        //                            b2 = k
        // Note that when z = z1 = z2.conj(), this simplifies to:
        //                            b0 = k*abs(z)**2
        //                            b1 = -2*k*real(z)
        //                            b2 = k

        let b = if let Some(z) = z {
            match z {
                PoleOrZero::Complex(z) => [k * z.norm_sqr(), -2. * k * z.re(), k],
                PoleOrZero::Real1(z) => [-k * z, k, 0.],
                PoleOrZero::Real2(z1, z2) => [k * z1 * z2, -k * (z1 + z2), k],
            }
        } else {
            [k, 0., 0.]
        };

        // For a single pole:
        // (s-p) = a0 + a1*s --> a0 = -p, a1 = 1.

        // If we have a set of two poles, the math says:
        // (s-p1)*(s-p2) = a0 + a1*s + a2*s^2 -->
        //                            a0 = p1*p2
        //                            a1 = -k*(p1+p2)
        //                            a2 = 1.0
        // Note that when p = p1 = p2.conj(), this simplifies to:
        //                            a0 = abs(p)**2
        //                            a1 = -2*real(p)
        //                            a2 = 1.0
        let a = if let Some(p) = p {
            match p {
                PoleOrZero::Complex(p) => [p.norm_sqr(), -2. * p.re(), 1.0],
                PoleOrZero::Real1(p) => [-p, 1.0, 0.],
                PoleOrZero::Real2(p1, p2) => [p1 * p2, -(p1 + p2), 1.0],
            }
        } else {
            [1., 0., 0.]
        };
        Biquad::bilinear(fs, &b, &a, fwarp)
    }
}
impl Default for Biquad {
    /// Unit impulse (does not transform signal whatsoever)
    fn default() -> Self {
        Biquad::unit()
    }
}

impl Filter for Biquad {
    fn filter(&mut self, input: &[Flt]) -> Vec<Flt> {
        let mut out = input.to_vec();
        self.filter_inout(&mut out);
        // println!("{:?}", out);
        out
    }
    fn reset(&mut self) {
        self.w1 = 0.;
        self.w2 = 0.;
    }
    fn clone_dyn(&self) -> Box<dyn Filter> {
        Box::new(*self)
    }
}
impl<'a, T: AsArray<'a, Flt>> TransferFunction<'a, T> for Biquad {
    fn tf(&self, fs: Flt, freq: T) -> Ccol {
        let freq = freq.into();

        freq.mapv(|f| {
            let zm = Complex::exp(-I * 2. * pi * f / fs);
            let num = self.b0 + self.b1 * zm + self.b2 * zm * zm;
            let den = 1. + self.a1 * zm + self.a2 * zm * zm;
            num / den
        })
    }
}

#[cfg(test)]
mod test {
    use approx::assert_abs_diff_eq;
    use num::{complex::ComplexFloat, integer::sqrt};

    use super::*;

    #[test]
    fn test_biquad1() {
        let mut ser = Biquad::unit();
        let inp = vec![1., 0., 0., 0., 0., 0.];
        let filtered = ser.filter(&inp);
        assert_eq!(&filtered, &inp);
    }
    #[test]
    fn test_setDC() {
        let mut b = Biquad::firstOrderMovingAverage(7., 1.).unwrap();
        let dc = 7.8;
        b.setToDCValue(dc);

        let mut x = dc;
        b.filter_inout_single(&mut x);
        assert_abs_diff_eq!(x, dc, epsilon = Flt::EPSILON * 10.)
    }

    #[test]
    fn test_firstOrderLowpass() {
        let fs = 1e5;
        let fc = 10.;
        let b = Biquad::firstOrderMovingAverage(fs, fc).unwrap();
        println!("b = {b:#?}");
        let mut freq = Dcol::from_elem(5, 0.);
        freq[1] = fc;
        freq[2] = fs / 2.;
        let tf = b.tf(fs, freq.view());

        let epsilon = Flt::EPSILON * 150.;
        assert_abs_diff_eq!(tf[0].re, 1., epsilon = 10. * epsilon);
        assert_abs_diff_eq!(tf[0].im, 0., epsilon = epsilon);
        assert_abs_diff_eq!(tf[1].abs(), 1. / Flt::sqrt(2.), epsilon = 1e-4);
    }
    #[test]
    fn test_bilinear() {
        let fc = 100.;
        let omgc = 2. * pi * fc;
        let fs = 2e3;
        let b1 = Biquad::firstOrderMovingAverage(fs, fc).unwrap();
        let b2 = Biquad::bilinear_zpk(fs, None, Some(PoleOrZero::Real1(-omgc)), Some(omgc), None);
        println!("b1 = {b1:?}");
        println!("b2 = {b2:?}");
        let epsilon = Flt::EPSILON * 10.;
        println!("Epsilon = {epsilon}");
        assert_abs_diff_eq!(
            (b1.tf(fs, &[0.])[0] - Cflt::ONE).abs(),
            0.,
            epsilon = epsilon
        );
        assert_abs_diff_eq!(
            (b2.tf(fs, &[0.])[0] - Cflt::ONE).abs(),
            0.,
            epsilon = epsilon
        );
        // assert_eq!(b1, b2);
        assert_abs_diff_eq!((b1.tf(fs, &[fs / 2.])[0]).abs(), 0., epsilon = epsilon);
        assert_abs_diff_eq!((b2.tf(fs, &[fs / 2.])[0]).abs(), 0., epsilon = epsilon);
    }
    #[test]
    fn test_firstOrderHighPass() {
        let fc = 100.;
        let fs = 4e3;
        let b3 = Biquad::firstOrderHighPass(fs, fc).unwrap();

        println!("b3 = {b3:?}");
        let epsilon = Flt::EPSILON * 10.;
        assert_abs_diff_eq!((b3.tf(fs, &[0.])[0]).abs(), 0., epsilon = epsilon);
        assert_abs_diff_eq!(
            (b3.tf(fs, &[(fs - fs / 1e9) / 2.])[0]).abs(),
            1.,
            epsilon = epsilon
        );
        assert_abs_diff_eq!((b3.tf(fs, &[fc])[0]).abs(), (0.5).sqrt(), epsilon = epsilon);
        // let freq = &[0., 10.,100.,1000., 2000.];
        // println!("{:?}", b3.tf(fs, freq));
    }
}
