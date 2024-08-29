//! Provides stream messages that come from a running stream
use strum_macros::Display;

use super::*;

/// Gives the stream status of a (possible) stream, either input / output or duplex.
#[derive(strum_macros::EnumMessage, Debug, Clone, Copy, Display)]
#[cfg_attr(feature = "python-bindings", pyclass)]
pub enum StreamStatus {
    /// Stream is not running
    #[strum(message = "NotRunning", detailed_message = "Stream is not running")]
    NotRunning{},
    /// Stream is running properly
    #[strum(message = "Running", detailed_message = "Stream is running")]
    Running{},

    /// An error occured in the stream.
    #[strum(message = "Error", detailed_message = "An error occured with the stream")]
    Error{
        /// In case the stream has an error: e is the field name
        e: StreamError
    }
}
