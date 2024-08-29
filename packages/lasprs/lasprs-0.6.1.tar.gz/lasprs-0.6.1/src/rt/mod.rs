//! Real time signal analysis blocks, used for visual inspection and showing
//! data 'on the fly'. Examples are real time power spectra plotting
//! (Spectrograms, Auto powers, ..., or )
mod rtaps;
pub use  rtaps::{RtAps, RtApsResult};