use std::fs;
use std::ffi::OsStr;
use std::path::{Path, PathBuf};
use structopt::StructOpt;
use globset::{Glob,GlobMatcher};

mod submodules;

/// Search for files whose names match pattern
#[derive(StructOpt)]
struct Config {
    /// The patterns to look for
    patterns: Vec<String>,

    /// Do not go inside submodules
    #[structopt(long="exclude-submodules")]
    exclude_submodules: bool,
}

struct Context {
    matchers: Vec<GlobMatcher>,
    excluded_dirs: Vec<PathBuf>,
}

impl Context {
    fn is_match(&self, name: &OsStr) -> bool {
        let name_s = name.to_str().expect("Can't convert to str");
        for matcher in &self.matchers {
            if matcher.is_match(name_s) {
                return true;
            }
        }
        false
    }
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
        } else if context.is_match(&entry.file_name()) {
            println!("{}", &entry.path().display());
        }
    }
}

fn create_matcher(pattern: &str) -> Result<GlobMatcher, String> {
    let mypat = pattern.replace("%", "*");
    let glob = Glob::new(&mypat);
    match glob {
        Ok(x) => Ok(x.compile_matcher()),
        Err(x) => Err(x.to_string()),
    }
}

fn create_matchers(patterns: &Vec<String>) -> Result<Vec<GlobMatcher>, String> {
    let mut matchers : Vec<GlobMatcher> = Vec::new();
    for pattern in patterns {
        let matcher = create_matcher(&pattern);
        if let Err(message) = matcher {
            return Err(message);
        }
        matchers.push(matcher.unwrap());
    }
    Ok(matchers)
}

fn run_app() -> i32 {
    let config = Config::from_args();

    let matchers : Result<Vec<GlobMatcher>, String> = create_matchers(&config.patterns);
    if let Err(message) = matchers {
        println!("Can't parse pattern. {}", message);
        return 1;
    }

    let root = Path::new(".").canonicalize().unwrap();
    let excluded_dirs: Vec<PathBuf>;
    if config.exclude_submodules {
        excluded_dirs = submodules::list_submodules(&root);
    } else {
        excluded_dirs = Vec::new();
    }

    let context = Context{ matchers: matchers.unwrap(), excluded_dirs: excluded_dirs };
    visit_dir(&context, &root);
    return 0;
}

fn main() {
    ::std::process::exit(run_app());
}
