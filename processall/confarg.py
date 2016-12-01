"""
A generic system to define a configuration based on a config file and an
ArgumentParser.

Define your configuration options with ArgumentParser, then pass the parser and
to `parse_args`.

`parse_args` will add a `--config` argument. If this argument is set it must
points to a file which contain arguments, one per line, without the "--"
prefix.
"""
import sys


def _parse_line(line):
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
    yield '--' + opt
    yield value


def _load_config(config_name):
    with open(config_name) as fp:
        for line in fp.readlines():
            yield from _parse_line(line)


def parse_args(parser, args=None):
    parser.add_argument('-c', '--config', help='Configuration file')

    if args is None:
        args = sys.argv[1:]
    config = parser.parse_args(args)

    if config.config:
        config_argv = _load_config(config.config)
        config = parser.parse_args(list(config_argv) + args)
    return config
