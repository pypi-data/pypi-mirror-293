use anyhow::Result;
use crossbeam::channel::{unbounded, Receiver, TryRecvError};
use lasprs::daq::{StreamMgr, StreamStatus, StreamType};
use lasprs::siggen::Siggen;
use std::io;
use std::{thread, time};
// use

/// Spawns a thread and waits for a single line, pushes it to the receiver and  returns
fn stdin_channel_wait_for_return() -> Receiver<String> {

    let (tx, rx) = unbounded();
   thread::spawn(move || {
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer).unwrap();
        // Do not care whether we succeed here.
        let _ = tx.send(buffer);
    });
    rx
}
fn sleep(millis: u64) {
    let duration = time::Duration::from_millis(millis);
    thread::sleep(duration);
}
fn main() -> Result<()> {
    let mut smgr = StreamMgr::new();

    let stdin_channel = stdin_channel_wait_for_return();

    println!("Creating signal generator...");
    let mut siggen = Siggen::newSine(2, 432.);

    // Some things that can be done
    // siggen.setDCOffset(&[0.1, 0.]);

    // Reduce all gains a bit...
    siggen.setAllGains(0.1);


    println!("Starting stream...");
    smgr.startDefaultOutputStream()?;
    
    // Apply signal generator
    smgr.setSiggen(siggen);

    println!("Press <enter> key to quit...");
    'infy: loop {
        match stdin_channel.try_recv() {
            Ok(_key) => break 'infy,
            Err(TryRecvError::Empty) => {}
            Err(TryRecvError::Disconnected) => panic!("Channel disconnected"),
        }
        sleep(100);
        match smgr.getStatus(StreamType::Output) {
            StreamStatus::NotRunning{} => {
                println!("Stream is not running?");
                break 'infy;
            }
            StreamStatus::Running{} => {}
            StreamStatus::Error{e} => {
                println!("Stream error: {}", e);
                break 'infy;
            }
        }
    }

    Ok(())
}
