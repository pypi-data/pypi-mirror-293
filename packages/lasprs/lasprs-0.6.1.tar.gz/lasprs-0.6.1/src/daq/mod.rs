//! Data acquisition code. Provides abstract layers around DAQ devices, creating
//! input and output streams and interact with them (record, create signal
//! generators, filter data, show real time sound levels and so on).
//! 
//! - Record data in a `Recording`
//! - Interact with DAQ devices:
//!   - Set number of channels, channel names etc.
//!   - Enable / disable IEPE
//!   - Set datatypes etc.
//! 
//! Most of the things are done using a [StreamMgr], which is an object to I/O
//! DAQ data, interact with devices etc.

mod api;
mod daqconfig;
mod datatype;
mod deviceinfo;
mod qty;

#[cfg(feature = "record")]
mod record;
#[cfg(feature = "record")]
pub use record::*;

mod streamcmd;
mod streamdata;
mod streamhandler;
mod streammgr;
mod streammsg;
mod streamstatus;
mod streammetadata;
mod streamerror;

// Module re-exports
pub use daqconfig::{DaqChannel, DaqConfig};
pub use datatype::DataType;
pub use deviceinfo::DeviceInfo;
pub use qty::Qty;
pub use streamhandler::StreamHandler;
pub use streammgr::*;
pub use streammsg::InStreamMsg;
pub use streamstatus::StreamStatus;
pub use streamdata::{RawStreamData, InStreamData};
pub use streammetadata::StreamMetaData;
pub use streamerror::StreamError;
use api::*;

#[cfg(feature = "record")]

use crate::config::*;
/// Stream types that can be started
///
// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
// #[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(PartialEq, Clone, Copy)]
pub enum StreamType {
    /// Input-only stream
    Input,
    /// Output-only stream
    Output,
    /// Input and output at the same time
    Duplex,
}

#[cfg(feature = "python-bindings")]
/// Add Python classes from stream manager
pub fn add_py_classses(m: &Bound<'_, PyModule>) -> PyResult<()> {

    m.add_class::<DeviceInfo>()?;
    m.add_class::<StreamMgr>()?;
    m.add_class::<StreamApiDescr>()?;
    m.add_class::<DataType>()?;
    m.add_class::<Qty>()?;
    m.add_class::<StreamType>()?;
    m.add_class::<StreamStatus>()?;
    m.add_class::<StreamError>()?;
    m.add_class::<DaqChannel>()?;
    m.add_class::<DaqConfig>()?;

    Ok(())
}
