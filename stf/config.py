import argparse
import os

from stf.confarg import parse_args


DESCRIPTION = """\
A file finder tool, easier to use than `find`.
"""


def _flatten_patterns(pattern_list):
    lst = [x.split() for x in pattern_list]
    # lst is a list of lists, this call to `sum()` flattens it
    return sum(lst, [])


def post_process_config(config):
    if not config.directory:
        if config.config:
            config.directory = os.path.dirname(config.config)
        else:
            config.directory = '.'
    config.directory = os.path.abspath(os.path.expanduser(config.directory))

    config.include = _flatten_patterns(config.include +
                                       config.include_patterns)
    config.exclude = _flatten_patterns(config.exclude)


def load_config(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION)

    parser.add_argument('-i', '--include', action='append', default=[],
                        metavar='PATTERN', help='Patterns of files to include')
    parser.add_argument('-x', '--exclude', action='append', default=[],
                        metavar='PATTERN', help='Patterns of files to exclude')
    parser.add_argument('--exclude-submodules', action='store_true',
                        help='Do not go inside submodules')

    parser.add_argument('-C', '--directory', help='Base directory')

    parser.add_argument('--exec', action='append', dest='exec_',
                        help='Command to execute on the matching files. ' +
                             '@filelist in the command is replaced with the ' +
                             'path to a file containing the list of ' +
                             'matching files.')

    parser.add_argument('include_patterns', default=[],
                        nargs='*', help='Patterns of files to include',
                        metavar='PATTERN')

    config = parse_args(parser, args=args)
    post_process_config(config)
    return config
