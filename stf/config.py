import os


def _flatten_patterns(pattern_list):
    lst = [x.split() for x in pattern_list]
    # lst is a list of lists, this call to `sum()` flattens it
    return sum(lst, [])


def post_process_config(config):
    if not config.source_dir:
        if config.config:
            config.source_dir = os.path.dirname(config.config)
        else:
            config.source_dir = '.'
    config.source_dir = os.path.abspath(os.path.expanduser(config.source_dir))

    config.include = _flatten_patterns(config.include)
    config.exclude = _flatten_patterns(config.exclude)
