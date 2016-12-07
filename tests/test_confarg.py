from argparse import ArgumentParser

from filefind.confarg import parse_args


def test_parse_args(tmpdir):
    config_file = tmpdir.join('file.cfg')
    config_file.write("""
# Some comment
include *.cpp
include *.hpp
flag

exclude vendor/dir/*
""")

    parser = ArgumentParser()
    parser.add_argument('--include', action='append')
    parser.add_argument('--exclude', action='append')
    parser.add_argument('--flag', action='store_true')

    args = ['--config', str(config_file), '--include', '*.h']

    config = parse_args(parser, args=args)

    assert config.include == ['*.cpp', '*.hpp', '*.h']
    assert config.flag is True
    assert config.exclude == ['vendor/dir/*']


def test_nested_config(tmpdir):
    config_file = tmpdir.join('file.cfg')
    config_file.write("""
config nested.cfg
foo
""")

    nested_file = tmpdir.join('nested.cfg')
    nested_file.write("""
bar
""")

    parser = ArgumentParser()
    parser.add_argument('--foo', action='store_true')
    parser.add_argument('--bar', action='store_true')

    args = ['--config', str(config_file)]

    config = parse_args(parser, args=args)

    assert config.foo is True
    assert config.bar is True
