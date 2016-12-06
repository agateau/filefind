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

    def __repr__(self):
        return '<PlainPatternItem "{}">'.format(self._pattern_text)


class SuperPatternItem(PatternItem):
    def match(self, text):
        return True

    def __repr__(self):
        return '<SuperPatternItem>'


def find_pattern(pattern, path_components, start_idx=0):
    for idx, component in enumerate(path_components[start_idx:]):
        if pattern.match(component):
            return start_idx + idx
    return -1


class Pattern:
    def __init__(self, text):
        self._pattern_items = [PatternItem.parse(x) for x in text.split('/')]

    def match(self, path_components):
        if len(self._pattern_items) == 1:
            # name only pattern, can match anywhere
            return find_pattern(self._pattern_items[0], path_components) != -1

        # multi component pattern, must match at start
        idx = 0
        for pattern_idx, pattern in enumerate(self._pattern_items):
            if idx == len(path_components):
                # We reached the end of the path, but we are not done with all
                # the patterns
                return False
            if isinstance(pattern, SuperPatternItem):
                if pattern_idx == len(self._pattern_items) - 1:
                    # Pattern ends with super pattern, we are done
                    return True
                else:
                    next_pattern = self._pattern_items[pattern_idx + 1]
                    idx = find_pattern(next_pattern, path_components, idx)
                    if idx == -1:
                        return False
                    # idx is on the component matching next_pattern, stop
                    # iteration here to avoid incrementing twice
                    continue
            if not pattern.match(path_components[idx]):
                return False
            idx += 1
        return True
