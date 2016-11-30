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


def _load_config(config_name):
    with open(config_name) as fp:
        for line in fp.readlines():
            line = line.strip()
            if line and line[0] != '#':
                opt, value = line.split(' ', 1)
                yield '--' + opt
                if value:
                    yield value.strip()


def parse_args(parser, args=None):
    parser.add_argument('-c', '--config', help='Configuration file')

    if args is None:
        args = sys.argv[1:]
    config = parser.parse_args(args)

    if config.config:
        config_argv = _load_config(config.config)
        config = parser.parse_args(list(config_argv) + args)
    return config
