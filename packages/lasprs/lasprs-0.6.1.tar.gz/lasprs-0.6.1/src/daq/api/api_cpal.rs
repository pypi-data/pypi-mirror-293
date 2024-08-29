#![allow(dead_code)]
use super::Stream;
use super::StreamMetaData;
use crate::config::{self, *};
use crate::daq::{self, *};
use crate::daq::{streamdata::*, StreamApiDescr};
use anyhow::{bail, Result};
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::SampleRate;
use cpal::SupportedStreamConfig;
use cpal::{Device, Host, Sample, SampleFormat, SupportedBufferSize};
use crossbeam::atomic::AtomicCell;
use crossbeam::channel::{Receiver, Sender};
use itertools::Itertools;
use num::ToPrimitive;
use reinterpret::reinterpret_slice;
use std::any;
use std::any::{Any, TypeId};
use std::collections::btree_map::OccupiedEntry;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::sync::Arc;

/// Convert CPAL sampleformat datatype
impl From<DataType> for cpal::SampleFormat {
    fn from(dt: DataType) -> cpal::SampleFormat {
        match dt {
            DataType::F64 => SampleFormat::F64,
            DataType::F32 => SampleFormat::F32,
            DataType::I8 => SampleFormat::I8,
            DataType::I16 => SampleFormat::I16,
            DataType::I32 => SampleFormat::I32,
        }
    }
}
// Convert datatype to CPAL sample format
impl From<cpal::SampleFormat> for DataType {
    fn from(sf: cpal::SampleFormat) -> DataType {
        match sf {
            SampleFormat::F64 => DataType::F64,
            SampleFormat::F32 => DataType::F32,
            SampleFormat::I8 => DataType::I8,
            SampleFormat::I16 => DataType::I16,
            SampleFormat::I32 => DataType::I32,
            _ => panic!("Not implemented sample format: {}", sf),
        }
    }
}

/// Cpal api
pub struct CpalApi {
    host: cpal::Host,
}
pub struct CpalStream {
    stream: cpal::Stream,
    metadata: Arc<StreamMetaData>,
    noutchannels: usize,
    status: Arc<AtomicCell<StreamStatus>>,
}
impl Stream for CpalStream {
    fn metadata(&self) -> Arc<StreamMetaData> {
        self.metadata.clone()
    }
    fn ninchannels(&self) -> usize {
        self.metadata.nchannels()
    }
    fn noutchannels(&self) -> usize {
        self.noutchannels
    }
    fn status(&self) -> StreamStatus {
        self.status.load()
    }
}

impl CpalApi {
    pub fn new() -> CpalApi {
        // for h in cpal::platform::available_hosts() {
        //     println!("h: {:?}", h);
        // }
        CpalApi {
            host: cpal::default_host(),
        }
    }
    pub fn getDeviceInfo(&self) -> Result<Vec<DeviceInfo>> {
        let srs_1 = [
            1000, 2000, 4000, 8000, 12000, 16000, 24000, 48000, 96000, 192000, 384000,
        ];
        let srs_2 = [11025, 22050, 44100, 88200];

        let mut srs_tot = Vec::from_iter(srs_1.iter().chain(srs_2.iter()));
        srs_tot.sort();
        let srs_tot = Vec::from_iter(srs_tot.iter().copied().map(|i| *i as Flt));

        // srs_tot.sort();

        let mut devs = vec![];
        'devloop: for dev in self.host.devices()? {
            // println!("{:?}", dev.name());
            let mut iChannelCount = 0;
            let mut oChannelCount = 0;

            let mut avSampleRates = srs_tot.clone();
            let mut avFramesPerBlock = vec![256_usize, 512, 1024, 2048, 8192];

            let mut sample_formats = vec![];
            // Search for sample formats
            if let Ok(icfg) = dev.supported_input_configs() {
                for icfg in icfg {
                    let thissf = icfg.sample_format();
                    if thissf.is_uint() {
                        continue;
                    }
                    sample_formats.push(icfg.sample_format());
                    avSampleRates.retain(|sr| *sr >= (icfg.min_sample_rate().0 as Flt));
                    avSampleRates.retain(|sr| *sr <= (icfg.max_sample_rate().0 as Flt));
                    if let SupportedBufferSize::Range { min, max } = icfg.buffer_size() {
                        avFramesPerBlock.retain(|i| i >= &(*min as usize));
                        avFramesPerBlock.retain(|i| i <= &(*max as usize));
                    }
                    iChannelCount = icfg.channels() as u8;
                    // avFramesPerBlock.retain(|i| i >= icfg.buffer_size().)
                }
            }
            if let Ok(ocfg) = dev.supported_output_configs() {
                for ocfg in ocfg {
                    let thissf = ocfg.sample_format();
                    if thissf.is_uint() {
                        continue;
                    }
                    sample_formats.push(thissf);
                    avSampleRates.retain(|sr| *sr >= (ocfg.min_sample_rate().0 as Flt));
                    avSampleRates.retain(|sr| *sr <= (ocfg.max_sample_rate().0 as Flt));
                    if let SupportedBufferSize::Range { min, max } = ocfg.buffer_size() {
                        avFramesPerBlock.retain(|i| i >= &(*min as usize));
                        avFramesPerBlock.retain(|i| i <= &(*max as usize));
                    }
                    oChannelCount = ocfg.channels() as u8;
                }
            }
            sample_formats.dedup();
            if sample_formats.is_empty() {
                continue;
            }

            let dtypes: Vec<DataType> =
                sample_formats.iter().dedup().map(|i| (*i).into()).collect();

            let prefDataType = match dtypes.iter().position(|d| d == &DataType::F32) {
                Some(idx) => dtypes[idx],
                None => dtypes[dtypes.len() - 1],
            };
            let prefSampleRate = *avSampleRates.last().unwrap_or(&48000.0);

            // Do not add device if it does not have any channels at all.
            if iChannelCount == oChannelCount && oChannelCount == 0 {
                break 'devloop;
            }
            devs.push(DeviceInfo {
                api: StreamApiDescr::Cpal,
                device_name: dev.name()?,
                avDataTypes: dtypes,
                prefDataType,

                avSampleRates,
                prefSampleRate,
                avFramesPerBlock,
                prefFramesPerBlock: 2048,

                iChannelCount,
                oChannelCount,

                hasInputIEPE: false,
                hasInputACCouplingSwitch: false,
                hasInputTrigger: false,
                hasInternalOutputMonitor: false,
                duplexModeForced: false,
                physicalIOQty: Qty::Number,
            });
        }

        Ok(devs)
    }

    // Create the error function closure, that capture the send channel on which error messages from the stream are sent
    fn create_errfcn(
        send_ch: Option<Sender<InStreamMsg>>,
        status: Arc<AtomicCell<StreamStatus>>,
    ) -> impl FnMut(cpal::StreamError) {
        move |err: cpal::StreamError| {
            let serr = match err {
                cpal::StreamError::DeviceNotAvailable => StreamError::DeviceNotAvailable,
                cpal::StreamError::BackendSpecific { err: _ } => StreamError::DriverError,
            };
            if let Some(sender) = &send_ch {
                sender.send(InStreamMsg::StreamError(serr)).unwrap();
            }
            status.store(StreamStatus::Error { e: serr });
        }
    }

    fn create_incallback<T>(
        meta: Arc<StreamMetaData>,
        config: &cpal::StreamConfig,
        sender: Sender<InStreamMsg>,
        framesPerBlock: usize,
        en_inchannels: Vec<usize>,
    ) -> impl FnMut(&[T], &cpal::InputCallbackInfo)
    where
        T: 'static + Sample + ToPrimitive,
    {
        let tot_inch = config.channels as usize;

        let mut q = VecDeque::<T>::with_capacity(2 * tot_inch * framesPerBlock);

        let mut enabled_ch_data: Vec<T> =
            vec![Sample::EQUILIBRIUM; en_inchannels.len() * framesPerBlock];

        // let meta = StreamMetaData::new()
        let mut ctr = 0;

        // The actual callback that is returned
        move |input: &[T], _: &cpal::InputCallbackInfo| {
            // Copy elements over in ring buffer
            q.extend(input);

            while q.len() > tot_inch * framesPerBlock {
                // Loop over enabled channels
                for (i, ch) in en_inchannels.iter().enumerate() {
                    let in_iterator = q.iter().skip(*ch).step_by(tot_inch);
                    let out_iterator = enabled_ch_data
                        .iter_mut()
                        .skip(i)
                        .step_by(en_inchannels.len());

                    // Copy over elements, *DEINTERLEAVED*
                    out_iterator.zip(in_iterator).for_each(|(o, i)| {
                        *o = *i;
                    });
                }

                // Drain copied elements from ring buffer
                q.drain(0..framesPerBlock * tot_inch);

                // Send over data
                let streamdata = Arc::new(InStreamData::new(
                    ctr,
                    meta.clone(),
                    enabled_ch_data.clone(),
                ));

                sender.send(InStreamMsg::InStreamData(streamdata)).unwrap();
                ctr += 1;
            }
        }
    }

    /// Create an input stream for a CPAL device.
    ///
    /// # Arguments
    ///
    /// * sf: Sample format
    fn build_input_stream(
        meta: Arc<StreamMetaData>,
        sf: cpal::SampleFormat,
        config: &cpal::StreamConfig,
        device: &cpal::Device,
        sender: Sender<InStreamMsg>,
        en_inchannels: Vec<usize>,
        framesPerBlock: usize,
    ) -> Result<(cpal::Stream, Arc<AtomicCell<StreamStatus>>)> {
        let status = Arc::new(AtomicCell::new(StreamStatus::NotRunning {}));

        let errfcn = CpalApi::create_errfcn(Some(sender.clone()), status.clone());

        macro_rules! build_stream {
            ($($cpaltype:pat => $rtype:ty),*) => {
                match sf {
                    $(
                        $cpaltype => {
                        let icb = CpalApi::create_incallback::<$rtype>(
                            meta,
                            &config, sender, framesPerBlock, en_inchannels);
                            device.build_input_stream(
                            &config,
                            icb,
                            errfcn,
                            None)?
                }),*,
                        _ => bail!("Unsupported sample format '{}'", sf)
                }
            };
        }
        let stream: cpal::Stream = build_stream!(
        SampleFormat::I8 => i8,
        SampleFormat::I16 => i16,
        SampleFormat::I32 => i32,
        SampleFormat::F32 => f32
        );
        Ok((stream, status))
    }

    fn create_outcallback<T>(
        config: &cpal::StreamConfig,
        streamstatus: Arc<AtomicCell<StreamStatus>>,
        receiver: Receiver<RawStreamData>,
        ch_config: &[DaqChannel],
        framesPerBlock: usize,
    ) -> impl FnMut(&mut [T], &cpal::OutputCallbackInfo)
    where
        T: 'static + Sample + Debug,
    {
        let number_total_out_channels: usize = config.channels as usize;
        let number_enabled_out_channels = ch_config.iter().filter(|ch| ch.enabled).count();

        let disabled_ch = DaqChannel::default();
        let disabled_repeater = std::iter::repeat(&disabled_ch);
        let enabled_outch = ch_config.iter().chain(disabled_repeater);

        // Vector of enabled output channells, with length of number_total_out_channels
        let enabled_outch: Vec<bool> = (0..number_total_out_channels)
            .zip(enabled_outch)
            .map(|(_, b)| b.enabled)
            .collect();
        assert_eq!(enabled_outch.len(), number_total_out_channels);

        let mut callback_ctr: usize = 0;
        let mut q = VecDeque::<T>::with_capacity(2 * number_total_out_channels * framesPerBlock);

        move |outdata, _info: &_| {
            let nsamples_asked =
                (outdata.len() / number_total_out_channels) * number_enabled_out_channels;
            let status = streamstatus.load();
            callback_ctr += 1;

            let mut setToEquilibrium = || {
                outdata.iter_mut().for_each(|v| {
                    *v = Sample::EQUILIBRIUM;
                })
            };
            match status {
                StreamStatus::NotRunning {} | StreamStatus::Error { .. } => {
                    setToEquilibrium();
                    return;
                }
                _ => {}
            }

            if q.len() < nsamples_asked {
                // Obtain new samples from the generator
                for dat in receiver.try_iter() {
                    let slice = dat.getRef::<T>();
                    if let StreamStatus::Running {} = status {
                        q.extend(slice);
                    }
                }
            }

            if q.len() >= nsamples_asked {
                // All right, we have enough samples to send out! They are
                // drained from the queue
                let out_chunks = outdata.iter_mut().chunks(number_total_out_channels);
                let siggen_chunks = q
                    .drain(..nsamples_asked)
                    .chunks(number_enabled_out_channels);
                for (och, ich) in out_chunks.into_iter().zip(siggen_chunks.into_iter()) {
                    let mut sig_frame_iter = ich.into_iter();
                    och.into_iter().zip(&enabled_outch).for_each(|(o, en)| {
                        if *en {
                            *o = sig_frame_iter.next().unwrap();
                        } else {
                            *o = Sample::EQUILIBRIUM;
                        }
                    });
                }

                // outdata
                //     .iter_mut()
                //     .zip(q.drain(..nsamples_asked))
                //     .for_each(|(o, i)| {
                //         *o = i;
                //     });
            } else if callback_ctr <= 2 {
                // For the first two blocks, we allow dat the data is not yet
                // ready, without complaining on underruns
                setToEquilibrium();
            } else {
                // Output buffer underrun
                streamstatus.store(StreamStatus::Error {
                    e: StreamError::OutputUnderrunError,
                });
                setToEquilibrium();
            }
        }
    }

    fn build_output_stream(
        sf: cpal::SampleFormat,
        config: &cpal::StreamConfig,
        device: &cpal::Device,
        receiver: Receiver<RawStreamData>,
        ch_config: &[DaqChannel],
        framesPerBlock: usize,
    ) -> Result<(cpal::Stream, Arc<AtomicCell<StreamStatus>>)> {
        let status = Arc::new(AtomicCell::new(StreamStatus::NotRunning {}));

        let err_cb = CpalApi::create_errfcn(None, status.clone());
        macro_rules! build_stream {
            ($($cpaltype:pat => $rtype:ty),*) => {
                match sf {
                    $(
                        $cpaltype => {
        let outcallback = CpalApi::create_outcallback::<$rtype>(config, status.clone(), receiver, ch_config, framesPerBlock);
                            device.build_output_stream(
                            &config,
                            outcallback,
                            err_cb,
                            None)?
                }),*,
                        _ => bail!("Unsupported sample format '{}'", sf)
                }
            };
        }
        let stream: cpal::Stream = build_stream!(
        SampleFormat::I8 => i8,
        SampleFormat::I16 => i16,
        SampleFormat::I32 => i32,
        SampleFormat::F32 => f32
        );

        Ok((stream, status))
    }

    /// Create CPAL specific configuration, from our specified daq config and device info
    fn create_cpal_config<T>(
        st: StreamType,
        devinfo: &DeviceInfo,
        conf: &DaqConfig,
        _dev: &cpal::Device,
        conf_iterator: T,
    ) -> Result<cpal::SupportedStreamConfig>
    where
        T: Iterator<Item = cpal::SupportedStreamConfigRange>,
    {
        let nchannels = match st {
            StreamType::Input => devinfo.iChannelCount,
            StreamType::Output => devinfo.oChannelCount,
            _ => unreachable!(),
        };
        for cpalconf in conf_iterator {
            if cpalconf.sample_format() == conf.dtype.into() {
                // Specified sample format is available
                if cpalconf.channels() == (nchannels as u16) {
                    let requested_sr = conf.sampleRate(devinfo);
                    if (cpalconf.min_sample_rate().0 as Flt) <= requested_sr
                        && (cpalconf.max_sample_rate().0 as Flt) >= requested_sr
                    {
                        // Sample rate falls within range.
                        let requested_fpb = conf.framesPerBlock(devinfo) as u32;
                        // Last check: check if buffer size is allowed
                        match cpalconf.buffer_size() {
                            SupportedBufferSize::Range { min, max } => {
                                if min >= &requested_fpb || max <= &requested_fpb {
                                    bail!(
                                        "Frames per block should be >= {} and <= {}. Requested {}.",
                                        min,
                                        max,
                                        requested_fpb
                                    );
                                }
                            }
                            _ => {}
                        }
                        return Ok(cpalconf.with_sample_rate(cpal::SampleRate(requested_sr as u32)));
                    }
                }
            }
        }
        bail!("API error: specified DAQ configuration is not available for device")
    }

    /// Start a stream for a device with a given configuration.
    pub fn startInputStream(
        &self,
        stype: StreamType,
        devinfo: &DeviceInfo,
        conf: &DaqConfig,
        sender: Sender<InStreamMsg>,
    ) -> Result<Box<dyn Stream>> {
        for cpaldev in self.host.devices()? {
            if cpaldev.name().unwrap_or("".to_string()) == conf.device_name {
                // See if we can create a supported stream config.
                let supported_config = (match stype {
                    StreamType::Duplex => bail!("Duplex stream not supported for CPAL"),
                    StreamType::Input => CpalApi::create_cpal_config(
                        stype,
                        devinfo,
                        conf,
                        &cpaldev,
                        cpaldev.supported_input_configs()?,
                    ),
                    StreamType::Output => CpalApi::create_cpal_config(
                        stype,
                        devinfo,
                        conf,
                        &cpaldev,
                        cpaldev.supported_output_configs()?,
                    ),
                })?;
                let framesPerBlock = conf.framesPerBlock(devinfo);

                let sf = supported_config.sample_format();
                let config: cpal::StreamConfig = supported_config.config();

                let meta = StreamMetaData::new(
                    &conf.enabledInchannelConfig(),
                    conf.dtype,
                    supported_config.sample_rate().0 as Flt,
                    framesPerBlock,
                );
                let meta = Arc::new(meta);

                let (stream, status) = CpalApi::build_input_stream(
                    meta.clone(),
                    sf,
                    &config,
                    &cpaldev,
                    sender,
                    conf.enabledInchannelsList(),
                    framesPerBlock,
                )?;

                stream.play()?;
                status.store(StreamStatus::Running {});

                return Ok(Box::new(CpalStream {
                    stream,
                    metadata: meta,
                    noutchannels: 0,
                    status,
                }));
            }
        }
        bail!(format!(
            "Error: requested device {} not found. Please make sure the device is available.",
            devinfo.device_name
        ))
    }

    /// Start a default input stream.
    ///
    ///
    pub fn startDefaultInputStream(
        &mut self,
        sender: Sender<InStreamMsg>,
    ) -> Result<Box<dyn Stream>> {
        if let Some(device) = self.host.default_input_device() {
            if let Ok(config) = device.default_input_config() {
                let framesPerBlock: usize = 4096;
                let final_config = cpal::StreamConfig {
                    channels: config.channels(),
                    sample_rate: config.sample_rate(),
                    buffer_size: cpal::BufferSize::Fixed(framesPerBlock as u32),
                };
                let en_inchannels = Vec::from_iter((0..config.channels()).map(|i| i as usize));

                let sf = config.sample_format();
                // Specify data tape
                let dtype = DataType::from(sf);

                // Daq: default channel config
                let daqchannels = Vec::from_iter(
                    (0..final_config.channels)
                        .map(|i| DaqChannel::defaultAudio(format!("Unnamed input channel {}", i))),
                );
                // Create stream metadata
                let metadata = StreamMetaData::new(
                    &daqchannels,
                    dtype,
                    config.sample_rate().0 as Flt,
                    framesPerBlock,
                );
                let metadata = Arc::new(metadata);

                let (stream, status) = CpalApi::build_input_stream(
                    metadata.clone(),
                    sf,
                    &final_config,
                    &device,
                    sender,
                    en_inchannels,
                    framesPerBlock,
                )?;
                stream.play()?;
                status.store(StreamStatus::Running {});

                Ok(Box::new(CpalStream {
                    stream,
                    metadata,
                    noutchannels: 0,
                    status,
                }))
            } else {
                bail!("Could not obtain default input configuration")
            }
        } else {
            bail!("Could not open default input device")
        }
    }

    fn getDefaultOutputConfig(&self) -> Result<(Device, cpal::StreamConfig, SampleFormat, usize)> {
        if let Some(dev) = self.host.default_output_device() {
            let cfg = dev.default_output_config()?;
            // let framesPerBlock: usize = 256;
            // let framesPerBlock: usize = 8192;
            let framesPerBlock: usize = cfg.sample_rate().0 as usize;
            // let framesPerBlock: usize = 256;
            let final_config = cpal::StreamConfig {
                channels: cfg.channels(),
                sample_rate: cfg.sample_rate(),
                buffer_size: cpal::BufferSize::Fixed(framesPerBlock as u32),
            };
            return Ok((dev, final_config, cfg.sample_format(), framesPerBlock));
        }
        bail!("Could not find default output device!");
    }

    pub fn startDefaultOutputStream(
        &self,
        receiver: Receiver<RawStreamData>,
    ) -> Result<Box<dyn Stream>> {
        let (device, config, sampleformat, framesPerBlock) = self.getDefaultOutputConfig()?;

        // Daq: default channel config
        let daqchannels = Vec::from_iter(
            (0..config.channels)
                .map(|i| DaqChannel::defaultAudio(format!("Unnamed output channel {}", i))),
        );
        let (stream, status) = CpalApi::build_output_stream(
            sampleformat,
            &config,
            &device,
            receiver,
            &daqchannels,
            framesPerBlock,
        )?;

        stream.play()?;
        status.store(StreamStatus::Running {});

        // // Specify data tape
        let dtype = DataType::from(sampleformat);

        // // Create stream metadata
        let md = StreamMetaData::new(
            &daqchannels,
            dtype,
            config.sample_rate.0 as Flt,
            framesPerBlock,
        );
        let md = Arc::new(md);
        let str = Box::new(CpalStream {
            stream,
            metadata: md,
            noutchannels: daqchannels.len(),
            status,
        });
        Ok(str)
    }

    fn getCPALOutputConfig(
        &self,
        dev: &DeviceInfo,
        daqconfig: &DaqConfig,
    ) -> Result<(Device, cpal::StreamConfig, SampleFormat, usize)> {
        let samplerate = dev.avSampleRates[daqconfig.sampleRateIndex] as u32;
        let framesPerBlock = dev.avFramesPerBlock[daqconfig.framesPerBlockIndex];

        let highest_ch: Result<usize, anyhow::Error> = daqconfig
            .highestEnabledOutChannel()
            .ok_or_else(|| anyhow::anyhow!("No output channels enabled."));
        let highest_ch = highest_ch? as u16;

        for cpaldev in self.host.devices()? {
            if cpaldev.name()? == dev.device_name {
                // Check, device name matches required device name
                for cpalcfg in cpaldev.supported_output_configs()? {
                    let sf = cpalcfg.sample_format();
                    if sf == daqconfig.dtype.into() {
                        let max_sr = cpalcfg.max_sample_rate().0;
                        let min_sr = cpalcfg.min_sample_rate().0;
                        if samplerate <= max_sr && samplerate >= min_sr {
                            let cfg = cpalcfg.with_sample_rate(SampleRate(samplerate));

                            let mut cfg = cfg.config();
                            cfg.channels = highest_ch + 1;

                            // Overwrite buffer size to required buffer size
                            cfg.buffer_size = cpal::BufferSize::Fixed(framesPerBlock as u32);

                            // Return tuple of device, config, sample format and
                            // frames per block
                            return Ok((cpaldev, cfg, sf, framesPerBlock));
                        }
                    }
                }
            }
        }
        bail!("Could not find device with name '{}'", dev.device_name)
    }

    pub fn startOutputStream(
        &self,
        dev: &DeviceInfo,
        cfg: &DaqConfig,
        receiver: Receiver<RawStreamData>,
    ) -> Result<Box<dyn Stream>> {
        let (device, cpalconfig, sampleformat, framesPerBlock) =
            self.getCPALOutputConfig(dev, cfg)?;

        let (stream, status) = Self::build_output_stream(
            sampleformat,
            &cpalconfig,
            &device,
            receiver,
            &cfg.outchannel_config,
            framesPerBlock,
        )?;

        stream.play()?;
        status.store(StreamStatus::Running {});

        // // Specify data tape
        let dtype = DataType::from(sampleformat);

        let md = StreamMetaData::new(
            &cfg.enabledOutchannelConfig(),
            dtype,
            cpalconfig.sample_rate.0 as Flt,
            framesPerBlock,
        );
        let md = Arc::new(md);
        let str = Box::new(CpalStream {
            stream,
            metadata: md,
            noutchannels: cpalconfig.channels as usize,
            status,
        });
        Ok(str)
    }
}
