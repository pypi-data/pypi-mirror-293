use super::timebuffer::TimeBuffer;
use super::CrossPowerSpecra;
use super::*;
use crate::config::*;
use anyhow::{bail, Error, Result};
use derive_builder::Builder;
use freqweighting::FreqWeighting;

/// All settings used for computing averaged power spectra using Welch' method.
#[derive(Builder, Clone)]
#[builder(build_fn(validate = "Self::validate", error = "Error"))]
pub struct ApsSettings {
    /// Mode of computation, see [ApsMode].
    #[builder(default)]
    mode: ApsMode,
    /// Overlap in time segments. See [Overlap].
    #[builder(default)]
    overlap: Overlap,
    /// Window applied to time segments. See [WindowType].
    #[builder(default)]
    windowType: WindowType,
    /// Kind of freqency weighting. Defaults to Z
    #[builder(default)]
    freqWeightingType: FreqWeighting,
    /// FFT Length
    nfft: usize,
    /// Sampling frequency
    fs: Flt,
}

impl ApsSettingsBuilder {
    fn validate(&self) -> Result<()> {
        if !self.fs.is_some() {
            bail!("Sampling frequency not given");
        }
        let fs = self.fs.unwrap();

        if !fs.is_normal() {
            bail!("Sampling frequency not a normal number")
        }
        if fs <= 0.0 {
            bail!("Invalid sampling frequency given as parameter");
        }

        if self.nfft.is_none() {
            bail!("nfft not specified")
        };
        let nfft = self.nfft.unwrap();
        if nfft % 2 != 0 {
            bail!("NFFT should be even")
        }
        if nfft == 0 {
            bail!("Invalid NFFT, should be > 0.")
        }
        // Perform some checks on ApsMode
        if let Some(ApsMode::ExponentialWeighting { tau }) = self.mode {
            if tau <= 0.0 {
                bail!("Invalid time weighting constant [s]. Should be > 0 if given.");
            }
        }

        Ok(())
    }
}
impl ApsSettings {
    /// Returns nfft
    pub fn nfft(&self) -> usize {
        self.nfft
    }
    fn get_overlap_keep(&self) -> usize {
        self.validate_get_overlap_keep().unwrap()
    }
    /// Unpack all, returns parts in tuple
    pub fn get(self) -> (ApsMode, Overlap, WindowType, FreqWeighting, usize, Flt) {
        (
            self.mode,
            self.overlap,
            self.windowType,
            self.freqWeightingType,
            self.nfft,
            self.fs,
        )
    }
    /// Returns the amount of samples to `keep` in the time buffer when
    /// overlapping time segments using [TimeBuffer].
    pub fn validate_get_overlap_keep(&self) -> Result<usize> {
        let nfft = self.nfft;
        let overlap_keep = match self.overlap {
            Overlap::Number(i) if i >= nfft => {
                bail!("Invalid overlap number of samples. Should be < nfft, which is {nfft}.")
            }
            // Keep 1 sample, if overlap is 1 sample etc.
            Overlap::Number(i) if i < nfft => i,

            // If overlap percentage is >= 100, or < 0.0 its an error
            Overlap::Percentage(p) if !(0.0..100.).contains(&p) => {
                bail!("Invalid overlap percentage. Should be >= 0. And < 100.")
            }
            // If overlap percentage is 0, this gives
            Overlap::Percentage(p) => ((p * nfft as Flt) / 100.) as usize,
            Overlap::NoOverlap => 0,
            _ => unreachable!(),
        };
        if overlap_keep >= nfft {
            bail!("Computed overlap results in invalid number of overlap samples. Please make sure the FFT length is large enough, when high overlap percentages are required.");
        }
        Ok(overlap_keep)
    }

    /// Return a reasonable acoustic default with a frequency resolution around
    /// ~ 10 Hz, where nfft is still an integer power of 2.
    ///
    /// # Errors
    ///
    /// If `fs` is something odd, i.e. < 1 kHz, or higher than 1 MHz.
    ///
    pub fn reasonableAcousticDefault(fs: Flt, mode: ApsMode) -> Result<ApsSettings> {
        if fs < 1e3 || fs > 1e6 {
            bail!("Sampling frequency for reasonable acoustic data is >= 1 kHz and <= 1 MHz.");
        }
        let fs_div_10_rounded = (fs / 10.) as u32;

        // 2^30 is about 1 million. We search for a two-power of an nfft that is
        // the closest to fs/10. The frequency resolution is about fs/nfft.
        let nfft = (0..30).map(|i| 2u32.pow(i) - fs_div_10_rounded).fold(
            // Start wth a value that is always too large
            fs as u32 * 10,
            |cur, new| cur.min(new),
        ) as usize;

        Ok(ApsSettings {
            mode,
            fs,
            nfft,
            windowType: WindowType::default(),
            overlap: Overlap::default(),
            freqWeightingType: FreqWeighting::default(),
        })
    }

    /// Return sampling frequency
    pub fn fs(&self) -> Flt {
        self.fs
    }

    /// Return Nyquist frequency
    pub fn fnyq(&self) -> Flt {
        self.fs() / 2.
    }

    /// Returns a single-sided frequency array corresponding to points in Power
    /// spectra computation.
    pub fn getFreq(&self) -> Array1<Flt> {
        let df = self.fs / self.nfft as Flt;
        let K = self.nfft / 2 + 1;
        Array1::linspace(0., (K - 1) as Flt * df, K)
    }
}

///  Provide the overlap of blocks for computing averaged (cross) power spectra.
///  Can be provided as a percentage of the block size, or as a number of
///  samples.
#[derive(Clone, Debug)]
pub enum Overlap {
    /// Overlap specified as a percentage of the total FFT length. Value should
    /// be 0<=pct<100.
    Percentage(Flt),
    /// Number of samples to overlap
    Number(usize),
    /// No overlap at all, which is the same as Overlap::Number(0)
    NoOverlap,
}
impl Default for Overlap {
    fn default() -> Self {
        Overlap::Percentage(50.)
    }
}

/// The 'mode' used in computing averaged power spectra. When providing data in
/// blocks to the [AvPowerSpectra] the resulting 'current estimate' responds
/// differently, depending on the model.
#[derive(Default, Copy, Clone)]
pub enum ApsMode {
    /// Averaged over all data provided. New averages can be created by calling
    /// `AvPowerSpectra::reset()`
    #[default]
    AllAveraging,
    /// In this mode, the `AvPowerSpectra` works a bit like a sound level meter,
    /// where new data is weighted with old data, and old data exponentially
    /// backs off. This mode only makes sense when `tau >> nfft/fs`
    ExponentialWeighting {
        /// Time weighting constant, follows convention of Sound Level Meters.
        /// Means the data is approximately low-pass filtered with a cut-off
        /// frequency f_c of s/tau ≅ 1 → f_c = (2 * pi * tau)^-1.
        tau: Flt,
    },
    /// Spectrogram mode. Only returns the latest estimate(s).
    Spectrogram,
}

/// Averaged power spectra computing engine
/// Used to compute power spectra estimations on
/// long datasets, where nfft << length of data. This way, the variance of a
/// single periodogram is suppressed with increasing number of averages.
///
/// For more information, see the book on numerical recipes.
///
pub struct AvPowerSpectra {
    // Power spectra estimator for single block
    ps: PowerSpectra,

    settings: ApsSettings,

    // The number of samples to keep in the time buffer when overlapping time
    // blocks
    overlap_keep: usize,

    /// The number of blocks of length [self.nfft()] already used in the average
    N: usize,

    /// Storage for sample data.
    timebuf: TimeBuffer,

    // Current estimation of the power spectra
    cur_est: CPSResult,
}
impl AvPowerSpectra {
    /// The FFT Length of estimating (cross)power spectra
    pub fn nfft(&self) -> usize {
        self.ps.nfft()
    }

    /// Resets all state, starting with a clean sleave. After this step, also
    /// the number of channels can be different on the input.
    pub fn reset(&mut self) {
        self.N = 0;
        self.timebuf.reset();
        self.cur_est = CPSResult::zeros((0, 0, 0));
    }
    /// Create new averaged power spectra estimator for weighing over the full
    /// amount of data supplied (no exponential spectra weighting) using
    /// sensible defaults (Hann window, 50% overlap). This is a simpler method
    /// than [AvPowerSpectra.build]. But use with caution, it might panic on
    /// invalid nfft values!
    ///
    /// # Args
    ///
    /// * `fs` - Sampling frequency in \[Hz\]
    /// * `nfft` - FFT Length \[-\]
    ///
    /// # Panics
    ///
    /// - When nfft is not even, or 0.
    /// - When providing invalid sampling frequencies
    ///
    pub fn new_simple_all_averaging(fs: Flt, nfft: usize) -> AvPowerSpectra {
        let mut settings =
            ApsSettings::reasonableAcousticDefault(fs, ApsMode::AllAveraging).unwrap();
        settings.nfft = nfft;
        AvPowerSpectra::new(settings)
    }

    /// Create power spectra estimator which weighs either all data
    /// (`fs_tau=None`), or uses exponential weighting. Other parameters can be
    /// provided, like the overlap (Some(Overlap)). Otherwise: all parameters
    /// have sensible defaults.
    ///
    ///  # Exponential weighting
    ///
    ///  This can be used to `follow` a power spectrum as a function of time.
    ///  New data is weighted more heavily. Note that this way of looking at
    ///  spectra is not 'exact', and therefore should not be used for
    ///  spectrograms.
    ///
    /// # Args
    ///
    /// - `nfft` - The discrete Fourier Transform length used in the estimation.
    /// - `windowtype` - Window Type. The window type to use Hann, etc.
    /// - `overlap` - Amount of overlap in
    /// - `mode` - The mode in which the [AvPowerSpectra] runs. See [ApsMode].
    ///
    pub fn new(settings: ApsSettings) -> AvPowerSpectra {
        let overlap_keep = settings.get_overlap_keep();
        let window = Window::new(settings.windowType, settings.nfft);

        let ps = PowerSpectra::newFromWindow(window);

        AvPowerSpectra {
            ps,
            overlap_keep,
            settings,
            N: 0,
            cur_est: CPSResult::default((0, 0, 0)),
            timebuf: TimeBuffer::new(),
        }
    }
    // Update result for single block
    fn update_singleblock(&mut self, timedata: ArrayView2<Flt>) {
        let Cpsnew = self.ps.compute(timedata);
        // println!("Cpsnew: {:?}", Cpsnew[[0, 0, 0]]);

        // Initialize to zero
        if self.cur_est.is_empty() {
            assert_eq!(self.N, 0);
            self.cur_est = CPSResult::zeros(Cpsnew.raw_dim().f());
        }

        // Update the number of blocks processed
        self.N += 1;

        // Apply operation based on mode
        match self.settings.mode {
            ApsMode::AllAveraging => {
                let Nf = Cflt {
                    re: self.N as Flt,
                    im: 0.,
                };
                self.cur_est = (Nf - 1.) / Nf * &self.cur_est + 1. / Nf * Cpsnew;
            }
            ApsMode::ExponentialWeighting { tau } => {
                debug_assert!(self.N > 0);
                if self.N == 1 {
                    self.cur_est = Cpsnew;
                } else {
                    // A sound level meter specifies a low pass filter with one
                    // real pole at -1/tau, for a time weighting of tau. This
                    // means the analogue transfer function is 1 /
                    // (tau*s+1).

                    // Now we want to approximate this with a digital transfer
                    // function. The step size, or sampling period is:
                    // T = (nfft-overlap_keep)/fs.

                    // Then, when using the matched z-transform (
                    // https://en.wikipedia.org/wiki/Matched_Z-transform_method),
                    // an 1/(s-p) is replaced by 1/(1-exp(p*T)*z^-1).

                    // So the digital transfer function will be:
                    // H[n] ≅ K / (1 - exp(-T/tau) * z^-1).
                    // , where K is a to-be-determined constant, for which we
                    // take the value such that the D.C. gain equals 1. To get
                    // the frequency response at D.C., we have to set z=1, so
                    // to set the D.C. to 1, we have to set K = 1-exp(-T/tau).

                    // Hence:
                    // H[n] ≅ (1- exp(-T/tau)) / (1 - exp(-T/tau) * z^-1).

                    // Or as a finite difference equation:
                    //
                    // y[n] * (1-exp(-T/tau)* z^-1) = (1-exp(-T/tau)) * x[n]

                    // or, finally:
                    // y[n] = alpha * y[n-1] + (1-alpha) * x[n]

                    // where alpha = exp(-T/tau).
                    let T = (self.nfft() - self.overlap_keep) as Flt / self.settings.fs;
                    let alpha = Cflt::ONE * Flt::exp(-T / tau);
                    self.cur_est = alpha * &self.cur_est + (1. - alpha) * Cpsnew;
                }
            }

            ApsMode::Spectrogram => {
                self.cur_est = Cpsnew;
            }
        }
    }
    /// Computes average (cross)power spectra, and returns only the most recent
    /// estimate, if any can be given back. Only gives back a result when enough
    /// data is available.
    ///
    /// # Args
    ///
    /// * `timedata``: New available time data. Number of columns is number of
    ///   channels, number of rows is number of frames (samples per channel).
    ///
    /// # Panics
    ///
    /// If timedata.ncols() does not match number of columns in already present
    /// data.
    pub fn compute_last<'a, 'b, T>(&'a mut self, timedata: T) -> Option<&'a CPSResult>
    where
        T: AsArray<'b, Flt, Ix2>,
    {
        // Push new data in the time buffer.
        self.timebuf.push(timedata);

        // Flag to indicate that we have obtained one result for sure.
        let mut computed_single = false;

        // Iterate over all blocks that can come,
        while let Some(timeblock) = self.timebuf.pop(self.nfft(), self.overlap_keep) {
            // Compute cross-power spectra for current time block
            self.update_singleblock(timeblock.view());

            computed_single = true;
        }
        if computed_single {
            return Some(&self.cur_est);
        }
        None
    }

    /// Computes average (cross)power spectra, and returns all intermediate
    /// estimates that can be calculated. This is useful when plotting spectra
    /// as a function of time, and intermediate results need also be plotted.
    ///
    /// # Args
    ///
    /// * `timedata``: New available time data. Number of columns is number of
    ///   channels, number of rows is number of frames (samples per channel).
    ///
    /// # Panics
    ///
    /// If timedata.ncols() does not match number of columns in already present
    /// data.
    pub fn compute_all<'a, 'b, T>(&'a mut self, timedata: T) -> Vec<CPSResult>
    where
        T: AsArray<'b, Flt, Ix2>,
    {
        // Push new data in the time buffer.
        self.timebuf.push(timedata);

        // Storage for the result
        let mut result = Vec::new();

        // Iterate over all blocks that can come,
        while let Some(timeblock) = self.timebuf.pop(self.nfft(), self.overlap_keep) {
            // Compute cross-power spectra for current time block
            self.update_singleblock(timeblock.view());

            result.push(self.cur_est.clone());
        }

        result
    }
}

#[cfg(test)]
mod test {
    use approx::assert_abs_diff_eq;
    use ndarray_rand::rand_distr::Normal;
    use ndarray_rand::RandomExt;

    use super::*;
    use crate::config::*;

    use super::{ApsMode, AvPowerSpectra, CPSResult, Overlap, WindowType};
    use Overlap::Percentage;

    #[test]
    fn test_overlap_keep() {
        let ol = [
            Overlap::NoOverlap,
            Percentage(50.),
            Percentage(50.),
            Percentage(25.),
            Overlap::Number(10),
        ];
        let nffts = [10, 10, 1024, 10];
        let expected_keep = [0, 5, 512, 2, 10];

        for ((expected, nfft), overlap) in expected_keep.iter().zip(nffts.iter()).zip(ol.iter()) {
            let settings = ApsSettingsBuilder::default()
                .nfft(*nfft)
                .fs(1.)
                .overlap(overlap.clone())
                .build()
                .unwrap();

            assert_eq!(settings.get_overlap_keep(), *expected);
        }
    }

    /// When the time constant is 1.0, every second the powers approximately
    /// halve. That is the subject of this test.
    #[test]
    fn test_expweighting() {
        let nfft = 48000;
        let fs = nfft as Flt;
        let tau = 2.;
        let settings = ApsSettingsBuilder::default()
            .fs(fs)
            .nfft(nfft)
            .overlap(Overlap::NoOverlap)
            .mode(ApsMode::ExponentialWeighting { tau })
            .build()
            .unwrap();
        let overlap_keep = settings.get_overlap_keep();
        let mut aps = AvPowerSpectra::new(settings);
        assert_eq!(aps.overlap_keep, 0);

        let distr = Normal::new(1.0, 1.0).unwrap();
        let timedata_some = Dmat::random((nfft, 1), distr);
        let timedata_zeros = Dmat::zeros((nfft, 1));

        // Clone here, as first_result reference is overwritten by subsequent
        // calls to compute_last.
        let first_result = aps.compute_last(timedata_some.view()).unwrap().clone();

        aps.compute_last(&timedata_zeros).unwrap();

        let last = aps.compute_last(&timedata_zeros).unwrap();

        let alpha = Flt::exp(-((nfft - overlap_keep) as Flt) / (fs * tau));

        for i in 0..nfft / 2 + 1 {
            assert_abs_diff_eq!(first_result.ap(0)[i] * alpha.powi(2), last.ap(0)[i]);
        }
        assert_eq!(aps.N, 3);
    }

    #[test]
    fn test_tf1() {
        let nfft = 4800;
        let distr = Normal::new(1.0, 1.0).unwrap();
        let mut timedata = Dmat::random((nfft, 1), distr);
        timedata
            .push_column(timedata.column(0).mapv(|a| 2. * a).view())
            .unwrap();

        let settings = ApsSettingsBuilder::default()
            .fs(1.0)
            .nfft(nfft)
            .build()
            .unwrap();
        let mut aps = AvPowerSpectra::new(settings);
        if let Some(v) = aps.compute_last(&timedata) {
            let tf = v.tf(0, 1, None);
            assert_eq!((&tf - 2.0 * Cflt::ONE).sum().abs(), 0.0);
        } else {
            assert!(false);
        }
    }

    #[test]
    fn test_tf2() {
        let nfft = 4800;
        let distr = Normal::new(1.0, 1.0).unwrap();
        let mut timedata = Dmat::random((nfft, 1), distr);
        timedata
            .push_column(timedata.column(0).mapv(|a| 2. * a).view())
            .unwrap();
        // Negative reference channel
        timedata
            .push_column(timedata.column(0).mapv(|a| -1. * a).view())
            .unwrap();

        let settings = ApsSettingsBuilder::default()
            .fs(1.)
            .nfft(nfft)
            .build()
            .unwrap();
        let mut aps = AvPowerSpectra::new(settings);
        if let Some(v) = aps.compute_last(&timedata) {
            let tf = v.tf(0, 1, Some(2));
            assert_eq!((&tf - 2.0 * Cflt::ONE).sum().abs(), 0.0);
        } else {
            assert!(false);
        }
    }
    #[test]
    fn test_ap() {
        let nfft = 1024;
        let distr = Normal::new(1.0, 1.0).unwrap();
        let timedata = Dmat::random((150 * nfft, 1), distr);
        let timedata_mean_square = (&timedata * &timedata).sum() / (timedata.len() as Flt);

        for wt in [
            Some(WindowType::Rect),
            Some(WindowType::Hann),
            Some(WindowType::Bartlett),
            Some(WindowType::Blackman),
            None,
        ] {
            let settings = ApsSettingsBuilder::default()
                .fs(1.0)
                .nfft(nfft)
                .windowType(wt.unwrap_or_default())
                .build()
                .unwrap();
            let mut aps = AvPowerSpectra::new(settings);
            if let Some(v) = aps.compute_last(&timedata) {
                let ap = v.ap(0);
                assert_abs_diff_eq!((&ap).sum().abs(), timedata_mean_square, epsilon = 1e-2);
            } else {
                assert!(false);
            }
        }
    }
    #[test]
    #[should_panic]
    fn test_apssettings1() {
        let _ = ApsSettingsBuilder::default().build().unwrap();
    }

    #[test]
    fn test_apssettings2() {
        let _ = ApsSettingsBuilder::default()
            .nfft(2048)
            .fs(1.0)
            .build()
            .unwrap();
    }
}
