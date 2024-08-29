//! Data types (sample formats) that can come from a DAQ device, or have to be sent as output to a
//! DAQ device.
use strum::EnumMessage;
use strum_macros;
use serde::{Serialize, Deserialize};
use crate::config::*;

/// Data type description for samples coming from a stream
#[derive(strum_macros::EnumMessage, PartialEq, Copy, Debug, Clone, Serialize, Deserialize)]
// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
//#[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]
#[allow(dead_code)]
pub enum DataType {
    /// 32-bit floats
    #[strum(message = "F32", detailed_message = "32-bits floating points")]
    F32 = 0,
    /// 64-bit floats
    #[strum(message = "F64", detailed_message = "64-bits floating points")]
    F64 = 1,
    /// 8-bit integers
    #[strum(message = "I8", detailed_message = "8-bits integers")]
    I8 = 2,
    /// 16-bit integers
    #[strum(message = "I16", detailed_message = "16-bits integers")]
    I16 = 3,
    /// 32-bit integers
    #[strum(message = "I32", detailed_message = "32-bits integers")]
    I32 = 4,
}
