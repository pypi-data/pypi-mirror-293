//! Contains filter implemententations for [Biquad]s, series of
//! biquads ([SeriesBiquad]) and banks of series of biquads ([BiquadBank]).
//!
//! Contains [Biquad], [SeriesBiquad], and [BiquadBank]. These are all constructs that work on
//! blocks of input data, and apply filters on it. TODO: implement FIR filter.
#![allow(non_snake_case)]
use super::config::*;

mod biquad;
mod biquadbank;
mod dummy;
mod seriesbiquad;
mod zpkmodel;
mod butter;
mod octave;

pub use super::ps::FreqWeighting;
pub use biquad::Biquad;
pub use biquadbank::BiquadBank;
pub use octave::{StandardFilterDescriptor, G, FREQ_REF};
pub use dummy::DummyFilter;
pub use seriesbiquad::SeriesBiquad;
pub use zpkmodel::{PoleOrZero, ZPKModel, FilterSpec};

/// Implementations of this trait are able to DSP-filter input data.
pub trait Filter: Send {
    //! The filter trait is implemented by, for example, [Biquad], [SeriesBiquad], and [BiquadBank].

    /// Filter input to generate output. A vector of output floats is generated with the same
    /// length as input.
    fn filter(&mut self, input: &[Flt]) -> Vd;
    /// Reset the filter state(s). In essence, this makes sure that all memory of the past is
    /// forgotten.
    fn reset(&mut self);

    /// Required method for cloning a BiquadBank, such that arbitrary filter types can be used as
    /// their 'channels'.
    fn clone_dyn(&self) -> Box<dyn Filter>;
}

/// Implementations are able to generate transfer functions of itself

pub trait TransferFunction<'a, T>: Send
where
    T: AsArray<'a, Flt>,
{
    /// Compute frequency response (i.e. transfer function from input to output)
    ///
    /// # Args
    ///
    /// * `freq` - The frequency in \[Hz\]
    ///
    /// # Returns
    ///
    /// The transfer function: A column vector with the frequency response for
    /// each frequency in `freq`.
    ///
    fn tf(&self, fs: Flt, freq: T) -> Ccol;
}

impl Clone for Box<dyn Filter> {
    fn clone(&self) -> Self {
        self.clone_dyn()
    }
}
