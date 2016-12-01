#!/usr/bin/env python3
import argparse
import os
import logging
import subprocess
import sys

from fnmatch import fnmatch
from string import Template
from tempfile import TemporaryDirectory

from processall.confarg import parse_args
from processall.config import post_process_config
from processall.submodules import list_submodules


DESCRIPTION = """\
A file lister geared towards listing source code.
"""


class AtTemplate(Template):
    """Like template, but uses '@' as a delimiter to avoid clashes with
    environment variables."""
    delimiter = '@'


def path_match_patterns(path, patterns):
    for pattern in patterns:
        if fnmatch(path, pattern):
            return True
    return False


def must_be_included(path, exclude, include):
    if path_match_patterns(path, exclude):
        return False
    return path_match_patterns(path, include)


def write_file_list(fp, config):
    excluded_dirs = {os.path.join(config.source_dir, '.git')}
    for submodule in list_submodules(config.source_dir):
        excluded_dirs.add(os.path.join(config.source_dir, submodule))

    for dirpath, dirnames, filenames in os.walk(config.source_dir):
        # Remove excluded_dirs from dirnames. We must modify the actual
        # dirnames instance, we can't replace it, hence the old-school
        # iteration
        for idx in range(len(dirnames) - 1, -1, -1):
            if os.path.join(dirpath, dirnames[idx]) in excluded_dirs:
                del dirnames[idx]

        relative_root = os.path.relpath(dirpath, config.source_dir)
        for filename in filenames:
            path = os.path.join(relative_root, filename)
            if must_be_included(path, config.exclude, config.include):
                print(path, file=fp)


def list_files(config):
    write_file_list(sys.stdout, config)
    return 0


def run_commands(config):
    with TemporaryDirectory(prefix='processall-') as tmp_dir_name:
        file_list = os.path.join(tmp_dir_name, 'lst')
        with open(file_list, 'wt') as fp:
            write_file_list(fp, config)

        for command in config.exec_:
            tmpl = AtTemplate(command)
            cmd = tmpl.safe_substitute(filelist=file_list)
            logging.info('Running `{}`'.format(cmd))
            returncode = subprocess.call(cmd, cwd=config.source_dir, shell=True)
            if returncode != 0:
                logging.error('Command `{}` failed with error code {}'.format(cmd, returncode))
                return 1
    return 0


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = DESCRIPTION)

    parser.add_argument('-i', '--include', action='append',
                        help='Patterns of files to include')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Patterns of files to exclude')

    parser.add_argument('-s', '--source-dir', help='Base source directory')

    parser.add_argument('--exec', action='append', dest='exec_',
                        help='Command to execute on the matching files. @filelist in the command is replaced with the path to a file containing the list of matching files.')

    config = parse_args(parser)
    post_process_config(config)

    if config.exec_:
        return run_commands(config)
    else:
        return list_files(config)


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
