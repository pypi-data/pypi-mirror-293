//! This module provide signal generators. The import struct defined here is
//! [Siggen], which has several creation methods.
//!
//! # Examples
//!
//! ## Create some white noise and print it.
//!
//! ```
//! use lasprs::siggen::Siggen;
//! let mut wn = Siggen::newWhiteNoise(1);
//! // Set gains for all channels
//! wn.setAllGains(0.1);
//! // Unmute all channels
//! wn.setAllMute(false);
//! // Create a slice where data is stored.
//! let mut sig = [0. ; 1024];
//! // Fill `sig` with the signal data.
//! wn.genSignal(&mut sig);
//! // Print data.
//! println!("{:?}", &sig);
//!
//! ```
use super::config::*;
use super::filter::Filter;
use dasp_sample::{FromSample, Sample};
use rayon::prelude::*;
use std::fmt::Debug;
use std::iter::ExactSizeIterator;
use std::slice::IterMut;

use rand::prelude::*;
use rand::rngs::ThreadRng;
use rand_distr::StandardNormal;

/// Ratio between circumference and radius of a circle
const twopi: Flt = 2.0 * pi;

/// Source for the signal generator. Implementations are sine waves, sweeps, noise.
pub trait Source: Send {
    /// Generate the 'pure' source signal. Output is placed inside the `sig` argument.
    fn genSignal_unscaled(&mut self, sig: &mut dyn ExactSizeIterator<Item = &mut Flt>);
    /// Reset the source state, i.e. set phase to 0, etc
    fn reset(&mut self, fs: Flt);
    /// Used to make the Siggen struct cloneable
    fn clone_dyn(&self) -> Box<dyn Source>;
}
impl Clone for Box<dyn Source> {
    fn clone(&self) -> Self {
        self.clone_dyn()
    }
}

#[derive(Clone)]
struct Silence {}

impl Source for Silence {
    fn genSignal_unscaled(&mut self, sig: &mut dyn ExactSizeIterator<Item = &mut Flt>) {
        sig.for_each(|s| {
            *s = 0.0;
        });
    }
    fn reset(&mut self, _fs: Flt) {}
    fn clone_dyn(&self) -> Box<dyn Source> {
        Box::new(self.clone())
    }
}

/// White noise source
#[derive(Clone)]
struct WhiteNoise {}
impl WhiteNoise {
    /// Generate new WhiteNoise generator
    fn new() -> WhiteNoise {
        WhiteNoise {}
    }
}
impl Source for WhiteNoise {
    fn genSignal_unscaled(&mut self, sig: &mut dyn ExactSizeIterator<Item = &mut Flt>) {
        sig.for_each(|s| {
            *s = thread_rng().sample(StandardNormal);
        });
    }
    fn reset(&mut self, _fs: Flt) {}
    fn clone_dyn(&self) -> Box<dyn Source> {
        Box::new(self.clone())
    }
}

/// Sine wave, with configurable frequency
#[derive(Clone)]
struct Sine {
    // Sampling freq [Hz]
    fs: Flt,
    // current stored phase
    phase: Flt,
    // Signal frequency [rad/s]
    omg: Flt,
}
impl Sine {
    /// Create new sine source signal
    ///
    /// Args:
    ///
    /// * fs: Sampling freq [Hz]
    /// *
    fn new(freq: Flt) -> Sine {
        Sine {
            fs: -1.0,
            phase: 0.0,
            omg: 2.0 * pi * freq,
        }
    }
}
impl Source for Sine {
    fn genSignal_unscaled(&mut self, sig: &mut dyn ExactSizeIterator<Item = &mut Flt>) {
        if self.fs <= 0.0 {
            sig.for_each(|s| {
                *s = 0.0;
            });
            return;
        }
        sig.for_each(|s| {
            *s = Flt::sin(self.phase);
            self.phase += self.omg / self.fs;
            self.phase %= twopi;
        });
    }
    fn reset(&mut self, fs: Flt) {
        self.fs = fs;
        self.phase = 0.0;
    }
    fn clone_dyn(&self) -> Box<dyn Source> {
        Box::new(self.clone())
    }
}

/// Signal generator. Able to create acoustic output signals. See above example on how to use.
/// Typical signal that can be created are:
///
/// * (Siggen::newWhiteNoise)
/// * (Siggen::newSine)
///
#[derive(Clone)]
#[cfg_attr(feature = "python-bindings", pyclass)]
pub struct Siggen {
    // The source dynamic signal. Noise, a sine wave, sweep, etc
    source: Box<dyn Source>,
    // Filter applied to the source signal
    channels: Vec<SiggenChannelConfig>,

    // Temporary source signal buffer
    source_buf: Vec<Flt>,

    // Output buffers (for filtered source signal)
    chout_buf: Vec<Vec<Flt>>,
}
#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl Siggen {
    #[pyo3(name = "newWhiteNoise")]
    #[staticmethod]
    fn newWhiteNoise_py() -> Siggen {
        Siggen::newWhiteNoise(0)
    }
    #[pyo3(name = "newSine")]
    #[staticmethod]
    fn newSine_py(freq: Flt) -> Siggen {
        Siggen::newSine(0, freq)
    }
}

/// Multiple channel signal generator. Can use a single source (coherent) to provide multiple signals
/// that can be sent out through different EQ's
impl Siggen {
    /// Returns the number of channels this signal generator is generating for.
    pub fn nchannels(&self) -> usize {
        self.channels.len()
    }

    /// Silence: create a signal generator that does not output any dynamic
    /// signal at all.
    pub fn newSilence(nchannels: usize) -> Siggen {
        Siggen {
            channels: vec![SiggenChannelConfig::new(); nchannels],
            source: Box::new(Silence {}),
            source_buf: vec![],
            chout_buf: vec![],
        }
    }

    /// Create a white noise signal generator.
    pub fn newWhiteNoise(nchannels: usize) -> Siggen {
        Siggen::new(nchannels, Box::new(WhiteNoise::new()))
    }

    /// Set gains of all channels in signal generator to the same value
    ///
    /// # Args
    ///
    /// * g: New gain value
    pub fn setAllGains(&mut self, g: Flt) {
        self.channels.iter_mut().for_each(|set| set.setGain(g))
    }

    /// Set the number of channels to generate a signal for. Truncates the
    /// output in case the value before calling this method is too little.
    /// Appends new channel configs in case to little is available.
    ///
    /// * nch: The new required number of channels
    pub fn setNChannels(&mut self, nch: usize) {
        self.channels.truncate(nch);

        while self.channels.len() < nch {
            self.channels.push(SiggenChannelConfig::new());
        }
    }

    /// Set the DC offset for all channels
    pub fn setDCOffset(&mut self, dc: &[Flt]) {
        self.channels.iter_mut().zip(dc).for_each(|(ch, dc)| {
            ch.DCOffset = *dc;
        });
    }

    /// Create a sine wave signal generator
    ///
    /// * freq: Frequency of the sine wave in \[Hz\]
    pub fn newSine(nchannels: usize, freq: Flt) -> Siggen {
        Siggen::new(nchannels, Box::new(Sine::new(freq)))
    }

    /// Create a new signal generator wiht an arbitrary source.
    pub fn new(nchannels: usize, source: Box<dyn Source>) -> Siggen {
        Siggen {
            source,
            channels: vec![SiggenChannelConfig::new(); nchannels],
            source_buf: vec![],
            chout_buf: vec![],
        }
    }

    /// Creates *interleaved* output signal
    pub fn genSignal<T>(&mut self, out: &mut [T])
    where
        T: Sample + FromSample<Flt> + Debug,
        Flt: Sample,
    {
        let nch = self.nchannels();
        let nsamples: usize = out.len() / nch;
        assert!(out.len() % self.nchannels() == 0);

        // Create source signal
        self.source_buf.resize(nsamples, 0.0);
        self.source
            .genSignal_unscaled(&mut self.source_buf.iter_mut());
        // println!("Source signal: {:?}", self.source_buf);

        // Write output while casted to the correct type
        // Iterate over each channel, and counter
        self.chout_buf.resize(nch, vec![]);

        for (channelno, (channel, chout)) in self
            .channels
            .iter_mut()
            .zip(self.chout_buf.iter_mut())
            .enumerate()
        {
            chout.resize(nsamples, 0.0);

            // Create output signal, overwrite chout
            channel.genSignal(&self.source_buf, chout);
            // println!("Channel: {}, {:?}", channelno, chout);

            let out_iterator = out.iter_mut().skip(channelno).step_by(nch);
            out_iterator.zip(chout).for_each(|(out, chin)| {
                *out = chin.to_sample();
            });
        }
        // println!("{:?}", out);
    }

    /// Reset signal generator. Applies any kind of cleanup necessary.
    ///
    /// Args
    ///
    /// * fs: (New) Sampling frequency \[Hz\]
    ///
    pub fn reset(&mut self, fs: Flt) {
        self.source.reset(fs);
        self.channels.iter_mut().for_each(|x| x.reset(fs))
    }
    /// Mute / unmute all channels at once
    pub fn setAllMute(&mut self, mute: bool) {
        self.channels.iter_mut().for_each(|s| {
            s.setMute(mute);
        });
    }

    /// Mute / unmute individual channels. Array of bools should have same size
    /// as number of channels in signal generator.
    pub fn setMute(&mut self, mute: &[bool]) {
        assert!(mute.len() == self.nchannels());
        self.channels.iter_mut().zip(mute).for_each(|(s, m)| {
            s.setMute(*m);
        });
    }
}

/// Signal generator config for a certain channel
#[derive(Clone)]
struct SiggenChannelConfig {
    muted: bool,
    prefilter: Option<Box<dyn Filter>>,
    gain: Flt,
    DCOffset: Flt,
}
unsafe impl Send for SiggenChannelConfig {}
impl SiggenChannelConfig {
    /// Set new pre-filter that filters the source signal
    pub fn setPreFilter(&mut self, pref: Option<Box<dyn Filter>>) {
        self.prefilter = pref;
    }
    /// Set the gain applied to the source signal
    ///
    /// * g: Gain value. Can be any float. If set to 0.0, the source is effectively muted. Only
    /// using (setMute) is a more efficient way to do this.
    pub fn setGain(&mut self, g: Flt) {
        self.gain = g;
    }

    /// Reset signal channel config. Only resets the prefilter state
    pub fn reset(&mut self, _fs: Flt) {
        if let Some(f) = &mut self.prefilter {
            f.reset()
        }
    }
    /// Generate new channel configuration using 'arbitrary' initial config: muted false, gain 1.0, DC offset 0.
    /// and no prefilter
    pub fn new() -> SiggenChannelConfig {
        SiggenChannelConfig {
            muted: false,
            prefilter: None,
            gain: 1.0,
            DCOffset: 0.0,
        }
    }

    /// Set mute on channel. If true, only DC signal offset is outputed from (SiggenChannelConfig::transform).
    pub fn setMute(&mut self, mute: bool) {
        self.muted = mute;
    }
    /// Generate new signal data, given input source data.
    ///
    /// # Args
    ///
    /// source: Input source signal.
    /// result: Reference of array of float values to be filled with signal data.
    ///
    /// # Details
    ///
    /// - When muted, the DC offset is still applied
    /// - The order of the generation is:
    ///     - If a prefilter is installed, this pre-filter is applied to the source signal.
    ///     - Gain is applied.
    ///     - Offset is applied (thus, no gain is applied to the DC offset).
    ///
    pub fn genSignal(&mut self, source: &[Flt], result: &mut [Flt]) {
        if self.muted {
            result.iter_mut().for_each(|x| {
                *x = 0.0;
            });
        } else {
            result.copy_from_slice(source);
            if let Some(f) = &mut self.prefilter {
                f.filter(result);
            }
        }
        result.iter_mut().for_each(|x| {
            // First apply gain, then offset
            *x *= self.gain;
            *x += self.DCOffset;
        });
    }
}

#[cfg(test)]
mod test {
    use approx::assert_abs_diff_eq;

    use super::*;
    use crate::Flt;

    #[test]
    fn test_whitenoise() {
        // This code is just to check syntax. We should really be listening to these outputs.
        let mut t = [0.0; 10];
        Siggen::newWhiteNoise(1).genSignal(&mut t);
        // println!("{:?}", &t);
    }

    #[test]
    fn test_sine() {
        // This code is just to check syntax. We should really be listening to
        // these outputs.
        const N: usize = 10000;
        let mut s1 = [0.0; N];
        let mut s2 = [0.0; N];
        let mut siggen = Siggen::newSine(1, 1.0);

        siggen.reset(10.0);
        siggen.setAllMute(false);
        siggen.genSignal(&mut s1);
        siggen.reset(10.0);
        siggen.genSignal(&mut s2);

        let absdiff = s1
            .iter()
            .zip(s2.iter())
            .map(|(s1, s2)| Flt::abs(*s1 - *s2))
            .sum::<Flt>();
        assert_abs_diff_eq!(absdiff, 0., epsilon = Flt::EPSILON * 100.);
    }

    #[test]
    fn test_sine2() {
        // Test if channels are properly separated etc. Check if RMS is correct
        // for amplitude = 1.0.
        const fs: Flt = 10.0;
        // Number of samples per channel
        const Nframes: usize = 10000;
        const Nch: usize = 2;
        let mut signal = [0.0; Nch * Nframes];
        let mut siggen = Siggen::newSine(Nch, 1.0);

        siggen.reset(fs);
        siggen.setMute(&[false, true]);
        // siggen.channels[0].DCOffset = 0.1;

        // Split off in two terms, see if this works properly
        siggen.genSignal(&mut signal[..Nframes / 2]);
        siggen.genSignal(&mut signal[Nframes / 2..]);

        // Mean square of the signal
        let ms1 = signal.iter().step_by(2).map(|s1| *s1 * *s1).sum::<Flt>() / (Nframes as Flt);
        println!("ms1: {}", ms1);

        let ms2 = signal
            .iter()
            .skip(1)
            .step_by(2)
            .map(|s1| *s1 * *s1)
            .sum::<Flt>()
            / (Nframes as Flt);

        assert_abs_diff_eq!(Flt::abs(ms1 - 0.5) , 0., epsilon= Flt::EPSILON * 1e3);
        assert_eq!(ms2, 0.0);
    }

    // A small test to learn a bit about sample types and conversion. This
    // is the thing we want.
    #[test]
    fn test_sample() {
        assert_eq!((0.5f32).to_sample::<i8>(), 64);
        assert_eq!((1.0f32).to_sample::<i8>(), 127);
        assert_eq!(-(1.0f32).to_sample::<i8>(), -127);
        assert_eq!((1.0f32).to_sample::<i16>(), i16::MAX);
    }
}
