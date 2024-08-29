use anyhow::Result;
use crossbeam::channel::{ unbounded, Receiver, TryRecvError };
use lasprs::daq::{ DaqConfig, StreamMgr, StreamStatus, StreamType };
use lasprs::siggen::Siggen;
use std::io;
use std::time::Duration;
use std::{ thread, time };
// use

/// Spawns a thread and waits for a single line, pushes it to the receiver and  returns
fn stdin_channel_wait_for_return() -> Receiver<String> {
    let (tx, rx) = unbounded();
    thread::spawn(move || {
        loop {
            let mut buffer = String::new();
            io::stdin().read_line(&mut buffer).unwrap();
            // Do not care whether we succeed here.
            let _ = tx.send(buffer);
        }
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
    let mut siggen = Siggen::newSine(2, 432.0);

    // Reduce all gains a bit...
    siggen.setAllGains(0.1);

    // Apply signal generator
    smgr.setSiggen(siggen);

    println!("Starting stream...");
    let devs = smgr.getDeviceInfo();
    for (i, dev) in devs.iter().enumerate() {
        println!("No: {}, name: {}", i, dev.device_name);
    }
    print!("Please choose device by number [0-{}]: ", devs.len());
    let dev = loop {
        match stdin_channel.try_recv() {
            Ok(nostr) => {
                if let Ok(val) = nostr.trim().parse::<i32>() {
                    if (val as usize) > devs.len() - 1 {
                        println!(
                            "Invalid device number. Expected a value between 0 and {}. Please try again.",
                            devs.len()
                        );
                        continue;
                    }
                    break &devs[val as usize];
                } else {
                    println!("Invalid value. Please fill in a number. ");
                }
            }
            Err(TryRecvError::Empty) => {
                continue;
            }
            Err(TryRecvError::Disconnected) => panic!("Channel disconnected"),
        }
        thread::sleep(Duration::from_millis(100));
    };

    let mut cfg = DaqConfig::newFromDeviceInfo(dev);
    cfg.outchannel_config[0].enabled = true;
    cfg.outchannel_config[1].enabled = true;
    cfg.outchannel_config[2].enabled = true;

    smgr.startStream(StreamType::Output, &cfg)?;

    println!("Press <enter> key to quit...");
    'infy: loop {
        match stdin_channel.try_recv() {
            Ok(_key) => {
                break 'infy;
            }
            Err(TryRecvError::Empty) => {}
            Err(TryRecvError::Disconnected) => panic!("Channel disconnected"),
        }
        sleep(100);
        match smgr.getStatus(StreamType::Output) {
            StreamStatus::NotRunning {} => {
                println!("Stream is not running?");
                break 'infy;
            }
            StreamStatus::Running {} => {}
            StreamStatus::Error { e } => {
                println!("Stream error: {}", e);
                break 'infy;
            }
        }
    }

    Ok(())
}
