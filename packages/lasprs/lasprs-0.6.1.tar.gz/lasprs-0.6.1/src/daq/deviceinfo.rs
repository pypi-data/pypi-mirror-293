#![allow(non_snake_case)]

use super::StreamApiDescr;
use super::*;
use crate::config::*;

/// Device info structure. Gives all information regarding a device, i.e. the number of input and
/// output channels, its name and available sample rates and types.
#[derive(Clone, Debug)]
#[allow(dead_code)]
#[cfg_attr(feature = "python-bindings", pyclass(get_all))]

pub struct DeviceInfo {
    /// The api in use for this device
    pub api: StreamApiDescr,

    /// Name for the device.
    pub device_name: String,

    /// Available data types for the sample
    // #[pyo3(get)]
    pub avDataTypes: Vec<DataType>,

    /// Preferred data type for device
    // #[pyo3(get)]
    pub prefDataType: DataType,

    /// Available frames per block
    pub avFramesPerBlock: Vec<usize>,

    /// Preferred frames per block for device
    pub prefFramesPerBlock: usize,

    /// Available sample rates
    pub avSampleRates: Vec<Flt>,

    /// Preferred sample rate for device
    pub prefSampleRate: Flt,

    /// Number of input channels available for this device
    pub iChannelCount: u8,

    /// Number of output channels available for this device
    pub oChannelCount: u8,

    /// Whether the device is capable to provide IEPE constant current power supply.
    pub hasInputIEPE: bool,

    /// Whether the device is capable of enabling a hardware AC-coupling
    pub hasInputACCouplingSwitch: bool,

    ///Whether the device is able to trigger on input
    pub hasInputTrigger: bool,

    /// Whether the device has an internal monitor of the output signal. If
    /// true, the device is able to monitor output signals internally and able to
    /// present output signals as virtual input signals. This only works together
    /// Daq's that are able to run in full duplex mode.
    pub hasInternalOutputMonitor: bool,

    /// This flag is used to be able to indicate that the device cannot run
    /// input and output streams independently, without opening the device in
    /// duplex mode. This is for example true for the UlDaq: only one handle to
    /// the device can be given at the same time.
    pub duplexModeForced: bool,

    /// The physical quantity of the output signal. For 'normal' audio
    /// devices, this is typically a 'number' between +/- full scale. For some
    /// devices however, the output quantity corresponds to a physical signal,
    /// such a Volts.
    // #[pyo3(get)]
    pub physicalIOQty: Qty,
}
#[cfg_attr(feature = "python-bindings", pymethods)]
impl DeviceInfo {
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}
