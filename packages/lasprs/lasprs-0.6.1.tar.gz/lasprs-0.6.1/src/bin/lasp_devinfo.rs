use anyhow::Result;
use clap::Parser;
use lasprs::daq::{DaqConfig, StreamMgr};

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(author, version, about="Generates DAQ configurations for available devices.", long_about = None)]
struct Args {
    /// Devices to match. Search for these substrings in device names. Only
    /// configurations are output based on these names.
    #[arg(short, long)]
    matches: Vec<String>,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let write_all = args.matches.is_empty();
    let mut smgr = StreamMgr::new();

    // Obtain list of devices
    let devs = smgr.getDeviceInfo();

    // Iterate over them
    for dev in devs.iter() {
        // The file name will be the device name, plus toml extension
        let filename = dev.device_name.clone() + ".toml";

        // If no device name strings are given, we are outputting them all to a file.
        if write_all {
            let daqconfig = DaqConfig::newFromDeviceInfo(dev);
            daqconfig.serialize_TOML_file(&filename.clone().into())?;
        } else {
            // See if we find the name in the match list.
            for m in args.matches.iter() {
                let needle = m.to_lowercase();
                let dev_lower = dev.device_name.to_lowercase();
                if dev_lower.contains(&needle) {
                    DaqConfig::newFromDeviceInfo(dev)
                        .serialize_TOML_file(&filename.clone().into())?;
                }
            }
        }
    }

    Ok(())
}
