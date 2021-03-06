#!/usr/bin/env python3
import os
import logging
import subprocess
import sys

from fnmatch import fnmatch
from string import Template
from tempfile import TemporaryDirectory

from filefind.config import load_config
from filefind.pattern import Pattern
from filefind.submodules import list_submodules


class AtTemplate(Template):
    """Like template, but uses '@' as a delimiter to avoid clashes with
    environment variables."""
    delimiter = '@'


def match_patterns(patterns, path_components):
    for pattern in patterns:
        if pattern.match(path_components):
            return True
    return False


def do_list_files(config):
    excluded_dirs = {os.path.join(config.directory, '.git')}
    if config.exclude_submodules:
        for submodule in list_submodules(config.directory):
            excluded_dirs.add(os.path.join(config.directory, submodule))

    include_patterns = [Pattern(x) for x in config.include]
    exclude_patterns = [Pattern(x) for x in config.exclude]

    for dirpath, dirnames, filenames in os.walk(config.directory):
        relative_dirpath = os.path.relpath(dirpath, config.directory)
        dirpath_components = relative_dirpath.split('/')

        # Remove excluded_dirs from dirnames. We must modify the actual
        # dirnames instance, we can't replace it, hence the old-school
        # iteration
        for idx in range(len(dirnames) - 1, -1, -1):
            if os.path.join(dirpath, dirnames[idx]) in excluded_dirs:
                del dirnames[idx]
            elif match_patterns(exclude_patterns, dirpath_components + [dirnames[idx]]):
                del dirnames[idx]

        for filename in filenames:
            path_components = dirpath_components + [filename]
            if match_patterns(exclude_patterns, path_components):
                continue
            if include_patterns:
                if not match_patterns(include_patterns, path_components):
                    continue
            yield os.path.join(*path_components)


def list_files(config):
    for path in do_list_files(config):
        print(path)
    return 0


def run_commands(config):
    with TemporaryDirectory(prefix='filefind-') as tmp_dir_name:
        file_list = os.path.join(tmp_dir_name, 'lst')
        with open(file_list, 'wt') as fp:
            for path in do_list_files(config):
                print(path, file=fp)

        for command in config.exec_:
            tmpl = AtTemplate(command)
            cmd = tmpl.safe_substitute(filelist=file_list)
            logging.info('Running `{}`'.format(cmd))
            returncode = subprocess.call(cmd, cwd=config.directory, shell=True)
            if returncode != 0:
                logging.error('Command `{}` failed with error code {}'.format(cmd, returncode))
                return 1
    return 0


def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config(sys.argv[1:])

    if config.exec_:
        return run_commands(config)
    else:
        return list_files(config)


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
