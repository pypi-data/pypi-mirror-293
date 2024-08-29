use anyhow::Result;
use crossbeam::channel::{unbounded, Receiver, TryRecvError};
use lasprs::daq::{StreamHandler, StreamMgr, InStreamMsg};
use std::io;
use std::{thread, time};
// use

fn spawn_stdin_channel() -> Receiver<String> {
    let (tx, rx) = unbounded();
    thread::spawn(move || loop {
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer).unwrap();
        tx.send(buffer).unwrap();
    });
    rx
}
fn sleep(millis: u64) {
    let duration = time::Duration::from_millis(millis);
    thread::sleep(duration);
}
fn main() -> Result<()> {
    let mut smgr = StreamMgr::new();

    smgr.startDefaultInputStream()?;
    let stdin_channel = spawn_stdin_channel();

    let sh = StreamHandler::new(&mut smgr);

    'infy: loop {
        match stdin_channel.try_recv() {
            Ok(_key) => break 'infy,
            Err(TryRecvError::Empty) => {}
            Err(TryRecvError::Disconnected) => panic!("Channel disconnected"),
        }
        sleep(100);
        match sh.rx.try_recv() {
            Ok(msg) => {
                // eprint!("Obtained message: {:?}", msg);
                match msg {
                    InStreamMsg::StreamStarted(meta) => {
                        println!("Stream started metadata: {meta:#?}");
                    },
                    InStreamMsg::InStreamData(_) => {}
                    _ => { println!("Other msg...");}
                }
            }
            Err(e) => match e {
                TryRecvError::Disconnected => {
                    break 'infy;
                }
                TryRecvError::Empty => {}
            },
        }
    }

    Ok(())
}
