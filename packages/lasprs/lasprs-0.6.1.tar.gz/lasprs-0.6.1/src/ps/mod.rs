//!
//! Provides code to estimate (cross)[PowerSpectra], averaged power spectra
//! [AvPowerSpectra] using
//! Welch' method, and windows for time-windowing the data with non-rectangular
//! windows (also known as 'tapers').
//!
mod aps;
mod fft;
mod ps;
mod timebuffer;
mod window;
mod freqweighting;
use crate::config::*;


pub use freqweighting::FreqWeighting;
pub use aps::{ApsSettings, ApsSettingsBuilder,ApsMode, AvPowerSpectra, Overlap};
pub use ps::{CrossPowerSpecra, PowerSpectra, CPSResult};
pub use window::{Window, WindowType};
