from fnmatch import fnmatch


class Pattern:
    def __init__(self, pattern_text):
        self._pattern_tokens = pattern_text.split('/')

    def match(self, path_components):
        # Find match start
        for idx, component in enumerate(path_components):
            if fnmatch(component, self._pattern_tokens[0]):
                break
        else:
            return False

        # Check rest of the pattern matches
        for pattern in self._pattern_tokens[1:]:
            idx += 1
            if idx == len(path_components):
                # We reached the end of the path, but we are not done with all
                # the patterns
                return False
            if not fnmatch(path_components[idx], pattern):
                return False
        return True
