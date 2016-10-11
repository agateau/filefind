import os


EXAMPLE_CONFIG = """
include=['*.cpp', '*.hpp', '*.h']
exclude=['dir1', 'foo/bar', 'moc_*.cpp']
processors=[
    'uncrustify -c path/to/uncrustify.cfg --replace --no-backup -F @filelist',
    'qpropertyformatter --files @filelist',
]
"""


class Config:
    __slots__ = ('include', 'exclude', 'processors', 'source_dir')

    def __init__(self):
        self.include = []
        self.exclude = []
        self.processors = []

    @staticmethod
    def from_path(config_path):
        dct = dict()
        with open(config_path, 'rt') as fp:
            src = fp.read()
        exec(src, dct)

        if not 'source_dir' in dct:
            dct['source_dir'] = os.path.dirname(config_path)
        dct['source_dir'] = os.path.abspath(dct['source_dir'])

        config = Config()
        for key in Config.__slots__:
            value = dct.get(key)
            if value is not None:
                setattr(config, key, value)
        return config



