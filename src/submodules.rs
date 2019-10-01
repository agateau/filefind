extern crate ini;

use ini::Ini;

use std::path::{Path, PathBuf};

fn find_gitmodules(path: &Path) -> Option<PathBuf> {
    let sm_path = path.join(".gitmodules");
    if sm_path.exists() {
        return Some(sm_path);
    }
    let parent = path.parent();
    if parent == None {
        return None;
    }
    return find_gitmodules(parent.unwrap());
}

fn parse_gitmodules(sm_path: &Path) -> Vec<PathBuf> {
    let mut paths : Vec<PathBuf> = Vec::new();
    let sm_dir : &Path = sm_path.parent().unwrap();
    let conf = Ini::load_from_file(sm_path).unwrap();
    for (section_name, _prop) in &conf {
        let section_name = section_name.as_ref().unwrap();
        if !section_name.starts_with("submodule ") {
            continue;
        }
        let section = conf.section(Some(section_name)).unwrap();
        let sub_path = section.get("path").unwrap();

        let path : PathBuf = sm_dir.join(sub_path);
        paths.push(path);
    }
    return paths;
    /*
    cfg = ConfigParser()
    cfg.read(gitmodules_path)
    for section in cfg.sections():
        if not section.startswith('submodule "'):
            continue
        path = cfg.get(section, 'path')
        path = os.path.join(gitmodules_dir, path)

        if path.startswith(source_dir):
            # Only yields paths inside source_dir
            yield path
            */

}

pub fn list_submodules(path: &Path) -> Vec<PathBuf> {
    let sm_path = find_gitmodules(&path.canonicalize().unwrap());
    if sm_path == None {
        return Vec::new();
    }
    return parse_gitmodules(&sm_path.unwrap());
}
