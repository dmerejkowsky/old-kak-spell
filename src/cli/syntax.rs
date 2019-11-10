use gumdrop::Options;

#[derive(Debug, Options)]
pub struct Opts {
    #[options(command)]
    pub command: Option<Command>,
}

#[derive(Debug, Options)]
pub enum Command {
    #[options(help = "check document for spelling errors")]
    Check(CheckOpts),

    #[options(help = "add word to personal word list")]
    Add(AddOpts),
}

#[derive(Debug, Options)]
pub struct CheckOpts {
    #[options(free, required)]
    pub path: std::path::PathBuf,
}

#[derive(Debug, Options)]
pub struct AddOpts {
    #[options(free, required)]
    pub word: String,
}
