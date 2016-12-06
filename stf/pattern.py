from fnmatch import fnmatch


SUPER_WILDCARD = '**'


class PatternItem:
    def match(self, text):
        raise NotImplementedError

    @staticmethod
    def parse(pattern_text):
        if pattern_text == SUPER_WILDCARD:
            return SuperPatternItem()
        else:
            return PlainPatternItem(pattern_text)


class PlainPatternItem(PatternItem):
    def __init__(self, pattern_text):
        self._pattern_text = pattern_text

    def match(self, text):
        return fnmatch(text, self._pattern_text)


class SuperPatternItem(PatternItem):
    def match(self, text):
        return True


class Pattern:
    def __init__(self, text):
        self._pattern_items = [PatternItem.parse(x) for x in text.split('/')]

    def match(self, path_components):
        if len(self._pattern_items) == 1:
            # name only pattern, can match anywhere
            pattern = self._pattern_items[0]
            for idx, component in enumerate(path_components):
                if pattern.match(component):
                    return True
            else:
                return False

        # multi component pattern, must match at start
        for idx, pattern in enumerate(self._pattern_items):
            if idx == len(path_components):
                # We reached the end of the path, but we are not done with all
                # the patterns
                return False
            if not pattern.match(path_components[idx]):
                return False
        return True
