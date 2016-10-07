import os

from configparser import ConfigParser


def list_submodules(source_dir):
    """Look for a .gitmodules in `source_dir`. If it finds it read it and
    returns a set of dirs to submodules. dirs are relative to source_dir"""

    filename = os.path.join(source_dir, '.gitmodules')

    if not os.path.exists(filename):
        return []

    cfg = ConfigParser()
    cfg.read(filename)
    for section in cfg.sections():
        if not section.startswith('submodule "'):
            continue
        yield cfg.get(section, 'path')
