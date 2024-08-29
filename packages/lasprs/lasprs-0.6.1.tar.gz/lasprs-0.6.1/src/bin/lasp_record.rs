use anyhow::Result;
use clap::{arg, command, Parser};
use crossbeam::channel::{unbounded, Receiver, TryRecvError};
#[cfg(feature = "record")]
use lasprs::daq::{RecordSettings, RecordStatus, Recording, StreamMgr, StreamType};
use lasprs::Flt;
use std::{
    io, thread,
    time::{self, Duration},
};

#[derive(Parser)]
#[command(author, version, about = "Record data to h5 file, according to LASP format", long_about = None)]
struct Cli {
    /// File name to write recording to
    filename: String,

    /// Recording duration in \[s\]. Rounds down to whole seconds. If not specified, records until user presses a key
    #[arg(short, long = "duration", default_value_t = 0.)]
    duration_s: Flt,

    /// Start delay in \[s\]. Rounds down to whole seconds. If not specified, no
    /// start delay will be used.
    #[arg(short, long = "startdelay", default_value_t = 0.)]
    start_delay_s: Flt,

    /// TOML configuration file for used stream
    #[arg(short, long = "config-file")]
    config_file_daq: Option<String>,
}
#[cfg(not(feature = "record"))]
fn main() -> Result<()> {
    bail!("Record feature not enabled. This executable is not working");
}

#[cfg(feature = "record")]
fn main() -> Result<()> {
    use lasprs::daq::DaqConfig;

    let ops = Cli::parse();

    let mut smgr = StreamMgr::new();
    let stdin_channel = spawn_stdin_channel();

    let settings = RecordSettings {
        filename: ops.filename.into(),
        duration: Duration::from_secs(ops.duration_s as u64),
        startDelay: Duration::from_secs(ops.start_delay_s as u64),
    };
    match ops.config_file_daq {
        // No config file is given, start default input stream
        None => smgr.startDefaultInputStream()?,
        Some(filename) => {
            // If config file is given, use that.
            let file = std::fs::read_to_string(filename)?;
            let cfg = DaqConfig::deserialize_TOML_str(&file)?;
            smgr.startStream(StreamType::Input, &cfg)?;
        }
    }

    let mut r = Recording::new(settings, &mut smgr)?;

    println!("Starting to record... Enter 'c' to cancel.");
    'infy: loop {
        match r.status() {
            RecordStatus::Idle => println!("\nIdle"),
            RecordStatus::Error(e) => {
                println!("\nRecord error: {}", e);
                break 'infy;
            }
            RecordStatus::Waiting => {
                println!("Waiting in start delay...");
            }
            RecordStatus::Finished => {
                println!("\nRecording finished.");
                break 'infy;
            }
            RecordStatus::Recording(duration) => {
                println!("Recording...   {} ms", duration.as_millis());
            }
            RecordStatus::NoUpdate => {}
        };

        match stdin_channel.try_recv() {
            Ok(_key) => {
                println!("User pressed key. Manually stopping recording here.");
                match _key.to_lowercase().as_str() {
                    "c" => r.cancel(),
                    _ => r.stop(),
                }
                break 'infy;
            }
            Err(TryRecvError::Empty) => {}
            Err(TryRecvError::Disconnected) => panic!("Channel disconnected"),
        }

        sleep(500);
    }

    Ok(())
}

fn sleep(millis: u64) {
    let duration = time::Duration::from_millis(millis);
    thread::sleep(duration);
}

fn spawn_stdin_channel() -> Receiver<String> {
    let (tx, rx) = unbounded();
    thread::spawn(move || loop {
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer).unwrap();
        tx.send(buffer).unwrap();
    });
    rx
}
