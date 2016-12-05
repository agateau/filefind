import os

import pytest

from stf.main import do_list_files, load_config


def create_files(tmpdir, *paths):
    for path in paths:
        full_path = os.path.join(tmpdir, path)
        dirname, basename = os.path.split(full_path)
        os.makedirs(dirname, exist_ok=True)
        if basename:
            open(full_path, 'w').close()


@pytest.mark.parametrize('args,expected', [
    (['--include', '*.cpp'],
        {'./foo.cpp', './bar.cpp', 'test/test_foo.cpp', 'build/moc_foo.cpp'}),
    (['--include', '*.cpp', '--exclude', 'build/* test_*'],
        {'./foo.cpp', './bar.cpp'}),
])
def test_list_files(args, expected, tmpdir):
    create_files(str(tmpdir),
                 'foo.cpp',
                 'foo.h',
                 'bar.cpp',
                 'bar.h',
                 'test/test_foo.cpp',
                 'build/',
                 'build/moc_foo.cpp')

    config = load_config(args)
    config.source_dir = str(tmpdir)

    assert(set(do_list_files(config)) == expected)
