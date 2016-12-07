import os


def _flatten_patterns(pattern_list):
    lst = [x.split() for x in pattern_list]
    # lst is a list of lists, this call to `sum()` flattens it
    return sum(lst, [])


def post_process_config(config):
    if not config.directory:
        if config.config:
            config.directory = os.path.dirname(config.config)
        else:
            config.directory = '.'
    config.directory = os.path.abspath(os.path.expanduser(config.directory))

    config.include = _flatten_patterns(config.include)
    config.exclude = _flatten_patterns(config.exclude)
