import os

from configparser import ConfigParser


def _find_gitmodules(source_dir):
    path = os.path.join(source_dir, '.gitmodules')
    if os.path.exists(path):
        return path
    parent_dir = os.path.normpath(os.path.join(source_dir, os.path.pardir))
    if source_dir == parent_dir:
        return None
    return _find_gitmodules(parent_dir)


def list_submodules(source_dir):
    """Looks for a .gitmodules in `source_dir` or its parents. If it finds one,
    it reads it and returns a set of dirs to submodules. dirs are absolutes"""

    gitmodules_path = _find_gitmodules(source_dir)
    if not gitmodules_path:
        return []
    gitmodules_dir = os.path.dirname(gitmodules_path)

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
