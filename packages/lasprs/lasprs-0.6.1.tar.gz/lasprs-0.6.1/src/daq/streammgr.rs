//! Data acquisition model. Provides abstract layers around DAQ devices.
use super::*;
use crate::{
    config::*,
    siggen::{self, Siggen},
};
use anyhow::{bail, Error, Result};
use api::StreamApiDescr;
use array_init::from_iter;
use core::time;
use cpal::Sample;
use crossbeam::{
    channel::{unbounded, Receiver, Sender, TrySendError},
    thread,
};
use std::sync::{atomic::AtomicBool, Arc, Mutex};
use std::thread::{JoinHandle, Thread};
use streamcmd::StreamCommand;
use streamdata::*;
use streammetadata::*;
use streammsg::*;

#[cfg(feature = "cpal-api")]
use super::api::{api_cpal::CpalApi, Stream};

/// Store a queue in a shared pointer, to share sending
/// and receiving part of the queue.
pub type SharedInQueue = Sender<InStreamMsg>;
/// Vector of queues for stream messages
pub type InQueues = Vec<SharedInQueue>;

struct StreamInfo<T> {
    streamtype: StreamType,
    stream: Box<dyn Stream>,
    threadhandle: JoinHandle<T>,
    comm: Sender<StreamCommand>,
}

/// Keep track of whether the stream has been created. To ensure singleton behaviour.
static smgr_created: AtomicBool = AtomicBool::new(false);

/// Configure and manage input / output streams. This method is supposed to be a
/// SINGLETON. Runtime checks are performed to see whether this is true.
///
/// A stream manager provides the interaction layer for interacting with audio /
/// data streams.
///
/// * See [Recording] for an example of starting a recording on an input stream.
/// * See [Siggen] for an example of playing a signal to an output stream.
///
#[cfg_attr(feature = "python-bindings", pyclass(unsendable))]
pub struct StreamMgr {
    // List of available devices
    devs: Vec<DeviceInfo>,

    // Input stream can be both input and duplex
    input_stream: Option<StreamInfo<InQueues>>,

    // Output only stream
    output_stream: Option<StreamInfo<Siggen>>,

    #[cfg(feature = "cpal-api")]
    cpal_api: CpalApi,

    /// The storage of queues. When no streams are running, they
    /// are here. When stream is running, they will become available
    /// in the JoinHandle of the thread.
    instreamqueues: Option<InQueues>,

    // Signal generator. Stored here on the bench in case no stream is running.
    // It is picked when it is configured correctly for the starting output stream
    // If it is not configured correctly, when a stream that outputs data is started
    // ,it is removed here.
    siggen: Option<crate::siggen::Siggen>,
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl StreamMgr {
    #[new]
    /// See (StreamMgr::new())
    fn new_py<'py>() -> StreamMgr {
        StreamMgr::new()
    }

    #[pyo3(name = "startDefaultInputStream")]
    fn startDefaultInputStream_py(&mut self) -> PyResult<()> {
        Ok(self.startDefaultInputStream()?)
    }
    #[pyo3(name = "startDefaultOutputStream")]
    fn startDefaultOutputStream_py(&mut self) -> PyResult<()> {
        Ok(self.startDefaultOutputStream()?)
    }
    #[pyo3(name = "startStream")]
    fn startStream_py(&mut self, st: StreamType, d: &DaqConfig) -> PyResult<()> {
        Ok(self.startStream(st, d)?)
    }
    #[pyo3(name = "stopStream")]
    fn stopStream_py(&mut self, st: StreamType) -> PyResult<()> {
        Ok(self.stopStream(st)?)
    }
    #[pyo3(name = "getDeviceInfo")]
    fn getDeviceInfo_py(&mut self) -> PyResult<Vec<DeviceInfo>> {
        Ok(self.getDeviceInfo())
    }
    #[pyo3(name = "getStatus")]
    fn getStatus_py(&self, st: StreamType) -> StreamStatus {
        self.getStatus(st)
    }
    #[pyo3(name = "setSiggen")]
    fn setSiggen_py(&mut self, siggen: Siggen) {
        self.setSiggen(siggen)
    }
}
impl Default for StreamMgr {
    fn default() -> Self {
        Self::new()
    }
}

impl StreamMgr {
    /// Create new stream manager. A stream manager is supposed to be a
    /// singleton. Note that we let Rust's ownership model handle that there is
    /// only a single [StreamMgr].
    ///
    /// # Panics
    ///
    /// When a StreamMgr object is already alive.
    ///
    pub fn new() -> StreamMgr {
        if smgr_created.load(std::sync::atomic::Ordering::Relaxed) {
            panic!("BUG: Stream manager is supposed to be a singleton");
        }
        smgr_created.store(true, std::sync::atomic::Ordering::Relaxed);

        let mut smgr = StreamMgr {
            devs: vec![],
            input_stream: None,
            output_stream: None,
            siggen: None,

            #[cfg(feature = "cpal-api")]
            cpal_api: CpalApi::new(),

            instreamqueues: Some(vec![]),
        };
        smgr.devs = smgr.scanDeviceInfo();
        smgr
    }

    /// Returns the metadata for a given stream, when the stream type (see
    /// [StreamType]) is alive, i.e. (StreamMgr::getStatus) gives a 'Running'.
    ///
    pub fn getStreamMetaData(&self, t: StreamType) -> Option<Arc<StreamMetaData>> {
        match t {
            StreamType::Input | StreamType::Duplex => {
                if let Some(s) = &self.input_stream {
                    return Some(s.stream.metadata());
                }
            }
            StreamType::Output => {
                if let Some(s) = &self.output_stream {
                    return Some(s.stream.metadata());
                }
            }
        }
        None
    }

    /// Get stream status for given stream type.
    pub fn getStatus(&self, t: StreamType) -> StreamStatus {
        match t {
            StreamType::Input | StreamType::Duplex => {
                if let Some(s) = &self.input_stream {
                    s.stream.status()
                } else {
                    StreamStatus::NotRunning {}
                }
            }
            StreamType::Output => {
                if let Some(s) = &self.output_stream {
                    s.stream.status()
                } else {
                    StreamStatus::NotRunning {}
                }
            }
        }
    }
    /// Set a new signal generator. Returns an error if it is unapplicable.
    /// It is unapplicable if the number of channels of output does not match the
    /// number of output channels in a running stream.
    pub fn setSiggen(&mut self, siggen: Siggen) {
        // Current signal generator. Where to place it?
        if let Some(istream) = &self.input_stream {
            if let StreamType::Duplex = istream.streamtype {
                assert!(self.siggen.is_none());
                istream.comm.send(StreamCommand::NewSiggen(siggen)).unwrap();
            }
        } else if let Some(os) = &self.output_stream {
            assert!(self.siggen.is_none());
            os.comm.send(StreamCommand::NewSiggen(siggen)).unwrap();
        } else {
            self.siggen = Some(siggen);
        }
    }

    /// Obtain a list of devices that are available for each available API
    pub fn getDeviceInfo(&mut self) -> Vec<DeviceInfo> {
        self.devs.clone()
    }

    fn scanDeviceInfo(&self) -> Vec<DeviceInfo> {
        let mut devinfo = vec![];
        #[cfg(feature = "cpal-api")]
        {
            let cpal_devs = self.cpal_api.getDeviceInfo();
            if let Ok(devs) = cpal_devs {
                devinfo.extend(devs);
            }
        }
        devinfo
    }

    /// Add a new queue to the lists of queues. On the queue, input data is
    /// added.
    ///
    /// If the stream is unable to write data on the queue (which might
    /// happen when the handler is dropped), the queue is removed from the list
    /// of queues that get data from the stream.
    pub fn addInQueue(&mut self, tx: Sender<InStreamMsg>) {
        if let Some(is) = &self.input_stream {
            is.comm.send(StreamCommand::AddInQueue(tx)).unwrap()
        } else {
            self.instreamqueues.as_mut().unwrap().push(tx);
        }
    }

    fn startInputStreamThread(
        &mut self,
        meta: Arc<StreamMetaData>,
        rx: Receiver<InStreamMsg>,
    ) -> (JoinHandle<InQueues>, Sender<StreamCommand>) {
        let (commtx, commrx) = unbounded();

        // Unwrap here, as the queues should be free to grab
        let mut iqueues = self
            .instreamqueues
            .take()
            .expect("No input streams queues!");

        let threadhandle = std::thread::spawn(move || {
            'infy: loop {
                if let Ok(comm_msg) = commrx.try_recv() {
                    match comm_msg {
                        // New queue added
                        StreamCommand::AddInQueue(queue) => {
                            match queue.send(InStreamMsg::StreamStarted(meta.clone())) {
                                Ok(()) => iqueues.push(queue),
                                Err(_) => {}
                            }
                        }

                        // Stop this thread. Returns the queue
                        StreamCommand::StopThread => {
                            sendMsgToAllQueuesRemoveUnused(
                                &mut iqueues,
                                InStreamMsg::StreamStopped,
                            );
                            break 'infy;
                        }
                        StreamCommand::NewSiggen(_) => {
                            panic!("Error: signal generator send to input-only stream.");
                        }
                    }
                }
                if let Ok(msg) = rx.recv_timeout(time::Duration::from_millis(10)) {

                    sendMsgToAllQueuesRemoveUnused(&mut iqueues, msg);
                }
            }
            iqueues
        });
        (threadhandle, commtx)
    }

    // Match device info struct on given daq config.
    fn find_device(&self, cfg: &DaqConfig) -> Result<&DeviceInfo> {
        if let Some(matching_dev) = self
            .devs
            .iter()
            .find(|&d| d.device_name == cfg.device_name && d.api == cfg.api)
        {
            return Ok(matching_dev);
        }
        bail!("Could not find device with name {}.", cfg.device_name);
    }
    fn startOuputStreamThread(
        &mut self,
        meta: Arc<StreamMetaData>,
        tx: Sender<RawStreamData>,
    ) -> (JoinHandle<Siggen>, Sender<StreamCommand>) {
        let (commtx, commrx) = unbounded();

        // Number of channels to output for
        let nchannels = meta.nchannels();

        // Obtain signal generator. Set to silence when no signal generator is
        // installed.
        let mut siggen = self
            .siggen
            .take()
            .unwrap_or_else(|| Siggen::newSilence(nchannels));

        if siggen.nchannels() != nchannels {
            // Updating number of channels
            siggen.setNChannels(nchannels);
        }
        siggen.reset(meta.samplerate);

        let threadhandle = std::thread::spawn(move || {
            let mut floatbuf: Vec<Flt> = Vec::with_capacity(nchannels * meta.framesPerBlock);
            'infy: loop {
                if let Ok(comm_msg) = commrx.try_recv() {
                    match comm_msg {
                        // New queue added
                        StreamCommand::AddInQueue(_) => {
                            panic!("Invalid message send to output thread: AddInQueue");
                        }

                        // Stop this thread. Returns the queue
                        StreamCommand::StopThread => {
                            break 'infy;
                        }
                        StreamCommand::NewSiggen(new_siggen) => {
                            // println!("NEW SIGNAL GENERATOR ARRIVED!");
                            siggen = new_siggen;
                            siggen.reset(meta.samplerate);
                            if siggen.nchannels() != nchannels {
                                // println!("Updating channels");
                                siggen.setNChannels(nchannels);
                            }
                        }
                    }
                }
                while tx.len() < 2 {
                    unsafe {
                        floatbuf.set_len(nchannels * meta.framesPerBlock);
                    }
                    // Obtain signal
                    siggen.genSignal(&mut floatbuf);
                    // println!("level: {}", floatbuf.iter().sum::<Flt>());
                    let msg = match meta.rawDatatype {
                        DataType::I8 => {
                            let v = Vec::<i8>::from_iter(floatbuf.iter().map(|f| f.to_sample()));
                            RawStreamData::Datai8(v)
                        }
                        DataType::I16 => {
                            let v = Vec::<i16>::from_iter(floatbuf.iter().map(|f| f.to_sample()));
                            RawStreamData::Datai16(v)
                        }
                        DataType::I32 => {
                            let v = Vec::<i32>::from_iter(floatbuf.iter().map(|f| f.to_sample()));
                            RawStreamData::Datai32(v)
                        }
                        DataType::F32 => {
                            let v = Vec::<f32>::from_iter(floatbuf.iter().map(|f| f.to_sample()));
                            RawStreamData::Dataf32(v)
                        }
                        DataType::F64 => {
                            let v = Vec::<f64>::from_iter(floatbuf.iter().map(|f| f.to_sample()));
                            RawStreamData::Dataf64(v)
                        }
                    };
                    if let Err(_e) = tx.send(msg) {
                        // println!("Error sending raw stream data to output stream!");
                        break 'infy;
                    }
                }
            }
            siggen
        });
        (threadhandle, commtx)
    }

    /// Start a stream of certain type, using given configuration
    pub fn startStream(&mut self, stype: StreamType, cfg: &DaqConfig) -> Result<()> {
        match stype {
            StreamType::Input | StreamType::Duplex => {
                self.startInputOrDuplexStream(stype, cfg)?;
            }
            StreamType::Output => {
                self.startOutputStream(cfg)?;
            }
        }
        Ok(())
    }

    /// Start a stream for output only, using only the output channel
    /// configuration as given in the `cfg`.
    fn startOutputStream(&mut self, cfg: &DaqConfig) -> Result<()> {
        let (tx, rx): (Sender<RawStreamData>, Receiver<RawStreamData>) = unbounded();
        let stream = match cfg.api {
            StreamApiDescr::Cpal => {
                let devinfo = self.find_device(cfg)?;
                cfg_if::cfg_if! {
                    if #[cfg(feature="cpal-api")] {
                            self.cpal_api.startOutputStream(devinfo, cfg, rx)?
                    } else {
                        bail!("API {} not available", cfg.api)
                    }
                }
            }
            _ => bail!("API {} not implemented!", cfg.api),
        };
        let meta = stream.metadata();
        let (threadhandle, commtx) = self.startOuputStreamThread(meta, tx);

        self.output_stream = Some(StreamInfo {
            streamtype: StreamType::Input,
            stream,
            threadhandle,
            comm: commtx,
        });

        Ok(())
    }

    // Start an input or duplex stream
    fn startInputOrDuplexStream(&mut self, stype: StreamType, cfg: &DaqConfig) -> Result<()> {
        if self.input_stream.is_some() {
            bail!("An input stream is already running. Please first stop existing input stream.")
        }
        if cfg.numberEnabledInChannels() == 0 {
            bail!("At least one input channel should be enabled for an input stream")
        }
        if stype == StreamType::Duplex {
            if cfg.numberEnabledOutChannels() == 0 {
                bail!("At least one output channel should be enabled for a duplex stream")
            }
            if self.output_stream.is_some() {
                bail!("An output stream is already running. Duplex mode stream cannot be started. Please first stop existing output stream.");
            }
        }
        let (tx, rx): (Sender<InStreamMsg>, Receiver<InStreamMsg>) = unbounded();

        let stream = match cfg.api {
            StreamApiDescr::Cpal => {
                if stype == StreamType::Duplex {
                    bail!("Duplex mode not supported for CPAL api");
                }
                let devinfo = self.find_device(cfg)?;
                cfg_if::cfg_if! {
                    if #[cfg(feature="cpal-api")] {
                        self.cpal_api.startInputStream(stype, devinfo, cfg, tx)?
                    } else {
                        bail!("API {} not available", cfg.api)
                    }
                }
            }
            _ => bail!("API {} not implemented!", cfg.api),
        };

        // Input queues should be available, otherwise panic bug.
        let iqueues = self.instreamqueues.as_mut().unwrap();

        let meta = stream.metadata();

        sendMsgToAllQueuesRemoveUnused(iqueues, InStreamMsg::StreamStarted(meta.clone()));

        let (threadhandle, commtx) = self.startInputStreamThread(meta, rx);

        self.input_stream = Some(StreamInfo {
            streamtype: stype,
            stream,
            threadhandle,
            comm: commtx,
        });

        Ok(())
    }

    /// Start a default input stream, using default settings on everything. This is only possible
    /// when the CPAL_api is available
    pub fn startDefaultInputStream(&mut self) -> Result<()> {
        if self.input_stream.is_some() {
            bail!("Input stream is already running. Please first stop existing input stream.")
        }

        let (tx, rx): (Sender<InStreamMsg>, Receiver<InStreamMsg>) = unbounded();

        // Only a default input stream when CPAL feature is enabled
        cfg_if::cfg_if! {
        if #[cfg(feature="cpal-api")] {
        let stream = self.cpal_api.startDefaultInputStream(tx)?;
                // Inform all listeners of new stream data

        let iqueues = self.instreamqueues.as_mut().unwrap();
        let meta = stream.metadata();
        sendMsgToAllQueuesRemoveUnused(iqueues, InStreamMsg::StreamStarted(meta.clone()));

        let (threadhandle, commtx) = self.startInputStreamThread(meta, rx);

        self.input_stream = Some(StreamInfo {
            streamtype: StreamType::Input,
            stream,
            threadhandle,
            comm: commtx,
        });
        Ok(())

        }
        else {
        bail!("Unable to start default input stream: no CPAL api available")
        }
        }
    }

    /// Start a default output stream. Only possible when CPAL Api is available.
    pub fn startDefaultOutputStream(&mut self) -> Result<()> {
        if let Some(istream) = &self.input_stream {
            if istream.streamtype == StreamType::Duplex {
                bail!("Duplex stream is already running");
            }
        }
        if self.output_stream.is_some() {
            bail!("An output stream is already running. Duplex mode stream cannot be started. Please first stop existing output stream.");
        }

        cfg_if::cfg_if! {
        if #[cfg(feature="cpal-api")] {

        let (tx, rx)= unbounded();
        let stream = self.cpal_api.startDefaultOutputStream(rx)?;
        let meta = stream.metadata();
        let (threadhandle, commtx) = self.startOuputStreamThread(meta, tx);
                // Inform all listeners of new stream data


        self.output_stream = Some(StreamInfo {
            streamtype: StreamType::Input,
            stream,
            threadhandle,
            comm: commtx,
        });
        Ok(())

        }  // end if cpal api available
        else {
        bail!("Unable to start default input stream: no CPAL api available")
        }

        } // end of cfg_if
    }

    /// Stop existing input stream.
    pub fn stopInputStream(&mut self) -> Result<()> {
        if let Some(StreamInfo {
            streamtype: _, // Ignored here
            stream: _,
            threadhandle,
            comm,
        }) = self.input_stream.take()
        {
            // println!("Stopping existing stream..");
            // Send thread to stop
            comm.send(StreamCommand::StopThread).unwrap();

            // Store stream queues back into StreamMgr
            self.instreamqueues = Some(threadhandle.join().expect("Stream thread panicked!"));
        } else {
            bail!("Stream is not running.")
        }
        Ok(())
    }
    /// Stop existing output stream
    pub fn stopOutputStream(&mut self) -> Result<()> {
        if let Some(StreamInfo {
            streamtype: _, // Ignored here
            stream: _,
            threadhandle,
            comm,
        }) = self.output_stream.take()
        {
            if comm.send(StreamCommand::StopThread).is_err() {
                // Failed to send command over channel. This means the thread is
                // already finished due to some other reason.
                assert!(threadhandle.is_finished());
            }
            // println!("Wainting for threadhandle to join...");
            self.siggen = Some(threadhandle.join().expect("Output thread panicked!"));
            // println!("Threadhandle joined!");
        } else {
            bail!("Stream is not running.");
        }
        Ok(())
    }
    /// Stop existing running stream.
    ///
    /// Args
    ///
    /// * st: The stream type.
    pub fn stopStream(&mut self, st: StreamType) -> Result<()> {
        match st {
            StreamType::Input | StreamType::Duplex => self.stopInputStream(),
            StreamType::Output => self.stopOutputStream(),
        }
    }
} // impl StreamMgr
impl Drop for StreamMgr {
    fn drop(&mut self) {
        // Kill input stream if there is one
        if self.input_stream.is_some() {
            self.stopStream(StreamType::Input).unwrap();
        }
        if self.output_stream.is_some() {
            // println!("Stopstream in Drop");
            self.stopStream(StreamType::Output).unwrap();
            // println!("Stopstream in Drop done");
        }

        // Decref the singleton
        smgr_created.store(false, std::sync::atomic::Ordering::Relaxed);
    }
}

/// Send to all queues, remove queues that are disconnected when found out
// on the way.
fn sendMsgToAllQueuesRemoveUnused(iqueues: &mut InQueues, msg: InStreamMsg) {
    // Loop over queues. Remove queues that error when we try to send
    // to them
    iqueues.retain(|q| match q.try_send(msg.clone()) {
        Ok(_) => true,
        Err(_e) => false,
    });
}
