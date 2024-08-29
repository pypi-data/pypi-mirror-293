//! Sound Level Meter (SLM) module.
//!
//! Provides structs and helpers (SLMBuilder) for creating configurated Sound
//! Level Meters.
//! 
//! # Usage examples
//! 
//! ## Simple over-all level SLM
//! 
//! This example creates a simple SLM that processes at 48kHz, uses fast time
//! weighting and A frequency weighting:
//! 
//! ```
//! # use anyhow::Result;
//! use lasprs::slm::*;
//! use lasprs::filter::StandardFilterDescriptor;
//! use ndarray::Array1;
//! # fn main() -> Result<()> {
//! 
//! // Generate an overall filter (no filter at all)
//! let desc = StandardFilterDescriptor::Overall().unwrap();
//! 
//! // Generate settings
//! let settings = SLMSettingsBuilder::default()
//!     .fs(48e3)
//!     .freqWeighting(FreqWeighting::A)
//!     .timeWeighting(TimeWeighting::Fast{})
//!     .filterDescriptors(&[desc]).build().unwrap();
//! 
//! let mut slm = SLM::new(settings);
//! // Generate some data. Yes, this is not the most spectacular set
//! let mut data = Array1::zeros(48000);
//! data[0] = 1.;
//! 
//! // Now apply some data. This is a kind of the SLM-s impulse response
//! let res = slm.run(data.as_slice().unwrap(), true).unwrap();
//! 
//! // Only one channel of result data
//! assert_eq!(res.len(), 1);
//! 
//! let res = &res[0];
//! println!("Data is: {res:#?}");
//! 
//! // Get the equivalent level:
//! let Leq = slm.Leq()[0];
//! 
//! # Ok::<() , anyhow::Error>(())
//! # }
//! ```
//! 
//! ## One-third octave band, plus overall
//! 
//! ```
//! use lasprs::filter::StandardFilterDescriptor;
//! // Generate the default set of one-third octave band filters
//! let mut desc = StandardFilterDescriptor::fullThirdOctaveFilterSet();
//! desc.push(StandardFilterDescriptor::Overall().unwrap());
//! 
//! // Rest of code is the same as in previous example
//! 
//! ```
//! 
mod settings;
mod tw;
mod slm;
pub use slm::SLM;
pub use settings::{SLMSettings, SLMSettingsBuilder};
pub use tw::TimeWeighting;
pub use crate::ps::FreqWeighting;

const SLM_MAX_CHANNELS: usize = 64;