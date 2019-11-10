use enchant;
use gumdrop::Options;
use std::path::Path;

mod cli;
mod errors;

use crate::cli::syntax::{Command, Opts};
use crate::errors::Error;

pub fn run_cmd() {
    let opts = Opts::parse_args_default_or_exit();
    match opts.command {
        None => {
            println!(
                "No command provided\nUsage:\n{}",
                Opts::command_list().unwrap()
            );
            std::process::exit(1);
        }
        Some(c) => on_command(c),
    }
}

fn on_command(c: Command) {
    let outcome = match c {
        Command::Check(opts) => check(&opts.path),
        Command::Add(opts) => add(&opts.word),
    };
    if let Err(e) = outcome {
        eprint!("{}", e);
        std::process::exit(1);
    }
}

fn check(path: &Path) -> Result<(), Error> {
    let mut broker = enchant::Broker::new();
    let dict = broker
        .request_dict("en_US")
        .map_err(|e| Error::new(format!("Could not request dict: {}", e)))?;
    dict.check("")
        .map_err(|e| Error::new(format!("Could not check: {}", e)))?;
    Ok(())
}

fn add(word: &str) -> Result<(), Error> {
    Ok(())
}
