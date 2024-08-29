use crate::config::*;
use derive_builder::Builder;
use itertools::Itertools;
use ndarray::ArrayView1;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use rayon::prelude::*;
use smallvec::SmallVec;

use super::{settings::SLMSettings, SLM_MAX_CHANNELS};
use crate::{config::*, filter::Filter};
use crate::{Biquad, Dcol, Flt, FreqWeighting, PoleOrZero, SeriesBiquad, ZPKModel};
#[derive(Debug, Clone)]
struct SLMChannel {
    // Statistics to store
    stat: SLMStat,
    // The bandpass filter for this channel
    bp: SeriesBiquad,
    // The rectifier filter
    rect_lowpass_up: Biquad,
    // The rectifier filter for decreasing values. Only for asymmetric time
    // weighting (case of impulse weighting: [TimeWeighting::Impulse])
    rect_lowpass_down: Option<Biquad>,
}

/// Sound Level Meter
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Debug, Clone)]
pub struct SLM {
    // Number of samples processed after last run() is called.
    N: usize,
    Lrefsq: Flt,
    prefilter: SeriesBiquad,
    channels: SmallVec<[SLMChannel; SLM_MAX_CHANNELS]>,
}

impl SLM {
    // Create simple first order lowpass filter with unit D.C. gain and given
    // real pole.
    fn lpfilter_from_pole(fs: Flt, p: PoleOrZero) -> Biquad {
        Biquad::bilinear_zpk(fs, None, Some(p), Some(1.0), None).setGainAt(0., 1.)
    }
    /// Create new Sound Level Meter from given settings
    pub fn new(settings: SLMSettings) -> Self {
        let fs = settings.fs;
        let prefilter = ZPKModel::freqWeightingFilter(settings.freqWeighting).bilinear(fs);
        let channels = settings
            .filterDescriptors
            .iter()
            .map(|descriptor| {
                // Generate bandpass filter
                let bp = descriptor.genFilter().bilinear(fs);
                // Initalize statistics with defaults
                let stat = SLMStat::default();

                // Generate rectifier filter for upwards
                let poles = settings.timeWeighting.getLowpassPoles();

                let rect_lowpass_up = Self::lpfilter_from_pole(fs, PoleOrZero::Real1(poles.0));

                let rect_lowpass_down = if let Some(p) = poles.1 {
                    Some(Self::lpfilter_from_pole(fs, PoleOrZero::Real1(p)))
                } else {
                    None
                };
                SLMChannel {
                    stat,
                    bp,
                    rect_lowpass_up,
                    rect_lowpass_down,
                }
            })
            .collect();
        SLM {
            prefilter,
            channels,
            Lrefsq: settings.Lref.powi(2),
            N: 0,
        }
    }
    /// Push new time data through sound level meter. Returns L(t) data for each
    /// channel. Updates the computed statistics and optionally outputs levels
    /// vs time if flag `provide_output` is set to `true`. Note that at the end
    /// of the block, the `L(t)` can also be obtained by calling [SLM::Ltlast].
    ///
    /// # Args
    ///
    /// - `td`: Time data
    /// - `provide_output` - Set this to true to give intermediate output data
    pub fn run(&mut self, td: &[Flt], provide_output: bool) -> Option<Vec<Vec<Flt>>> {
        if td.len() == 0 {
            return None;
        }
        let prefiltered = self.prefilter.filter(td);

        let level = |a| 10. * Flt::log10(a) / self.Lrefsq;

        let Lt_iter = self.channels.par_iter_mut().map(|ch| {
            let mut tmp = ch.bp.filter(&prefiltered);
            let mut N = self.N;

            // Filtered squared
            let mut filtered_squared = {
                let mut tmp_view = ArrayViewMut1::from(&mut tmp);
                tmp_view.mapv_inplace(|a| a * a);
                tmp_view
            };

            // Update Lpk, Leq
            filtered_squared.for_each(|sample_pwr| {
                let new_pk = sample_pwr.abs();
                if new_pk > ch.stat.Ppk {
                    ch.stat.Ppk = new_pk;
                }
                // Update equivalent level
                ch.stat.Peq = (ch.stat.Peq * N as Flt + sample_pwr) / (N as Flt + 1.);
                N += 1;
            });

            // Run filtered_squared signal throug rectifier
            if let Some(rectifier_down) = &mut ch.rect_lowpass_down {
                filtered_squared.mapv_inplace(|sample_sq| {
                    let rectifier_up = &mut ch.rect_lowpass_up;

                    // Asymmetric up/down case for level
                    let mut fup = sample_sq;
                    let mut fdown = sample_sq;

                    // Filter in up-filter
                    rectifier_up.filter_inout_single(&mut fup);
                    // Filter in down-filter
                    rectifier_down.filter_inout_single(&mut fdown);

                    // Check who wins
                    if fup >= fdown {
                        rectifier_down.setToDCValue(fup);
                        fup
                    } else {
                        rectifier_up.setToDCValue(fup);
                        fdown
                    }
                });
            } else {
                // Filter in place
                let rectifier = &mut ch.rect_lowpass_up;
                rectifier.filter_inout(filtered_squared.as_slice_mut().unwrap());
            }

            // Update max signal power gotten so far
            let rectified = &mut filtered_squared;
            rectified.for_each(|val| {
                if *val > ch.stat.Pmax {
                    ch.stat.Pmax = *val;
                }
            });
            // Update last signal power coming from SLM
            ch.stat.Pt_last = *filtered_squared.last().unwrap();
            // Convert output to levels
            filtered_squared.mapv_inplace(level);
            tmp
        });
        if provide_output {
            let Lt: Vec<_> = Lt_iter.collect();
            self.N += td.len();
            Some(Lt)
        } else {
            // Just consume the iterator
            Lt_iter.for_each(|_| {});
            self.N += td.len();
            None
        }
    }

    /// Number of channels in SLM
    pub fn nch(&self) -> usize {
        self.channels.len()
    }

    fn levels_from<T>(&self, stat_returner: T) -> Dcol
    where
        T: Fn(&SLMChannel) -> Flt,
    {
        Dcol::from_iter(
            self.channels
                .iter()
                .map(|ch| 10. * Flt::log10(stat_returner(ch) / self.Lrefsq)),
        )
    }

    /// Get max levels for each channel
    pub fn Lmax(&self) -> Dcol {
        self.levels_from(|ch| ch.stat.Pmax)
    }
    /// Get peak levels for each channel
    pub fn Lpk(&self) -> Dcol {
        self.levels_from(|ch| ch.stat.Ppk)
    }

    /// Get equivalent levels for each channel
    pub fn Leq(&self) -> Dcol {
        self.levels_from(|ch| ch.stat.Peq)
    }
    /// Get last value of level vs time
    pub fn Ltlast(&self) -> Dcol {
        self.levels_from(|ch| ch.stat.Pt_last)
    }
}

#[cfg(feature="python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl SLM {
    #[new]
    fn new_py(settings: SLMSettings) -> SLM {
        SLM::new(settings)
    }

    #[pyo3(name = "run", signature=(dat, provide_output=true))]
    fn run_py(&mut self, dat: PyArrayLike1<Flt>, provide_output: bool) -> Option<Vec<Vec<Flt>>> {
        self.run(dat.as_array().as_slice()?, provide_output)
    }

    #[pyo3(name = "Lmax")]
    fn Lmax_py<'py>(&self, py: Python<'py>) -> PyArr1Flt<'py> {
        PyArray1::from_array_bound(py, &self.Lmax())
    }
    #[pyo3(name = "Leq")]
    fn Leq_py<'py>(&self, py: Python<'py>) -> PyArr1Flt<'py> {
        PyArray1::from_array_bound(py, &self.Leq())
    }
    #[pyo3(name = "Lpk")]
    fn Lpk_py<'py>(&self, py: Python<'py>) -> PyArr1Flt<'py> {
        PyArray1::from_array_bound(py, &self.Lpk())
    }
    #[pyo3(name = "Ltlast")]
    fn Ltlast_py<'py>(&self, py: Python<'py>) -> PyArr1Flt<'py> {
        PyArray1::from_array_bound(py, &self.Ltlast())
    }
}

#[derive(Debug, Clone, Default)]
/// Quantities defined as powers, i.e. square of amplitude
struct SLMStat {
    // Max signal power
    Pmax: Flt,
    // Peak signal power
    Ppk: Flt,
    // Equivalent signal power
    Peq: Flt,

    // Last obtained signal power, after last time run() is called.
    Pt_last: Flt,
}

#[cfg(test)]
mod test {
    use crate::{
        siggen::Siggen,
        slm::{SLMSettingsBuilder, TimeWeighting},
        Flt, FreqWeighting, StandardFilterDescriptor,
    };

    use super::SLM;

    #[test]
    fn test_slm1() {
        const fs: Flt = 48e3;
        const N: usize = (fs / 8.) as usize;

        let desc = StandardFilterDescriptor::Overall().unwrap();

        let settings = SLMSettingsBuilder::default()
            .fs(fs)
            .timeWeighting(TimeWeighting::Fast {})
            .freqWeighting(FreqWeighting::Z)
            .filterDescriptors(&[desc])
            .build()
            .unwrap();

        let mut siggen = Siggen::newSine(1, 1000.);
        siggen.setAllMute(false);
        siggen.reset(fs);
        let mut data = vec![0.; N];
        siggen.genSignal(&mut data);

        let mut slm = SLM::new(settings);
        // println!("{slm:#?}");
        let res = slm.run(&data, true).unwrap();
        let res = &res[0];
        println!("{slm:#?}");
        println!("{:#?}", &res[res.len() - 100..]);
    }
}
