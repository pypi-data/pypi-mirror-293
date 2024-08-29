use strum_macros::Display;
use crate::config::*;

/// Errors that happen in a stream
#[derive(strum_macros::EnumMessage, PartialEq, Debug, Clone, Display, Copy)]

// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
//#[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]

pub enum StreamError {
    /// Input overrun
    #[strum(
        message = "InputOverrun Error",
        detailed_message = "Input buffer overrun"
    )]
    InputOverrunError,

    /// Output underrun
    #[strum(
        message = "OutputUnderrunError",
        detailed_message = "Output buffer underrun"
    )]
    OutputUnderrunError,

    /// Driver specific error
    #[strum(message = "DriverError", detailed_message = "Driver error")]
    DriverError,

    /// Device
    #[strum(detailed_message = "Device not available (anymore)")]
    DeviceNotAvailable,

    /// Logic error (something weird happened)
    #[strum(detailed_message = "Logic error")]
    LogicError,
}