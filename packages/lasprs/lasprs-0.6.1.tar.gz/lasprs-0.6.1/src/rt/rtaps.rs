use std::ops::Deref;
use std::thread::{self, JoinHandle};

use crate::daq::{InStreamMsg, StreamHandler, StreamMetaData, StreamMgr};
use crate::ps::ApsSettings;
use crate::ps::{AvPowerSpectra, CPSResult};
use crate::I;
use anyhow::Result;
use parking_lot::Mutex;
use rayon::ThreadPool;
use std::sync::Arc;

enum RtApsComm {
    CommStopThread,
    NewResult(CPSResult),
    NewMeta(Arc<StreamMetaData>),
}
/// Result type coming from Real time Averaged Power Spectra computing engine
pub enum RtApsResult {
    /// New result
    NewResult(CPSResult),
    /// New metadata
    NewMeta(Arc<StreamMetaData>),
}

/// Real time power spectra viewer. Shows cross-power or auto-power signal 'time-dependent'
pub struct RtAps {
    /// Storage for optional last result
    comm: Arc<Mutex<Option<RtApsComm>>>,
    /// Settings used for real time power spectra.
    pub settings: ApsSettings,
}

impl RtAps {
    /// Create new Real time power spectra computing engine.
    pub fn new(mgr: &mut StreamMgr, settings: ApsSettings) -> RtAps {
        // Handler needs to be created here.
        let handler = StreamHandler::new(mgr);
        let last_result = Arc::new(Mutex::new(None));
        let last_result2 = last_result.clone();
        let settings2 = settings.clone();

        let mut aps = AvPowerSpectra::new(settings);

        let thread = std::thread::spawn(move || {
            // println!("Thread started...");
            let rx = handler.rx;
            // What is running on the thread

            'mainloop: loop {
                let mut last_cps: Option<CPSResult> = None;
                let mut meta: Option<Arc<StreamMetaData>> = None;

                if let Some(msg) = rx.recv_timeout(std::time::Duration::from_millis(10)).ok() {
                    match msg {
                        InStreamMsg::StreamStarted(new_meta) => {
                            aps.reset();
                            last_cps = None;
                            meta = Some(new_meta);
                        }
                        InStreamMsg::StreamStopped | InStreamMsg::StreamError(_) => {
                            debug_assert!(meta.is_none());
                            last_cps = None;
                        }
                        InStreamMsg::InStreamData(id) => {
                            debug_assert!(meta.is_none());
                            let flt = id.getFloatData();
                            if let Some(cpsresult) = aps.compute_last(flt.view()) {
                                last_cps = Some(cpsresult.clone());
                            }
                        }
                    }
                }

                // Communicate last result, if any.
                'commscope: {
                    let mut last_result_lock = last_result.lock();

                    if let Some(RtApsComm::CommStopThread) = *last_result_lock {
                        break 'mainloop;
                    }
                    if let Some(newmeta) = meta.take() {
                        // New metadata has arrived. This is always the first
                        // thing to push. Only when it is read, we will start
                        // pushing actual data.
                        *last_result_lock = Some(RtApsComm::NewMeta(newmeta));
                        break 'commscope;
                    }

                    if let Some(RtApsComm::NewMeta(_)) = *last_result_lock {
                        // New metadata is not yet read by reading thread. It
                        // basically means we are not yet ready to give actual
                        // data back.
                        break 'commscope;
                    }
                    // Move last_cps into mutex.
                    if let Some(last_cps) = last_cps.take() {
                        *last_result_lock = Some(RtApsComm::NewResult(last_cps));
                    }
                }
            } // End of loop
        });
        assert!(!thread.is_finished());

        RtAps {
            comm: last_result2,
            settings: settings2,
        }
    }
    /// Get last computed value. When new stream metadata is
    pub fn get_last(&self) -> Option<RtApsResult> {
        let mut lck = self.comm.lock();
        let res = lck.take();
        if let Some(res) = res {
            match res {
                RtApsComm::CommStopThread => panic!("BUG: CommStopThread should never be set!"),
                RtApsComm::NewMeta(m) => return Some(RtApsResult::NewMeta(m)),
                RtApsComm::NewResult(r) => return Some(RtApsResult::NewResult(r)),
            }
        }
        None
    }
}
impl Drop for RtAps {
    fn drop(&mut self) {
        let mut lck = self.comm.lock();
        *lck = Some(RtApsComm::CommStopThread);
    }
}

#[cfg(test)]
mod test {
    use std::time::Duration;

    use anyhow::{anyhow, bail, Result};

    use super::*;
    use crate::{daq::StreamMgr, ps::ApsSettingsBuilder};
    #[test]
    fn test_rtaps1() -> Result<(), anyhow::Error> {
        {
            let mut smgr = StreamMgr::new();
            smgr.startDefaultInputStream()?;
            let meta = smgr
                .getStreamMetaData(crate::daq::StreamType::Input)
                .ok_or_else(|| anyhow!("Stream is not running"))?;

            let settings = ApsSettingsBuilder::default()
                .nfft(2048)
                .fs(meta.samplerate)
                .build()
                .unwrap();
            let rtaps = RtAps::new(&mut smgr, settings);
            thread::sleep(Duration::from_secs(2));
            drop(rtaps);
        }
        Ok(())
    }
}
