use super::*;
use crate::config::Flt;
use anyhow::{bail, Error, Result};
use clap::builder::OsStr;
use crossbeam::atomic::AtomicCell;
use hdf5::types::{VarLenArray, VarLenUnicode};
use hdf5::{dataset, datatype, Dataset, File, H5Type};
use parking_lot::Mutex;
use std::path::{Path, PathBuf};
use std::str::FromStr;
use std::sync::atomic::{AtomicBool, Ordering::SeqCst};
use std::sync::Arc;
use std::thread::{spawn, JoinHandle};
use std::time::Duration;
use streamdata::*;
use streammgr::*;
use streammsg::InStreamMsg;
use strum::EnumMessage;

#[derive(Clone, Debug)]
/// Status of a recording
pub enum RecordStatus {
    /// Nothing to update
    NoUpdate,

    /// Not yet started, waiting for first msg
    Idle,

    /// Waiting for start delay to be processed.
    Waiting,

    /// Recording in progress
    Recording(Duration),

    /// Recording finished
    Finished,

    /// An error occurred, in any case when an error occurs, it is tried to remove the file.
    Error(String),
}

/// Settings used to start a recording.
#[derive(Clone)]
pub struct RecordSettings {
    /// File name to record to.
    pub filename: PathBuf,

    /// The recording time. Set to 0 to perform indefinite recording
    pub duration: Duration,

    /// The delay to wait before adding data
    pub startDelay: Duration,
}
impl RecordSettings {
    /// Create new record settings. Convenience wrapper to fill in fields in
    /// right form. Start delay is optional
    ///
    /// * args:
    ///     filename: Name of file to record to
    ///     duration: How long recording should be. Zero means record indefinitely.
    ///     startDelay: Optional start delay.
    pub fn new<T, U>(filename: T, duration: U, startDelay: Option<U>) -> RecordSettings
    where
        T: Into<PathBuf>,
        U: Into<Duration> + Default,
    {
        RecordSettings {
            filename: filename.into(),
            duration: duration.into(),
            startDelay: startDelay
                .map(|s| s.into())
                .unwrap_or_else(|| Duration::ZERO),
        }
    }
}

/// This struct lets a recording run on a stream, waits till the first data arrives and records for a given period of time. Usage:
///
/// ```
/// use lasprs::daq::{RecordSettings, StreamMgr, Recording};
/// use std::time::Duration;
///
/// fn main() -> anyhow::Result<()> {
/// let mut smgr = StreamMgr::new();
/// smgr.startDefaultInputStream()?;
///
/// // Create record settings
/// let settings = RecordSettings::new(
///  "test.h5",
///  Duration::from_millis(100),
///  None,
/// );
/// let rec = Recording::new(settings, &mut smgr)?;
/// Ok(())
/// }
/// ```
pub struct Recording {
    settings: RecordSettings,
    handle: Option<JoinHandle<Result<()>>>,

    // Stop the recording. This stops the thread
    stopThread: Arc<AtomicBool>,
    // Obtain status from thread.
    status_from_thread: Arc<AtomicCell<RecordStatus>>,
    // Stores latest status from thread, if no update comes from status_from_thread
    last_status: RecordStatus,
}

impl Recording {
    fn create_dataset_type<T>(file: &File, meta: &StreamMetaData) -> Result<Dataset>
    where
        T: H5Type,
    {
        let bs = meta.framesPerBlock;
        let nch = meta.nchannels();
        match file
            .new_dataset::<T>()
            .chunk((1, bs, nch))
            .shape((1.., bs, nch))
            // .deflate(3)
            .create("audio")
        {
            Ok(f) => Ok(f),
            Err(e) => bail!("{}", e),
        }
    }

    fn create_dataset(file: &File, meta: &StreamMetaData) -> Result<Dataset> {
        match meta.rawDatatype {
            DataType::I8 => Recording::create_dataset_type::<i8>(file, meta),
            DataType::I16 => Recording::create_dataset_type::<i16>(file, meta),
            DataType::I32 => Recording::create_dataset_type::<i32>(file, meta),
            DataType::F32 => Recording::create_dataset_type::<f32>(file, meta),
            DataType::F64 => Recording::create_dataset_type::<f64>(file, meta),
        }
    }

    fn write_hdf5_attr_scalar<T>(file: &File, name: &str, val: T) -> Result<()>
    where
        T: H5Type,
    {
        let attr = file.new_attr::<T>().create(name)?;
        attr.write_scalar(&val)?;
        Ok(())
    }
    fn write_hdf5_attr_list<T>(file: &File, name: &str, val: &[T]) -> Result<()>
    where
        T: H5Type,
    {
        let attr = file.new_attr::<T>().shape([val.len()]).create(name)?;
        attr.write(&val)?;
        Ok(())
    }

    #[inline]
    fn append_to_dset(
        ds: &Dataset,
        ctr: usize,
        data: &InStreamData,
        framesPerBlock: usize,
        nchannels: usize,
    ) -> Result<()> {
        match data.getRaw() {
            RawStreamData::Datai8(dat) => {
                let arr = ndarray::ArrayView2::<i8>::from_shape((framesPerBlock, nchannels), dat)?;
                ds.write_slice(arr, (ctr, .., ..))?;
            }
            RawStreamData::Datai16(dat) => {
                let arr =
                    ndarray::ArrayView2::<i16>::from_shape((framesPerBlock, nchannels), dat)?;
                ds.write_slice(arr, (ctr, .., ..))?;
            }
            RawStreamData::Datai32(dat) => {
                let arr =
                    ndarray::ArrayView2::<i32>::from_shape((framesPerBlock, nchannels), dat)?;
                ds.write_slice(arr, (ctr, .., ..))?;
            }
            RawStreamData::Dataf32(dat) => {
                let arr =
                    ndarray::ArrayView2::<f32>::from_shape((framesPerBlock, nchannels), dat)?;
                ds.write_slice(arr, (ctr, .., ..))?;
            }
            RawStreamData::Dataf64(dat) => {
                let arr =
                    ndarray::ArrayView2::<f64>::from_shape((framesPerBlock, nchannels), dat)?;
                ds.write_slice(arr, (ctr, .., ..))?;
            }
        }
        Ok(())
    }

    /// Start a new recording
    ///
    /// # Arguments
    ///
    /// * setttings: The settings to use for the recording
    /// * smgr: Stream manager to use to start the recording
    ///
    pub fn new(mut settings: RecordSettings, mgr: &mut StreamMgr) -> Result<Recording> {
        // Append extension if not yet there
        match settings.filename.extension() {
            Some(a) if a == "h5" => {}
            None | Some(_) => {
                settings.filename =
                    (settings.filename.to_string_lossy().to_string() + ".h5").into();
            }
        };

        let stopThread = Arc::new(AtomicBool::new(false));
        let stopThread_clone = stopThread.clone();

        // Fail if filename already exists
        if settings.filename.exists() {
            bail!(
                "Filename '{}' already exists in filesystem",
                settings.filename.to_string_lossy()
            );
        }
        let settings_clone = settings.clone();

        let status = Arc::new(AtomicCell::new(RecordStatus::Idle));
        let status_clone = status.clone();

        let (tx, rx) = crossbeam::channel::unbounded();
        mgr.addInQueue(tx.clone());

        // The thread doing the actual work
        let handle = spawn(move || {
            let file = File::create(settings.filename)?;

            let firstmsg = match rx.recv() {
                Ok(msg) => msg,
                Err(_) => bail!("Queue handle error"),
            };

            let meta = match firstmsg {
                InStreamMsg::StreamStarted(meta) => meta,
                _ => bail!("Recording failed. Missed stream metadata message."),
            };

            // Samplerate, block size, number of channels
            Recording::write_hdf5_attr_scalar(&file, "samplerate", meta.samplerate)?;
            Recording::write_hdf5_attr_scalar(&file, "nchannels", meta.nchannels())?;
            Recording::write_hdf5_attr_scalar(&file, "blocksize", meta.framesPerBlock)?;

            // Store sensitivity
            let sens: Vec<Flt> = meta.channelInfo.iter().map(|ch| ch.sensitivity).collect();
            Recording::write_hdf5_attr_list(&file, "sensitivity", &sens)?;

            // Timestamp
            use chrono::DateTime;
            let now_utc = chrono::Utc::now();
            let timestamp = now_utc.timestamp();
            Recording::write_hdf5_attr_scalar(&file, "time", timestamp)?;

            // Create UUID for measurement
            use hdf5::types::VarLenUnicode;
            let uuid = uuid::Uuid::new_v4();
            let uuid_unicode: VarLenUnicode = VarLenUnicode::from_str(&uuid.to_string()).unwrap();
            Recording::write_hdf5_attr_scalar(&file, "UUID", uuid_unicode)?;

            // Channel names
            let chnames: Vec<VarLenUnicode> = meta
                .channelInfo
                .iter()
                .map(|ch| VarLenUnicode::from_str(&ch.name).unwrap())
                .collect();
            let chname_attr = file
                .new_attr::<VarLenUnicode>()
                .shape([chnames.len()])
                .create("channelNames")?;
            chname_attr.write(&chnames)?;

            // Create the dataset
            let ds = Recording::create_dataset(&file, &meta)?;

            let framesPerBlock = meta.framesPerBlock as usize;
            let mut wait_block_ctr = 0;
            // Indicate we are ready to rec!
            if settings.startDelay > Duration::ZERO {
                status.store(RecordStatus::Waiting);
                let startdelay_s = settings.startDelay.as_micros() as Flt / 1e6;
                wait_block_ctr =
                    (meta.samplerate as Flt * startdelay_s / framesPerBlock as Flt) as u32;
            } else {
                status.store(RecordStatus::Recording(Duration::ZERO));
            }

            // Counter of stored blocks
            let mut stored_ctr = 0;

            // Offset in stream
            let mut ctr_offset = 0;

            // Flag indicating that the first RawStreamData package still has to
            // be arrived
            let mut first = true;

            // Indicating the file is still empty (does not contain recorded data)
            let mut empty_file = true;

            let nchannels = meta.nchannels() as usize;
            'recloop: loop {
                if stopThread.load(SeqCst) {
                    break 'recloop;
                }
                match rx.recv().unwrap() {
                    InStreamMsg::StreamError(e) => {
                        bail!("Recording failed due to stream error: {}.", e)
                    }
                    InStreamMsg::StreamStarted(_) => {
                        bail!("Stream started again?")
                    }
                    InStreamMsg::StreamStopped => {
                        // Early stop. User stopped it.
                        break 'recloop;
                    }
                    InStreamMsg::InStreamData(instreamdata) => {
                        if first {
                            first = false;
                            // Initialize counter offset
                            ctr_offset = instreamdata.ctr;
                        } else if instreamdata.ctr != stored_ctr + ctr_offset {
                            println!("********** PACKAGES MISSED ***********");
                            bail!("Packages missed. Recording is invalid.")
                        }

                        if wait_block_ctr > 0 {
                            // We are still waiting
                            wait_block_ctr -= 1;
                            if wait_block_ctr == 0 {
                                status.store(RecordStatus::Recording(Duration::ZERO));
                            }
                            // TODO: Is it a good idea to increase the counter
                            // here, as well as below?
                            stored_ctr += 1;
                            continue 'recloop;
                        }

                        ds.resize((stored_ctr + 1, framesPerBlock, nchannels))?;
                        Recording::append_to_dset(
                            &ds,
                            stored_ctr,
                            &instreamdata,
                            framesPerBlock,
                            nchannels,
                        )?;
                        // Once we have added to the file, this flag is swapped
                        // and a file should be deleted in case of an error.
                        empty_file = false;

                        // Recorded time rounded of to milliseconds.
                        let recorded_time = Duration::from_millis(
                            ((1000 * (stored_ctr + 1) * framesPerBlock) as Flt / meta.samplerate)
                                as u64,
                        );

                        if !settings.duration.is_zero() {
                            // Duration not equal to zero, meaning we record up to a
                            // certain duration.
                            if recorded_time >= settings.duration {
                                break 'recloop;
                            }
                        }
                        // println!("\n... {} {} {}", recorded_time.as_millis(), meta.samplerate, framesPerBlock);
                        stored_ctr += 1;
                        status.store(RecordStatus::Recording(recorded_time));
                    }
                }
            } // end of 'recloop

            if empty_file {
                bail!("Recording stopped before any data is stored.");
            }

            status.store(RecordStatus::Finished);
            Ok(())
            // End of thread
        });

        Ok(Recording {
            settings: settings_clone,
            stopThread: stopThread_clone,
            handle: Some(handle),
            last_status: RecordStatus::NoUpdate,
            status_from_thread: status_clone,
        })
    }

    // Delete recording file, should be done when something went wrong (an error
    // occured), or when cancel() is called, or when recording object is dropped
    // while thread is still running.
    fn deleteFile(&self) {
        if let Some(_) = self.handle {
            panic!("Misuse bug: cannot delete file while thread is still running");
        }
        // File should not be un use anymore, as thread is joined.
        // In case of error, we try to delete the file
        if let Err(e) = std::fs::remove_file(&self.settings.filename) {
            eprintln!("Recording failed, but file removal failed as well: {}", e);
        }
    }

    // Join the thread, store the last status. Please make sure it is joinable,
    // otherwise this method will hang forever.
    fn cleanupThread(&mut self) {
        if let Some(h) = self.handle.take() {
            let res = h.join().unwrap();
            if let Err(e) = res {
                self.last_status = RecordStatus::Error(format!("{}", e));
            }
        }
    }
    /// Get current record status
    pub fn status(&mut self) -> RecordStatus {
        // Update status due to normal messaging
        let status_from_thread = self.status_from_thread.swap(RecordStatus::NoUpdate);
        match status_from_thread {
            RecordStatus::NoUpdate => {}
            _ => {
                self.last_status = status_from_thread;
            }
        }

        if let Some(h) = &self.handle {
            // Update the status by taking any error messages
            if h.is_finished() {
                self.cleanupThread();
            }
        }
        // Return latest status
        self.last_status.clone()
    }

    /// Stop existing recording early. At the current time, or st
    pub fn stop(&mut self) {
        // Stop thread , join, update status
        self.stopThread.store(true, SeqCst);
        self.cleanupThread();
        match self.status() {
            RecordStatus::Finished => { // Do nothing
            }
            _ => {
                //  an error occured, we try to delete the backing file
                self.deleteFile()
            }
        }
    }

    /// Cancel recording. Deletes the recording file
    pub fn cancel(&mut self) {
        self.stopThread.store(true, SeqCst);
        self.cleanupThread();
        self.deleteFile();
    }
}

impl Drop for Recording {
    fn drop(&mut self) {
        if self.handle.is_some() {
            // If we enter here, stop() or cancel() has not been called. In that
            // case, we cleanup here by cancelling the recording
            self.cancel();
        }
    }
}
