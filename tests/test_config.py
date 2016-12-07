import os

from stf.main import load_config
from stf.config import post_process_config


def test_post_process_config():
    config = load_config(['-i', '*.cpp *.h', '-i', '*.hpp'])
    post_process_config(config)

    assert config.include == ['*.cpp', '*.h', '*.hpp']
    assert config.exclude == []
    assert config.directory == os.path.abspath('.')
