//! # Library for acoustic signal processing
//!
//! This crate contains structures and functions to perform acoustic
//! measurements, interact with data acquisition devices and apply common
//! acoustic analysis operations on them.
//!
//! You will find the following stuff in this crate:
//!
//! - Data acquisition, recording, signal generation: [daq].
//! - Power spectra estimation, transfer function estimation tools: [ps].
//! - Sound Level Meter implementation: [slm].
//! - Filter design tools. I.e. [filter::ZPKModel::butter].
//!   - Includes bilinear transforms
//! - Tools for real time displaying of sensor data: [rt].
//!
//! ## Note to potential users
//!
//! **This crate is still under heavy development. API changes happen on the
//! fly. Documentation is not finished. Use with caution and expect things to be
//! broken and buggy. Use at your own risk and responsibility.**
//!
//! ## Author information
//!
//! The main developer is J.A. de Jong from [ASCEE](https://www.ascee.nl). In
//! case of bug reports, please file them to [info@ascee.nl](info@ascee.nl).
//!
//! If you have particular interest in this library, please also contact us.
//!
#![warn(missing_docs)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]

mod config;
use config::*;

pub use config::Flt;
pub mod daq;
pub mod filter;
pub mod ps;
pub mod siggen;
use filter::*;
pub mod rt;
pub mod slm;

/// A Python module implemented in Rust.
#[cfg(feature = "python-bindings")]
#[pymodule]
#[pyo3(name = "_lasprs")]
fn lasprs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    daq::add_py_classses(m)?;

    // Add filter submodule
    m.add_class::<filter::Biquad>()?;
    m.add_class::<filter::SeriesBiquad>()?;
    m.add_class::<filter::BiquadBank>()?;
    m.add_class::<siggen::Siggen>()?;
    m.add_class::<filter::FilterSpec>()?;
    m.add_class::<filter::ZPKModel>()?;
    m.add_class::<filter::StandardFilterDescriptor>()?;
    m.add_class::<slm::TimeWeighting>()?;
    m.add_class::<ps::FreqWeighting>()?;
    m.add_class::<slm::SLMSettings>()?;
    m.add_class::<slm::SLM>()?;

    Ok(())
}
