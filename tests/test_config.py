import os

from io import StringIO

from processall.config import Config


def test_load_config():
    source = """
include: ['*.cpp']
exclude: ['vendor/dir/*']
processors: ['mycmd args']
"""

    with StringIO(source) as f:
        config = Config.from_file('some/dir', f)

    assert config.include == ['*.cpp']
    assert config.exclude == ['vendor/dir/*']
    assert config.processors == ['mycmd args']
    assert config.source_dir == os.path.abspath('some/dir')
