
use crossbeam::channel::{unbounded, Receiver};
use super::*;
use streammsg::InStreamMsg;

/// A stream handler registers a queue in the stream manager, and keeps the other end to 
/// get InStreamData from a running input stream.
pub struct StreamHandler {
    /// The receiving part of the channel on which (InStreamData) is received..
    pub rx: Receiver<InStreamMsg>
}
impl StreamHandler {
    /// Create new stream handler.
    pub fn new(smgr: &mut StreamMgr) -> StreamHandler{
        let (tx, rx) = unbounded();

        // The queue there is not 'drop()' in streamhandler, as StreamMgr
        // detects on its own when the stream other end of the channel is
        // dropped.
        smgr.addInQueue(tx);
        StreamHandler{rx}
    }

}

