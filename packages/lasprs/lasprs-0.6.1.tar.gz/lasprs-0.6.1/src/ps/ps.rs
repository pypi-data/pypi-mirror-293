use crate::config::*;
use ndarray::parallel::prelude::*;
use num::pow::Pow;
use reinterpret::reinterpret_slice;
use std::sync::Arc;
use std::usize;

use crate::Dcol;

use super::fft::FFT;
use super::window::*;
use std::mem::MaybeUninit;

use realfft::{RealFftPlanner, RealToComplex};

/// Cross power spectra, which is a 3D array, with the following properties:
///
/// - The first index is the frequency index, starting at DC, ending at nfft/2.
/// - The second, and third index result in `[i,j]` = C_ij = p_i  * conj(p_j)
///
pub type CPSResult = Array3<Cflt>;

/// Extra typical methods that are of use for 3D-arrays of complex numbers, that
/// are typically implemented as cross-power spectra.
pub trait CrossPowerSpecra {
    /// Returns the autopower for a single channel, as a array of real values
    /// (imaginary part is zero and is stripped off).
    ///
    /// # Args
    ///
    /// - `ch` - The channel number to compute autopower for.
    fn ap(&self, ch: usize) -> Array1<Flt>;

    /// Returns the transfer function from `chi` to `chj`, that is ~ Pj/Pi a
    /// single channel, as a array of complex numbers.
    ///
    /// # Args
    ///
    /// - `chi` - The channel number of the *denominator*
    /// - `chj` - The channel number of the *numerator*
    /// - `chRef` - Optional, a reference channel that has the lowest noise. If
    ///   not given, the average of the two autopowers is used, which gives
    ///   always a worse result than when two a low noise reference channel is
    ///   used.
    ///
    fn tf(&self, chi: usize, chj: usize, chRef: Option<usize>) -> Array1<Cflt>;
}

impl CrossPowerSpecra for CPSResult {
    fn ap(&self, ch: usize) -> Array1<Flt> {
        // Slice out one value for all frequencies, map to only real part, and
        // return.
        self.slice(s![.., ch, ch]).mapv(|f| f.re)
    }
    // fn apsp
    fn tf(&self, chi: usize, chj: usize, chRef: Option<usize>) -> Array1<Cflt> {
        match chRef {
            None => {
                let cij = self.slice(s![.., chi, chj]);
                let cii = self.slice(s![.., chi, chi]);
                let cjj = self.slice(s![.., chj, chj]);
                Zip::from(cij)
                    .and(cii)
                    .and(cjj)
                    .par_map_collect(|cij, cii, cjj| 0.5 * (cij.conj() / cii + cjj / cij))
            }
            Some(chr) => {
                let cir = self.slice(s![.., chi, chr]);
                let cjr = self.slice(s![.., chj, chr]);

                Zip::from(cir)
                    .and(cjr)
                    .par_map_collect(|cir, cjr| cjr / cir)
            }
        }
    }
}

/// Single-sided (cross)power spectra estimator, that uses a Windowed FFT to estimate cross-power
/// spectra. Window functions are documented in the `window` module. Note that
/// directly using this power spectra estimator is generally not useful as it is
/// basically the periodogram estimator, with its high variance.
///
/// This power spectrum estimator is instead used as a building block for for
/// example the computations of spectrograms, or Welch' method of spectral
/// estimation.
///
pub struct PowerSpectra {
    /// Window used in estimator. The actual Window in here is normalized with
    /// the square root of the Window power. This safes one division when
    /// processing time data.
    pub window_normalized: Window,

    ffts: Vec<FFT>,

    // Time-data buffer used for multiplying signals with Window
    timedata: Array2<Flt>,
    // Frequency domain buffer used for storage of signal FFt's in inbetween stage
    freqdata: Array2<Cflt>,
}

impl PowerSpectra {
    /// Returns the FFT length used in power spectra computations
    pub fn nfft(&self) -> usize {
        self.window_normalized.win.len()
    }
    /// Create new power spectra estimator. Uses FFT size from window length
    ///
    /// # Panics
    ///
    /// - If win.len() != nfft
    /// - if nfft == 0
    ///
    /// # Args
    ///
    /// - `window` - A `Window` struct, from which NFFT is also used.
    ///
    pub fn newFromWindow(mut window: Window) -> PowerSpectra {
        let nfft = window.win.len();
        let win_pwr = window.win.mapv(|w| w.powi(2)).sum() / (nfft as Flt);
        let sqrt_win_pwr = Flt::sqrt(win_pwr);
        window.win.mapv_inplace(|v| v / sqrt_win_pwr);

        assert!(nfft > 0);
        assert!(nfft % 2 == 0);

        let mut planner = RealFftPlanner::<Flt>::new();
        let fft = planner.plan_fft_forward(nfft);

        let Fft = FFT::new(fft);

        PowerSpectra {
            window_normalized: window,
            ffts: vec![Fft],
            timedata: Array2::zeros((nfft, 1)),
            freqdata: Array2::zeros((nfft / 2 + 1, 1)),
        }
    }

    /// Compute FFTs of input channel data. Stores the scaled FFT data in
    /// self.freqdata.
    fn compute_ffts(&mut self, timedata: ArrayView2<Flt>) -> ArrayView2<Cflt> {
        let (n, nch) = timedata.dim();
        let nfft = self.nfft();
        assert!(n == nfft);

        // Make sure enough fft engines are available
        while nch > self.ffts.len() {
            self.ffts.push(self.ffts.last().unwrap().clone());
            self.freqdata
                .push_column(Ccol::from_vec(vec![Cflt::new(0., 0.); nfft / 2 + 1]).view())
                .unwrap();
            self.timedata.push_column(Dcol::zeros(nfft).view()).unwrap();
        }

        assert!(n == self.nfft());
        assert!(n == self.window_normalized.win.len());

        // Multiply signals with window function, and compute fft's for each channel
        Zip::from(timedata.axis_iter(Axis(1)))
            .and(self.timedata.axis_iter_mut(Axis(1)))
            .and(&mut self.ffts)
            .and(self.freqdata.axis_iter_mut(Axis(1)))
            .par_for_each(|time_in, mut time_tmp_storage, fft, mut freq| {
                let DC = time_in.mean().unwrap();

                azip!((t in &mut time_tmp_storage, &tin in time_in, &win in &self.window_normalized.win) {
                // Substract DC value from time data, as this leaks into
                // positive frequencies due to windowing.
                // Multiply with window and copy over to local time data buffer
                    *t=(tin-DC)*win});

                fft.process(&time_tmp_storage, &mut freq);
                freq[0] = DC + 0. * I;
            });

        self.freqdata.view()
    }

    /// Compute cross power spectra from input time data. First axis is
    /// frequency, second axis is channel i, third axis is channel j.
    ///
    /// # Panics
    ///
    /// - When `timedata.nrows() != self.nfft()`
    ///
    /// # Args
    ///
    /// * `tdata` - Input time data. This is a 2D array, where the first axis is
    ///   time and the second axis is the channel number.
    ///
    ///  # Returns
    ///
    ///  - 3D complex array of signal cross-powers with the following shape
    ///  (nfft/2+1,timedata.ncols(), timedata.ncols()). Its content is:
    ///  [freq_index, chi, chj] = crosspower: chi*conj(chj)
    ///
    pub fn compute<'a, T>(&mut self, tdata: T) -> CPSResult
    where
        T: AsArray<'a, Flt, Ix2>,
    {
        let tdata = tdata.into();
        let nfft = self.nfft();
        let clen = nfft / 2 + 1;
        if tdata.nrows() != nfft {
            panic!("Invalid timedata length! Should be equal to nfft={nfft}");
        }
        let nchannels = tdata.ncols();

        // Compute fft of input data, and store in self.freqdata
        let fd = self.compute_ffts(tdata);
        let fdconj = fd.mapv(|c| c.conj());

        let result = Array3::uninit((clen, nchannels, nchannels));
        let mut result: Array3<Cflt> = unsafe { result.assume_init() };

        // Loop over result axis one and channel i IN PARALLEL
        Zip::from(result.axis_iter_mut(Axis(1)))
            .and(fd.axis_iter(Axis(1)))
            .par_for_each(|mut out, chi| {
                // out: channel i of output 3D array, channel j all
                // chi: channel i
                Zip::from(out.axis_iter_mut(Axis(1)))
                    .and(fdconj.axis_iter(Axis(1)))
                    .for_each(|mut out, chj| {
                        // out: channel i, j
                        // chj: channel j conjugated
                        Zip::from(&mut out)
                            .and(chi)
                            .and(chj)
                            .for_each(|out, chi, chjc| {
                                // Loop over frequency components
                                *out = 0.5 * chi * chjc;
                            });

                        // The DC component has no 0.5 correction, as it only
                        // occurs ones in a (double-sided) power spectrum. So
                        // here we undo the 0.5 of 4 lines above here.
                        out[0] *= 2.;
                        out[clen - 1] *= 2.;
                    });
            });
        result
    }
}

#[cfg(test)]
mod test {
    use approx::{abs_diff_eq, assert_relative_eq, assert_ulps_eq, ulps_eq};
    // For absolute value
    use num::complex::ComplexFloat;
    use rand_distr::StandardNormal;

    /// Generate a sine wave at the order i
    fn generate_sinewave(nfft: usize, order: usize) -> Dcol {
        Dcol::from_iter(
            (0..nfft).map(|i| Flt::sin(i as Flt / (nfft) as Flt * order as Flt * 2. * pi)),
        )
    }
    /// Generate a sine wave at the order i
    fn generate_cosinewave(nfft: usize, order: usize) -> Dcol {
        Dcol::from_iter(
            (0..nfft).map(|i| Flt::cos(i as Flt / (nfft) as Flt * order as Flt * 2. * pi)),
        )
    }

    use super::*;
    #[test]
    /// Test whether DC part of single-sided FFT has right properties
    fn test_fft_DC() {
        const nfft: usize = 10;
        let rect = Window::new(WindowType::Rect, nfft);
        let mut ps = PowerSpectra::newFromWindow(rect);

        let td = Dmat::ones((nfft, 1));

        let fd = ps.compute_ffts(td.view());
        // println!("{:?}", fd);
        assert_relative_eq!(fd[(0, 0)].re, 1.);
        assert_relative_eq!(fd[(0, 0)].im, 0.);
        let abs_fneq0 = fd.slice(s![1.., 0]).sum();
        assert_relative_eq!(abs_fneq0.re, 0.);
        assert_relative_eq!(abs_fneq0.im, 0.);
    }

    /// Test whether AC part of single-sided FFT has right properties
    #[test]
    fn test_fft_AC() {
        const nfft: usize = 256;
        let rect = Window::new(WindowType::Rect, nfft);
        let mut ps = PowerSpectra::newFromWindow(rect);

        // Start with a time signal
        let mut t: Dmat = Dmat::default((nfft, 0));
        t.push_column(generate_sinewave(nfft, 1).view()).unwrap();
        // println!("{:?}", t);

        let fd = ps.compute_ffts(t.view());
        // println!("{:?}", fd);
        assert_relative_eq!(fd[(0, 0)].re, 0., epsilon = Flt::EPSILON * nfft as Flt);
        assert_relative_eq!(fd[(0, 0)].im, 0., epsilon = Flt::EPSILON * nfft as Flt);

        assert_relative_eq!(fd[(1, 0)].re, 0., epsilon = Flt::EPSILON * nfft as Flt);
        assert_ulps_eq!(fd[(1, 0)].im, -1., epsilon = Flt::EPSILON * nfft as Flt);

        // Sum of all terms at frequency index 2 to ...
        let sum_higher_freqs_abs = Cflt::abs(fd.slice(s![2.., 0]).sum());
        assert_ulps_eq!(
            sum_higher_freqs_abs,
            0.,
            epsilon = Flt::EPSILON * nfft as Flt
        );
    }

    /// Thest whether power spectra scale properly. Signals with amplitude of 1
    /// should come back with a power of 0.5. DC offsets should come in as
    /// value^2 at frequency index 0.
    #[test]
    fn test_ps_scale() {
        const nfft: usize = 124;
        let rect = Window::new(WindowType::Rect, nfft);
        let mut ps = PowerSpectra::newFromWindow(rect);

        // Start with a time signal
        let mut t: Dmat = Dmat::default((nfft, 0));
        t.push_column(generate_cosinewave(nfft, 1).view()).unwrap();
        let dc_component = 0.25;
        let dc_power = dc_component.pow(2);
        t.mapv_inplace(|t| t + dc_component);

        let power = ps.compute(t.view());
        assert_relative_eq!(
            power[(0, 0, 0)].re,
            dc_power,
            epsilon = Flt::EPSILON * nfft as Flt
        );
        assert_relative_eq!(
            power[(1, 0, 0)].re,
            0.5,
            epsilon = Flt::EPSILON * nfft as Flt
        );
        assert_relative_eq!(
            power[(1, 0, 0)].im,
            0.0,
            epsilon = Flt::EPSILON * nfft as Flt
        );
    }

    use ndarray_rand::RandomExt;
    // Test parseval's theorem for some random data
    #[test]
    fn test_parseval() {
        const nfft: usize = 512;
        let rect = Window::new(WindowType::Rect, nfft);
        let mut ps = PowerSpectra::newFromWindow(rect);

        // Start with a time signal
        let t: Dmat = Dmat::random((nfft, 1), StandardNormal);

        let tavg = t.sum() / (nfft as Flt);
        let t_dc_power = tavg.powi(2);
        // println!("dc power in time domain: {:?}", t_dc_power);

        let signal_pwr = t.mapv(|t| t.powi(2)).sum() / (nfft as Flt);
        // println!("Total signal power in time domain: {:?} ", signal_pwr);

        let power = ps.compute(t.view());
        // println!("freq domain power: {:?}", power);

        let fpower = power.sum().abs();

        assert_ulps_eq!(
            t_dc_power,
            power[(0, 0, 0)].abs(),
            epsilon = Flt::EPSILON * (nfft as Flt).powi(2)
        );
        assert_ulps_eq!(
            signal_pwr,
            fpower,
            epsilon = Flt::EPSILON * (nfft as Flt).powi(2)
        );
    }

    // Test parseval's theorem for some random data
    #[test]
    fn test_parseval_with_window() {
        // A sufficiently high value is required here, to show that it works.
        const nfft: usize = 2usize.pow(20);
        let window = Window::new(WindowType::Hann, nfft);
        // let window = Window::new(WindowType::Rect, nfft);
        let mut ps = PowerSpectra::newFromWindow(window);

        // Start with a time signal
        let t: Dmat = 2. * Dmat::random((nfft, 1), StandardNormal);

        let tavg = t.sum() / (nfft as Flt);
        let t_dc_power = tavg.powi(2);
        // println!("dc power in time domain: {:?}", t_dc_power);

        let signal_pwr = t.mapv(|t| t.powi(2)).sum() / (nfft as Flt);
        // println!("Total signal power in time domain: {:?} ", signal_pwr);

        let power = ps.compute(t.view());
        // println!("freq domain power: {:?}", power);

        let fpower = power.sum().abs();

        assert_ulps_eq!(
            t_dc_power,
            power[(0, 0, 0)].abs(),
            epsilon = Flt::EPSILON * (nfft as Flt).powi(2)
        );

        // This one fails when nfft is too short.
        assert_ulps_eq!(signal_pwr, fpower, epsilon = 2e-2);
    }
}
