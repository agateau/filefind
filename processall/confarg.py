"""
A generic system to define a configuration based on a config file and an
ArgumentParser.

Define your configuration options with ArgumentParser, then pass the parser and
to `parse_args`.

`parse_args` will add a `--config` argument. If this argument is set it must
points to a file which contain arguments, one per line, without the "--"
prefix.
"""
import os
import sys


def _parse_line(config_dir, line):
    line = line.strip()
    if not line or line[0] == '#':
        return

    idx = line.find(' ')
    if idx == -1:
        # Flag-like option
        yield '--' + line
        return

    opt = line[:idx]
    value = line[idx:].strip()

    if opt == 'config':
        config_path = os.path.join(config_dir, value)
        yield from _load_config(config_path)
    else:
        yield '--' + opt
        yield value


def _load_config(config_path):
    config_dir = os.path.dirname(config_path)
    with open(config_path) as fp:
        for line in fp.readlines():
            yield from _parse_line(config_dir, line)


def parse_args(parser, *, config_arg=None, args=None):
    if args is None:
        args = sys.argv[1:]

    if config_arg is None:
        parser.add_argument('-c', '--config', help='Configuration file')
        config_arg = 'config'

    config = parser.parse_args(args)

    config_path = getattr(config, config_arg)
    if config_path:
        config_argv = _load_config(config_path)
        config = parser.parse_args(list(config_argv) + args)
    return config
