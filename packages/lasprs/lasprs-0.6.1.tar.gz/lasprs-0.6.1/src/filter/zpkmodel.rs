use super::butter::butter_lowpass_roots;
use super::{Biquad, SeriesBiquad, TransferFunction};
use crate::{config::*, ps::FreqWeighting};
use itertools::{EitherOrBoth, Itertools};
use num::{zero, Complex};
use std::cmp::{max, min};

/// Reasonable maximum order of Butterworth filters.
pub const BUTTER_MAX_ORDER: u32 = 40;
/// Specification of a filter for a certain type.
///
/// The order corresponds to the rolloff in dB/decade. order=1 means 20
/// dB/dec, order=2 40 dB/dec and so on. For a bandpass filter, the order also
/// corresponds to the roll-off and roll-on of the filter. For this case, the
/// order is not 'shared' between the highpass and lowpass part.
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Debug, Copy, Clone, PartialEq)]
pub enum FilterSpec {
    /// Bandpass filter. Cuton frequency `fl` in \[Hz\]. Cutoff frequency `fu`
    /// in \[Hz\]. Typically implemented as a highpass combined with a lowpass.
    Bandpass {
        /// Lower cut-on frequency \[Hz\]
        fl: Flt,
        /// Higher cut-off frequency \[Hz\]
        fu: Flt,
        /// Filter order n*20 dB/dec roll-on and off
        order: u32,
    },
    /// Lowpass filter. Cutoff frequency `fc` in \[Hz\].
    Lowpass {
        /// Cut-off frequency \[Hz\]
        fc: Flt,

        /// Filter order n*20 dB/dec roll-on and off
        order: u32,
    },
    /// Highpass filter. Cuton frequency `fc` in \[Hz\].
    Highpass {
        /// Cut-on frequency \[Hz\]
        fc: Flt,
        /// Filter order n*20 dB/dec roll-on and off
        order: u32,
    },
}

/// Analog zero-pole-gain model for real input to real output. Provides methods
/// to generate analog filters of standard type, i.e. bandpass, lowpass and
/// highpass. These can subsequentially be used to generate a digital filter.
///
///
/// # Example: Create a digital second order Butterworth bandpass filter
///
/// ```rust
/// use lasprs::filter::{FilterSpec, ZPKModel};
/// let fs = 48000.;
///
/// let butter = ZPKModel::butter(FilterSpec::Bandpass{fl: 10., fu: 100., order: 2});
/// let mut filt = butter.bilinear(fs);
///
/// ```
///
/// It has a transfer function that can be described as a rational function of
/// the form:
///         
/// ```math
///          Π_i (s-z_i)
/// H(s) = k ------------
///          Π_i (s-p_i)
/// ```
///
/// where `Π` denotes the product of a series, `z_i` are the zeros, and `p_i`
/// are the poles. In order to have real output for a real input, the zeros and
/// poles should either be real, or come in complex conjugate pairs. This is
/// enforced by the way the poles and zero's are internally stored.
///
#[derive(Clone, Debug)]
#[cfg_attr(feature = "python-bindings", pyclass)]
pub struct ZPKModel {
    // List of zeros
    z: Vec<PoleOrZero>,
    // List of poles
    p: Vec<PoleOrZero>,
    // Gain factor
    k: Flt,

    // Optional: prewarping critical frequency. Used when using bilinear
    // transform to create digital filter of this analogue one.
    fwarp: Option<Flt>,
}
impl Default for ZPKModel {
    fn default() -> Self {
        ZPKModel {
            z: vec![],
            p: vec![],
            k: 1.0,
            fwarp: None,
        }
    }
}
impl<'a, T: AsArray<'a, Flt>> TransferFunction<'a, T> for ZPKModel {
    fn tf(&self, _fs: Flt, freq: T) -> Ccol {
        let freq = freq.into();
        freq.mapv(|freq| {
            let s = 2. * I * pi * freq;
            let mut res = Cflt::ONE;
            use PoleOrZero::*;
            self.z.iter().for_each(|z| match z {
                Complex(z) => {
                    res *= (s - z) * (s - z.conj());
                }
                Real1(z) => {
                    res *= s - z;
                }
                Real2(z1, z2) => {
                    res *= (s - z1) * (s - z2);
                }
            });
            self.p.iter().for_each(|p| match p {
                Complex(p) => {
                    res *= 1. / ((s - p) * (s - p.conj()));
                }
                Real1(p) => {
                    res *= 1. / (s - p);
                }
                Real2(p1, p2) => {
                    res *= 1. / ((s - p1) * (s - p2));
                }
            });
            res *= self.k;
            res
        })
    }
}

use std::ops::Mul;
impl Mul for ZPKModel {
    type Output = Self;
    // Combines two ZPK model transfer functions into one
    fn mul(self, rhs: ZPKModel) -> Self {
        let (mut z, mut p, mut k) = (self.z, self.p, self.k);
        k *= rhs.k;
        z.extend(rhs.z);
        p.extend(rhs.p);
        ZPKModel {
            z,
            p,
            k,
            ..Default::default()
        }
    }
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl ZPKModel {
    #[pyo3(name = "butter")]
    #[staticmethod]
    fn butter_py<'py>(spec: FilterSpec) -> ZPKModel {
        ZPKModel::butter(spec)
    }

    #[pyo3(name = "freqWeightingFilter")]
    #[staticmethod]
    fn freqWeightingFilter_py(fw: FreqWeighting) ->ZPKModel {
        Self::freqWeightingFilter(fw)
    }

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    /// See: [ZPKModel::tf]
    #[pyo3(name = "tf")]
    fn tf_py<'py>(
        &self,
        py: Python<'py>,
        fs: Flt,
        freq: PyArrayLike1<Flt>,
    ) -> PyResult<PyArr1Cflt<'py>> {
        let freq = freq.as_array();
        let res = PyArray1::from_array_bound(py, &self.tf(fs, freq));
        Ok(res)
    }

    /// See: [ZPKModel::tf]
    #[pyo3(name = "bilinear")]
    fn bilinear_py(&self, fs: Flt) -> SeriesBiquad {
        self.bilinear(fs)
    }
}
impl ZPKModel {
    /// Creata a new ZPK model, with give list of poles and zeros, and gain
    ///
    /// # Args
    ///
    /// - `zeros` - list like struct of zeros. Can be a `Vec<ZeroOrPole>` or an
    ///   `&[ZeroOrPole]`.
    /// - `poles` - list like struct of poles. Can be a `Vec<ZeroOrPole>` or an
    ///   `&[ZeroOrPole]`.
    /// - `k` - linear gain.
    pub fn new<T, U>(zeros: T, poles: U, k: Flt) -> ZPKModel
    where
        T: Into<Vec<PoleOrZero>>,
        U: Into<Vec<PoleOrZero>>,
    {
        let z = zeros.into();
        let p = poles.into();
        ZPKModel {
            z,
            p,
            k,
            ..Default::default()
        }
        .compactize()
    }

    // Combine real poles / zeros for two Real1s to 1 Real2.
    fn combine_reals(v: Vec<PoleOrZero>) -> Vec<PoleOrZero> {
        let mut real1: Option<PoleOrZero> = None;
        let mut v: Vec<PoleOrZero> = v
            .iter()
            .filter_map(|z| match z {
                PoleOrZero::Complex(z) => Some(PoleOrZero::Complex(*z)),
                PoleOrZero::Real2(z1, z2) => Some(PoleOrZero::Real2(*z1, *z2)),
                PoleOrZero::Real1(z) => {
                    if let Some(real1) = real1.take() {
                        if let PoleOrZero::Real1(z2) = real1 {
                            return Some(PoleOrZero::Real2(z2, *z));
                        } else {
                            unreachable!()
                        }
                    } else {
                        real1 = Some(PoleOrZero::Real1(*z));
                        return None;
                    }
                }
            })
            .collect();

        // A leftover real1, push it at the end
        if let Some(real1) = real1 {
            if let PoleOrZero::Real1(z) = real1 {
                v.push(PoleOrZero::Real1(z));
            } else {
                unreachable!()
            }
        }

        v
    }
    // Compactice filter, combines real1 poles/zeros to create more real2 poles/zeros.
    fn compactize(self) -> ZPKModel {
        let (z, p, k, fwarp) = (self.z, self.p, self.k, self.fwarp);
        let z = Self::combine_reals(z);
        let p = Self::combine_reals(p);

        ZPKModel { z, p, k, fwarp }
    }

    /// Set critical frequency in filter, used for bilinear transform.
    ///
    /// # Args
    ///
    /// - `fcrit` - New critical frequency in \[Hz\].
    pub fn setWarpFreq(mut self, fcrit: Flt) -> ZPKModel {
        self.fwarp = Some(fcrit);
        self
    }
    /// Change the gain value such that it matches `val` at frequency `freq`.
    /// Does not change the phase at the given frequency.
    pub fn setGainAt(mut self, freq: Flt, required_gain: Flt) -> ZPKModel {
        assert!(required_gain > 0.);
        let freq = [freq];
        let cur_gain_at_freq = self.tf(-1.0, &freq)[0].abs();
        let gain_fac = required_gain / cur_gain_at_freq;
        // Update overall gain to set it equal to val
        self.k *= gain_fac;
        self
    }

    // For each original pole in the lowpass filter, generate new poles and
    // zeros that transform the lowpass filter to a bandpass filter with mid
    // frequency of `fc` and bandwidth `Bw_Hz` = fu-fl.
    // Returns first a list of new poles, and secondly a list of extra zeros.
    fn replace_poles_lp2bp(
        pzlp: PoleOrZero,
        fc: Flt,
        Bw_Hz: Flt,
    ) -> (Vec<PoleOrZero>, Vec<PoleOrZero>) {
        let omgc = 2. * pi * fc;
        let mut new_poles = Vec::with_capacity(2);
        let mut extra_zeros = Vec::with_capacity(2);

        let omgcsq = omgc.powi(2);

        match pzlp {
            PoleOrZero::Real1(pz) => {
                // Scale each pole or zero from the original cut-off frequency
                // of the low-pass filter to the new bandwidth divided by 2
                let pz_lp = pz * Bw_Hz / fc / 2.;
                let sq = pz_lp.powi(2) - omgcsq;
                if sq >= 0. {
                    let sqrt = sq.sqrt();
                    // For every 2 poles that are the result of a single
                    // original pole, we will have 1 new zero
                    extra_zeros.push(PoleOrZero::Real1(0.));
                    new_poles.push(PoleOrZero::Real2(
                        pz_lp + sqrt, // Two new poles or zeros
                        pz_lp - sqrt, // Two new poles or zeros
                    ));
                } else {
                    let sqrt = (sq + 0. * I).sqrt();
                    // For every 2 poles that are the result of a single
                    // original pole, we will have 1 new zero. A complex pole
                    // also has its complex conjugate as a new pole, zo we have
                    // one real zero here.
                    extra_zeros.push(PoleOrZero::Real1(0.));
                    new_poles.push(PoleOrZero::Complex(pz_lp + sqrt));
                }
            }
            PoleOrZero::Real2(z1, z2) => {
                // We do this in two parts. Not the most efficient, but we see
                // filter calculation as a `once in a while calculation`.
                for z in [z1, z2] {
                    let (np, ez) = Self::replace_poles_lp2bp(PoleOrZero::Real1(z), fc, Bw_Hz);
                    new_poles.extend(np);
                    extra_zeros.extend(ez);
                }
            }
            PoleOrZero::Complex(pz) => {
                // Scale each pole or zero from the original cut-off frequency
                // of the low-pass filter to the new bandwidth divided by 2
                let pz_lp = pz * Bw_Hz / fc / 2.;
                let sqrt = (pz_lp.powi(2) - omgcsq).sqrt();
                extra_zeros.push(PoleOrZero::Real2(0., 0.));
                new_poles.push(PoleOrZero::Complex(pz_lp + sqrt));
                new_poles.push(PoleOrZero::Complex(pz_lp - sqrt));
            }
        }
        (new_poles, extra_zeros)
    }

    fn lowpass_to_bandpass(self, fc: Flt, Bw_Hz: Flt) -> ZPKModel {
        // Lowpass to bandpass transformation. Means, we map:
        //        s^2 + omg_1 * omg_2
        // s -> --------------------
        //       ( omg_2 - omg_1) + s

        // This means, for each (s - z), we get:
        //
        //             s^2 -z*s + omg_1 * omg_2 - z*(omg_2-omg_1)
        // (s-z)  ->  ---------------------------------------------
        //                    ( omg_2 - omg_1) + s

        // So:
        // - we get a new pole real at omg_1 - omg_2
        // - And a new zero at: 0

        let (mut z, p, k, fwarp) = (self.z, self.p, self.k, self.fwarp);
        // Does not *yet* work with zeros in the lowpass filter.
        assert!(z.len() == 0);
        let mut new_poles = Vec::with_capacity(2 * p.len());

        // Replace poles with new poles of the bandpass flter, add extra zeros
        // to the list of zeros
        for p in p {
            let (new_poles_current, extra_zeros_current) = Self::replace_poles_lp2bp(p, fc, Bw_Hz);
            new_poles.extend(new_poles_current);
            z.extend(extra_zeros_current);
        }

        ZPKModel {
            z,
            p: new_poles,
            k,
            fwarp,
        }
    }

    fn check_spec(spec: FilterSpec) {
        let check_fc = |fc| assert!(fc > 0., "Cut-off frequency should be > 0");
        let check_order = |order| {
            assert!(
                order > 0 && order <= BUTTER_MAX_ORDER,
                "Invalid filter order"
            )
        };

        match spec {
            FilterSpec::Lowpass { fc, order } => {
                check_fc(fc);
                check_order(order);
            }
            FilterSpec::Highpass { fc, order } => {
                check_fc(fc);
                check_order(order);
            }
            FilterSpec::Bandpass { fl, fu, order } => {
                assert!(
                    fl <= fu && fl > 0.,
                    "Invalid cut-on and cut-off frequency specified"
                );
                check_order(order);
            }
        }
    }
    /// Create a Butterworth filter according to a certain specification in
    /// `spec`.
    ///
    /// # Panics
    ///
    /// - If specified `order == 0`
    /// - If order is larger than [BUTTER_MAX_ORDER].
    /// - If for a bandpass filter `fl>=fu`.
    /// - If `fl`, or `fu < 0`.
    pub fn butter(spec: FilterSpec) -> ZPKModel {
        Self::check_spec(spec);
        match spec {
            FilterSpec::Lowpass { fc, order } => {
                let p = butter_lowpass_roots(fc, order as u32).collect();
                let z = vec![];
                ZPKModel {
                    z,
                    p,
                    k: 1.0,
                    ..Default::default()
                }
                .compactize()
                .setGainAt(fc, (0.5).sqrt())
                .setWarpFreq(fc)
            }
            FilterSpec::Highpass { fc, order } => {
                let p = butter_lowpass_roots(fc, order as u32).collect();
                let z = vec![PoleOrZero::Real1(0.); order as usize];
                ZPKModel {
                    z,
                    p,
                    k: 1.0,
                    ..Default::default()
                }
                .compactize()
                .setGainAt(fc, (0.5).sqrt())
                .setWarpFreq(fc)
            }
            FilterSpec::Bandpass { fl, fu, order } => {
                let fmid = (fl * fu).sqrt();
                let Bw_Hz = fu - fl;
                let lp = Self::butter(FilterSpec::Lowpass { fc: fmid, order });
                Self::lowpass_to_bandpass(lp, fmid, Bw_Hz)
                    .compactize()
                    .setGainAt(fmid, 1.0)
                    .setWarpFreq(fmid)
            }
        }
    }
    /// Apply bilinear transform to obtain series biquads from this ZPK model.
    /// Pre-warping is taken into account, based on settings stored in
    /// [ZPKModel]. Using [ZPKModel::setWarpFreq], this can be overridden.
    ///
    /// # Args
    ///
    /// - `fs` - Sampling frequency \[Hz\]
    ///
    pub fn bilinear(&self, fs: Flt) -> SeriesBiquad {
        let mut biqs = vec![];

        // We spread the gain over all biquads.
        let max_len = max(self.z.len(), self.p.len());
        if max_len == 0 {
            // No poles or zeros, return a gain-only biquad series with only one
            // biquad.
            return SeriesBiquad::new(&[self.k, 0., 0., 1., 0., 0.]).unwrap();
        }
        // Convert to floating point
        let max_len = max_len as Flt;

        // Spread gain over all biquads
        let k_fac = self.k.powf(1. / max_len);

        for case in self.z.iter().zip_longest(&self.p) {
            match case {
                EitherOrBoth::Both(z, p) => {
                    biqs.push(Biquad::bilinear_zpk(
                        fs,
                        Some(*z),
                        Some(*p),
                        Some(k_fac),
                        self.fwarp,
                    ));
                }
                EitherOrBoth::Left(z) => {
                    biqs.push(Biquad::bilinear_zpk(
                        fs,
                        Some(*z),
                        None,
                        Some(k_fac),
                        self.fwarp,
                    ));
                }
                EitherOrBoth::Right(p) => {
                    biqs.push(Biquad::bilinear_zpk(
                        fs,
                        None,
                        Some(*p),
                        Some(k_fac),
                        self.fwarp,
                    ));
                }
            }
        }
        SeriesBiquad::newFromBiqs(biqs)
    }

    /// Create analog filter prototype for a frequency weighting as used in
    /// Sound Level Meters.
    ///
    /// # Args
    ///
    /// - `wt` - `[FreqWeighting]` to use. i.e. A-weighting.
    ///
    /// # Examples
    ///
    /// ## Get part of pulse response of digital A-filter at 48 kHz
    ///
    /// ```
    /// use lasprs::filter::{ZPKModel, FreqWeighting, Filter};
    ///
    /// // Sampling frequency in Hz
    /// let fs = 48000.;
    ///
    /// let mut afilter = ZPKModel::freqWeightingFilter(FreqWeighting::A).bilinear(fs);
    /// let mut data = [0.; 1000];
    /// data[0] = 1.0;
    /// let out = afilter.filter(&data);
    /// ```
    ///
    pub fn freqWeightingFilter(wt: FreqWeighting) -> ZPKModel {
        if let FreqWeighting::Z = wt {
            return ZPKModel {
                z: vec![],
                p: vec![],
                k: 1.0,
                fwarp: None,
            };
        }

        let fr: Flt = 1000.;
        let fL: Flt = num::Float::powf(10., 1.5);
        let fH: Flt = num::Float::powf(10., 3.9);

        let sq5: Flt = num::Float::powf(5., 0.5);

        let fLsq = fL.powi(2);
        let fHsq: Flt = fH.powi(2);
        let frsq: Flt = fr.powi(2);
        let fA = num::Float::powf(10., 2.45);
        let D = Flt::sqrt(0.5);

        let b = (1. / (1. - D)) * (frsq + fLsq * fHsq / frsq - D * (fLsq + fHsq));
        let c = fLsq * fHsq;
        let f2 = (3. - sq5) / 2. * fA;
        let f3 = (3. + sq5) / 2. * fA;

        let sqrtfac = (b.powi(2) - 4. * c).sqrt();
        let f1 = ((-b - sqrtfac) / 2.).sqrt();
        let f4 = ((-b + sqrtfac) / 2.).sqrt();

        let p1 = 2. * pi * f1;
        let p2 = 2. * pi * f2;
        let p3 = 2. * pi * f3;
        let p4 = 2. * pi * f4;
        println!("{b} {p1}, {p2}, {p3}, {p4}");

        let (zeros, poles) = match wt {
            FreqWeighting::Z => {
                unreachable!()
            }
            FreqWeighting::C => {
                let zeros = vec![PoleOrZero::Real2(0., 0.)];
                let poles = vec![PoleOrZero::Real2(-p1, -p1), PoleOrZero::Real2(-p4, -p4)];
                (zeros, poles)
            }
            FreqWeighting::A => {
                let poles = vec![
                    PoleOrZero::Real2(-p1, -p1),
                    PoleOrZero::Real2(-p2, -p3),
                    PoleOrZero::Real2(-p4, -p4),
                ];
                let zeros = vec![PoleOrZero::Real2(0., 0.), PoleOrZero::Real2(0., 0.)];
                (zeros, poles)
            }
        };

        ZPKModel::new(zeros, poles, 1.0).setGainAt(1000., 1.0)
    }
}

/// Enumeration describing a pole or zero, a complex conjugate pair, a single
/// real pole / zero, or a set of two real poles / zeros, or nothing at all.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum PoleOrZero {
    /// Complex conjugate pair, only single one listed, other one can be
    /// inferred.
    Complex(Cflt),
    /// Set of two real poles / zeros
    Real2(Flt, Flt),
    /// Single zero / pole
    Real1(Flt),
}

#[cfg(test)]
mod test{
    use super::ZPKModel;


    #[test]
    fn test_A() {
        let Aw = ZPKModel::freqWeightingFilter(crate::FreqWeighting::A);
    }
}
