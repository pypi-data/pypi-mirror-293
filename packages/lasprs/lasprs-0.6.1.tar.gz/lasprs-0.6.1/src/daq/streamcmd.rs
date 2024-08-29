use crate::siggen::*;
use super::streammgr::SharedInQueue;


/// Commands that can be sent to a running stream
pub enum StreamCommand {
    /// Add a new queue to a running INPUT stream
    AddInQueue(SharedInQueue),

    /// New signal generator config to be used in OUTPUT stream
    NewSiggen(Siggen),

    /// Stop the thread, do not listen for data anymore.
    StopThread,

    // New signal generator source
    // NewSiggenSource(Source)
}
