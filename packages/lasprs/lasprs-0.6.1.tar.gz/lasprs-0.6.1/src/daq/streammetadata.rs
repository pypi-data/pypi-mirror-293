use super::*;
use crate::config::Flt;
use anyhow::Result;
/// Stream metadata. All information required for properly interpreting the raw
/// data that is coming from the stream.
#[derive(Clone, Debug)]
pub struct StreamMetaData {
    /// Information for each channel in the stream
    pub channelInfo: Vec<DaqChannel>,

    /// The data type of the device [Number / voltage / Acoustic pressure / ...]
    pub rawDatatype: DataType,

    /// Sample rate in \[Hz\]
    pub samplerate: Flt,

    /// The number of frames per block of data that comes in. Multiplied by
    /// channelInfo.len() we get the total number of samples that come in at
    /// each callback.
    pub framesPerBlock: usize,
}

impl StreamMetaData {
    /// Create new metadata object.
    ///     ///
    /// # Args
    ///
    pub fn new<'a, T>(
        channelInfo: T,
        rawdtype: DataType,
        sr: Flt,
        framesPerBlock: usize,
    ) -> StreamMetaData
    where
        T: IntoIterator<Item = &'a DaqChannel>,
    {
        let channelInfo = channelInfo
            .into_iter()
            .inspect(|ch| {
                assert!(
                    ch.enabled,
                    "Only enabled channels should be given as input to StreamMetaData"
                );
            })
            .cloned()
            .collect();
        StreamMetaData {
            channelInfo,
            rawDatatype: rawdtype,
            samplerate: sr,
            framesPerBlock,
        }
    }

    /// Returns the number of channels in the stream metadata.
    #[inline]
    pub fn nchannels(&self) -> usize {
        self.channelInfo.len()
    }
}
