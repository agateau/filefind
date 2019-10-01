use std::fs;
use std::ffi::OsStr;
use std::path::{Path, PathBuf};
use structopt::StructOpt;
use globset::{Glob,GlobMatcher};

mod submodules;

/// Search for files whose names match pattern
#[derive(StructOpt)]
struct Config {
    /// The pattern to look for
    pattern: String,

    /// Do not go inside submodules
    #[structopt(long="exclude-submodules")]
    exclude_submodules: bool,
}

struct Context {
    matcher: GlobMatcher,
    excluded_dirs: Vec<PathBuf>,
}

fn does_match(matcher: &GlobMatcher, name: &OsStr) -> bool {
    let name_s = name.to_str().expect("Can't convert to str");
    matcher.is_match(name_s)
}

fn visit_dir(context: &Context, root: &Path) {
    let entries = fs::read_dir(root);
    if entries.is_err() {
        println!("ERROR: Can't read dir {}", root.display());
        return;
    }
    for entry in entries.unwrap() {
        let entry = entry.expect("Can't get entry");
        let file_type = entry.file_type().expect("Can't get file type");
        if file_type.is_dir() && !context.excluded_dirs.contains(&entry.path()) {
            visit_dir(&context, &entry.path());
        } else if does_match(&context.matcher, &entry.file_name()) {
            println!("{}", &entry.path().display());
        }
    }
}

fn create_matcher(pattern: &str) -> GlobMatcher {
    let mypat = pattern.replace("%", "*");
    Glob::new(&mypat).expect("Failed to create matcher").compile_matcher()
}

fn main() {
    let config = Config::from_args();

    let matcher = create_matcher(&config.pattern);

    let root = Path::new(".").canonicalize().unwrap();
    let excluded_dirs: Vec<PathBuf>;
    if config.exclude_submodules {
        excluded_dirs = submodules::list_submodules(&root);
    } else {
        excluded_dirs = Vec::new();
    }
    let context = Context{ matcher: matcher, excluded_dirs: excluded_dirs };
    visit_dir(&context, &root);
}
