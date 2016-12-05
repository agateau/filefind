import os

from stf.config import post_process_config


def test_post_process_config():
    class Config:
        pass
    config = Config()
    config.include = ['*.cpp *.h', '*.hpp']
    config.exclude = []
    config.source_dir = None
    config.config = None
    config.exec_ = None

    post_process_config(config)

    assert config.include == ['*.cpp', '*.h', '*.hpp']
    assert config.exclude == []
    assert config.source_dir == os.path.abspath('.')
