//! Provides stream messages that come from a running stream
use crate::config::*;
use crate::daq::Qty;
use crate::siggen::Siggen;
use anyhow::{bail, Result};
use streamdata::*;
use crossbeam::channel::Sender;
use reinterpret::{reinterpret_slice, reinterpret_vec};
use std::any::TypeId;
use std::sync::{Arc, RwLock};
use std::u128::MAX;
use strum_macros::Display;

use super::*;

/// Input stream messages, to be send to handlers.
#[derive(Clone, Debug)]
pub enum InStreamMsg {
    /// Raw stream data that is coming from a device. This is interleaved data. The number of channels is correct and
    /// specified in the stream metadata.
    InStreamData(Arc<InStreamData>),

    /// An error has occured in the stream
    StreamError(StreamError),

    /// new Stream metadata enters the scene. Probably a new stream started.
    StreamStarted(Arc<StreamMetaData>),

    /// An existing stream stopped.
    StreamStopped,
}

