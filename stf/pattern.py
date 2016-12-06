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
        pattern_items = self._pattern_items[:]
        if len(self._pattern_items) == 1:
            # name only pattern, find start
            first = pattern_items.pop(0)
            for idx, component in enumerate(path_components):
                if first.match(component):
                    break
            else:
                return False
        else:
            # multi path pattern, must match at start
            idx = -1

        # Check rest of the pattern matches
        for pattern in pattern_items:
            idx += 1
            if idx == len(path_components):
                # We reached the end of the path, but we are not done with all
                # the patterns
                return False
            if not pattern.match(path_components[idx]):
                return False
        return True
