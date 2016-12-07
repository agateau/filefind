from fnmatch import fnmatch


SUPER_WILDCARD = '**'


def find_pattern(pattern, path_components, start_idx=0):
    """Returns the index of the first element of `path_components` starting at
    `start_idx` to match `pattern`."""
    for idx, component in enumerate(path_components[start_idx:]):
        if fnmatch(component, pattern):
            return start_idx + idx
    return -1


class Pattern:
    def __init__(self, text):
        self._patterns = [x for x in text.split('/')]

    def match(self, path_components):
        if len(self._patterns) == 1:
            # name only pattern, can match anywhere
            return find_pattern(self._patterns[0], path_components) != -1

        # multi component pattern, must match at start
        idx = 0
        for pattern_idx, pattern in enumerate(self._patterns):
            if idx == len(path_components):
                # We reached the end of the path, but we are not done with all
                # the patterns
                return False

            if pattern == SUPER_WILDCARD:
                if pattern_idx == len(self._patterns) - 1:
                    # Pattern ends with super wildcard, we are done
                    return True

                next_pattern = self._patterns[pattern_idx + 1]
                idx = find_pattern(next_pattern, path_components, idx)
                if idx == -1:
                    return False
                # idx is on the component matching next_pattern, stop iteration
                # here to avoid incrementing twice
                continue

            if not fnmatch(path_components[idx], pattern):
                return False
            idx += 1
        return True
