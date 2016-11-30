from argparse import ArgumentParser

from processall.confarg import parse_args


def test_parse_args(tmpdir):
    config_file = tmpdir.join('file.cfg')
    config_file.write("""
# Some comment
include *.cpp
include *.hpp

exclude vendor/dir/*
""")

    parser = ArgumentParser()
    parser.add_argument('--include', action='append')
    parser.add_argument('--exclude', action='append')

    args = ['--config', str(config_file), '--include', '*.h']

    config = parse_args(parser, args)

    assert config.include == ['*.cpp', '*.hpp', '*.h']
    assert config.exclude == ['vendor/dir/*']
