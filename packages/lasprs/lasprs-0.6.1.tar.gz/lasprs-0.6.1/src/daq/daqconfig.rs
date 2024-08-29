use std::{ops::Index, path::PathBuf};

use super::*;
use crate::config::*;
use anyhow::Result;
use serde::{Deserialize, Serialize};

/// DAQ Configuration for a single channel
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
#[cfg_attr(feature = "python-bindings", pyclass(get_all, set_all))]
pub struct DaqChannel {
    /// Whether the channel is enabled
    pub enabled: bool,
    /// Readable name for channel
    pub name: String,
    /// To convert to physical units. Divide values by this to obtain it.
    pub sensitivity: Flt,
    /// Enabled constant current power supply for sensor (if device supports it)
    pub IEPEEnabled: bool,
    /// Enabled hardware AC coupling (if)
    pub ACCouplingMode: bool,
    /// If supporting multiple input ranges: select the right index
    pub rangeIndex: usize,
    /// Physical quantity
    pub qty: Qty,
}
impl Default for DaqChannel {
    fn default() -> Self {
        DaqChannel {
            enabled: false,
            name: "".into(),
            sensitivity: -1.0,
            IEPEEnabled: false,
            ACCouplingMode: false,
            rangeIndex: 0,
            qty: Qty::Number,
        }
    }
}
impl DaqChannel {
    /// Default channel configuration for audio input from a certain channel
    pub fn defaultAudio(name: String) -> Self {
        DaqChannel {
            enabled: true,
            name,
            sensitivity: 1.0,
            IEPEEnabled: false,
            ACCouplingMode: false,
            rangeIndex: 0,
            qty: Qty::Number,
        }
    }
}

/// Configuration of a device.
#[derive(PartialEq, Clone, Debug, Serialize, Deserialize)]
#[cfg_attr(feature = "python-bindings", pyclass(get_all, set_all))]
pub struct DaqConfig {
    /// The API
    pub api: StreamApiDescr,

    /// Device name. Should match when starting a stream
    pub device_name: String,

    /// Configuration of the input channels
    pub inchannel_config: Vec<DaqChannel>,
    
    /// Configuration of the output channels
    pub outchannel_config: Vec<DaqChannel>,
    
    /// The data type to use
    pub dtype: DataType,

    /// Whether to apply a digital high pass on the input. <= 0 means disabled. > 0 means, the value specifies the cut-on frequency for the first order high pass filter.
    pub digitalHighPassCutOn: Flt,

    /// The index to use in the list of possible sample rates
    pub sampleRateIndex: usize,

    /// The index to use in the list of possible frames per block
    pub framesPerBlockIndex: usize,

    /// Used when output channels should be monitored, i.e. reverse-looped back as input channels.
    pub monitorOutput: bool,
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl DaqConfig {
    #[pyo3(name = "newFromDeviceInfo")]
    #[staticmethod]
    fn newFromDeviceInfo_py(d: &DeviceInfo) -> PyResult<DaqConfig> {
        Ok(DaqConfig::newFromDeviceInfo(d))
    }
    fn __repr__(&self) -> String {
        format!("{:#?}", self)
    }

}
impl DaqConfig {
    /// Creates a new default device configuration for a given device as specified with
    /// the DeviceInfo descriptor.
    pub fn newFromDeviceInfo(devinfo: &DeviceInfo) -> DaqConfig {
        let inchannel_config = (0..devinfo.iChannelCount)
            .map(|_| DaqChannel::default())
            .collect();
        let outchannel_config = (0..devinfo.oChannelCount)
            .map(|_| DaqChannel::default())
            .collect();

        let sampleRateIndex = devinfo
            .avSampleRates
            .iter()
            .position(|x| x == &devinfo.prefSampleRate)
            .unwrap_or(devinfo.avSampleRates.len() - 1);
        // Choose 4096 when in list, otherwise choose the highes available value in list
        let framesPerBlockIndex = devinfo
            .avFramesPerBlock
            .iter()
            .position(|x| x == &4096)
            .unwrap_or(devinfo.avFramesPerBlock.len() - 1);

        DaqConfig {
            api: devinfo.api.clone(),
            device_name: devinfo.device_name.clone(),
            inchannel_config,
            outchannel_config,
            dtype: devinfo.prefDataType,
            digitalHighPassCutOn: -1.0,
            sampleRateIndex,
            framesPerBlockIndex,
            monitorOutput: false,
        }
    }

    /// Serialize DaqConfig object to TOML.
    ///
    /// Args
    ///
    /// * writer: Output writer, can be file or string, or anything that *is* std::io::Write
    ///
    pub fn serialize_TOML(&self, writer: &mut dyn std::io::Write) -> Result<()> {
        let ser_str = toml::to_string(&self)?;
        writer.write_all(ser_str.as_bytes())?;

        Ok(())
    }

    /// Deserialize structure from TOML data
    ///
    /// # Args
    ///
    /// * reader: implements the Read trait, from which we read the data.
    pub fn deserialize_TOML<T>(reader: &mut T) -> Result<DaqConfig>
    where
        T: std::io::Read,
    {
        let mut read_str = vec![];
        reader.read_to_end(&mut read_str)?;
        let read_str = String::from_utf8(read_str)?;
        DaqConfig::deserialize_TOML_str(&read_str)
    }

    /// Deserialize from TOML string
    ///
    /// # Args
    ///
    /// * st: string containing TOML data.
    pub fn deserialize_TOML_str(st: &String) -> Result<DaqConfig> {
        let res: DaqConfig = toml::from_str(st)?;
        Ok(res)
    }

    /// Write this configuration to a TOML file.
    ///
    /// Args
    ///
    /// * file: Name of file to write to
    ///
    pub fn serialize_TOML_file(&self, file: &PathBuf) -> Result<()> {
        let mut file = std::fs::File::create(file)?;
        self.serialize_TOML(&mut file)?;
        Ok(())
    }

    /// Returns a list of enabled input channel numbers as indices
    /// in the list of all input channels (enabled and not)
    pub fn enabledInchannelsList(&self) -> Vec<usize> {
        self.inchannel_config
            .iter()
            .enumerate()
            .filter(|(_, ch)| ch.enabled)
            .map(|(i, _)| i)
            .collect()
    }

    /// Returns the total number of channels that appear in a running input stream.
    pub fn numberEnabledInChannels(&self) -> usize {
        self.inchannel_config.iter().filter(|ch| ch.enabled).count()
    }
    /// Returns the total number of channels that appear in a running output stream.
    pub fn numberEnabledOutChannels(&self) -> usize {
        self.outchannel_config
            .iter()
            .filter(|ch| ch.enabled)
            .count()
    }

    /// Provide samplerate, based on device and specified sample rate index
    pub fn sampleRate(&self, dev: &DeviceInfo) -> Flt {
        dev.avSampleRates[self.sampleRateIndex]
    }

    /// Provide samplerate, based on device and specified sample rate index
    pub fn framesPerBlock(&self, dev: &DeviceInfo) -> usize {
        dev.avFramesPerBlock[self.framesPerBlockIndex]
    }

    /// Returns vec of channel configuration for enabled input channels only
    pub fn enabledInchannelConfig(&self) -> Vec<DaqChannel> {
        self.inchannel_config
            .iter()
            .filter(|ch| ch.enabled)
            .cloned()
            .collect()
    }
    /// Returns vec of channel configuration for enabled output channels only
    pub fn enabledOutchannelConfig(&self) -> Vec<DaqChannel> {
        self.outchannel_config
            .iter()
            .filter(|ch| ch.enabled)
            .cloned()
            .collect()
    }

    /// Returns the channel number of the highest enabled input channel, if any.
    pub fn highestEnabledInChannel(&self) -> Option<usize> {
        let mut highest = None;

        self.inchannel_config.iter().enumerate().for_each(|(i,c)| if c.enabled {highest = Some(i);});

        highest
    }
    /// Returns the channel number of the highest enabled output channel, if any.
    pub fn highestEnabledOutChannel(&self) -> Option<usize> {
        let mut highest = None;

        self.outchannel_config.iter().enumerate().for_each(|(i,c)| if c.enabled {highest = Some(i);});
        println!("{:?}", highest);

        highest
    }


}
