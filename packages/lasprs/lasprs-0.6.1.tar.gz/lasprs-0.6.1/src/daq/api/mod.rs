/// Daq apis that are optionally compiled in. Examples:
///
/// - CPAL (Cross-Platform Audio Library)
/// - ...
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use strum::EnumMessage;
use strum_macros;
use crate::config::*;

use super::{StreamStatus, StreamMetaData};

#[cfg(feature = "cpal-api")]
pub mod api_cpal;

#[cfg(feature = "pulse-api")]
pub mod api_pulse;

/// A currently running stream
pub trait Stream {
    /// Stream metadata. Only available for input streams
    fn metadata(&self) -> Arc<StreamMetaData>;

    /// Number of input channels in stream
    fn ninchannels(&self) -> usize;

    /// Number of output channels in stream
    fn noutchannels(&self) -> usize;

    /// Obtain stream status
    fn status(&self) -> StreamStatus;
}

/// Stream API descriptor: type and corresponding text
// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
//#[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(strum_macros::EnumMessage, Debug, Clone, PartialEq, Serialize, Deserialize, strum_macros::Display)]
#[allow(dead_code)]
pub enum StreamApiDescr {
    /// CPAL api
    #[strum(message = "Cpal", detailed_message = "Cross-Platform Audio Library")]
    Cpal = 0,
    /// PulseAudio api
    #[strum(message = "pulse", detailed_message = "Pulseaudio")]
    Pulse = 1,
}