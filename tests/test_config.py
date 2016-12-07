import os

from filefind.config import load_config


def test_post_process_config():
    config = load_config(['-i', '*.cpp *.h', '--include', '*.hpp'])

    assert config.include == ['*.cpp', '*.h', '*.hpp']
    assert config.exclude == []
    assert config.directory == os.path.abspath('.')


def test_include_as_position_arguments():
    config = load_config(['-i', '*.cpp *.h', '*.hpp'])

    assert config.include == ['*.cpp', '*.h', '*.hpp']
