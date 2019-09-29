use std::fs;
use std::ffi::OsStr;
use std::path::Path;
use structopt::StructOpt;
use globset::{Glob,GlobMatcher};

/// Search for files whose names match pattern
#[derive(StructOpt)]
struct Cli {
    /// The pattern to look for
    pattern: String,
}

fn print_path(path: &Path) {
    let path_s = path.to_str().expect("Can't get path");
    println!("{}", path_s);
}

fn does_match(matcher: &GlobMatcher, name: &OsStr) -> bool {
    let name_s = name.to_str().expect("Can't convert to str");
    matcher.is_match(name_s)
}

fn visit_dir(matcher: &GlobMatcher, root: &Path) {
    for entry in fs::read_dir(root).expect("Can't read dir") {
        let entry = entry.expect("Can't get entry");
        let file_type = entry.file_type().expect("Can't get file type");
        if file_type.is_dir() {
            visit_dir(&matcher, &entry.path());
        } else if does_match(&matcher, &entry.file_name()) {
            print_path(&entry.path());
        }
    }
}

fn create_matcher(pattern: &str) -> GlobMatcher {
    let mypat = pattern.replace("%", "*");
    Glob::new(&mypat).expect("Failed to create matcher").compile_matcher()
}

fn main() {
    let args = Cli::from_args();

    let matcher = create_matcher(&args.pattern);

    let root = Path::new(".");
    visit_dir(&matcher, root);
}
