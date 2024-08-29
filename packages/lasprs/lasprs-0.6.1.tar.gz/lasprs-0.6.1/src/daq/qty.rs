//! Physical quantities that are input / output of a daq device. Provides an enumeration for these.
//!

use crate::config::*;
use strum::EnumMessage;
use strum_macros;
use serde::{Serialize, Deserialize};

/// Physical quantities that are I/O of a Daq device.
// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
// #[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(PartialEq, Serialize, Deserialize, strum_macros::EnumMessage, Debug, Clone, Copy)]
#[allow(dead_code)]
pub enum Qty {
    /// Number
    #[strum(message = "number", detailed_message = "Unitless number")]
    Number = 0,
    /// Acoustic pressure
    #[strum(message = "acousticpressure", detailed_message = "Acoustic Pressure [Pa]")]
    AcousticPressure = 1,
    /// Voltage
    #[strum(message = "voltage", detailed_message = "Voltage [V]")]
    Voltage = 2,
    #[strum(message = "userdefined", detailed_message = "User defined [#]")]
    /// User defined
    UserDefined = 3,
}
