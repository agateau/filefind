#!/usr/bin/env python3
import argparse
import os
import logging
import subprocess
import sys

from fnmatch import fnmatch
from string import Template
from tempfile import TemporaryDirectory

from processall.config import Config, EXAMPLE_CONFIG
from processall.submodules import list_submodules


DESCRIPTION = """\
Apply processors to a list of files matching defined filters.
"""

EPILOG = """
Commands:

  list:      Print files which would be processed on stdout
  process:   Process the files
  genconfig: Print a sample config on stdout
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

    for dirpath, dirnames, filenames in os.walk(config.source_dir):

        # Since source_dir is always absolute, dirpath is absolute as well, so
        # we can create an absolute path based on it
        for submodule in list_submodules(dirpath):
            excluded_dirs.add(os.path.join(dirpath, submodule))

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


class InvalidArgumentsError(Exception):
    pass


def check_config(config):
    if config is None:
        raise InvalidArgumentsError('You need to provide a configuration with --config')


def command_list(config):
    check_config(config)
    write_file_list(sys.stdout, config)
    return 0


def command_process(config):
    check_config(config)

    with TemporaryDirectory(prefix='processall-') as tmp_dir_name:
        file_list = os.path.join(tmp_dir_name, 'lst')
        with open(file_list, 'wt') as fp:
            write_file_list(fp, config)

        for processor in config.processors:
            tmpl = AtTemplate(processor)
            cmd = tmpl.safe_substitute(filelist=file_list)
            logging.info('Running `{}`'.format(cmd))
            returncode = subprocess.call(cmd, cwd=config.source_dir, shell=True)
            if returncode != 0:
                logging.error('Command `{}` failed with error code {}'.format(cmd, returncode))
                return 1
    return 0


def command_genconfig(config):
    print(EXAMPLE_CONFIG)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = DESCRIPTION,
        epilog = EPILOG)

    parser.add_argument('-c', '--config', help='Configuration file')

    parser.add_argument('command', choices=['list', 'process', 'genconfig'],
        help='The command to run')

    args = parser.parse_args()

    if args.config:
        config = Config.from_path(args.config)
    else:
        config = None

    function = eval('command_' + args.command)
    try:
        return function(config)
    except InvalidArgumentsError as exc:
        print('Error: {}'.format(exc), file=sys.stderr)
        return -1


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
