import os

from fnmatch import fnmatch


class Pattern:
    def __init__(self, pattern_text):
        self._pattern_text = pattern_text

    def match(self, path_components, is_dir=False):
        path = os.path.join(*path_components)
        return fnmatch(path, self._pattern_text)
