import pytest

from stf.pattern import Pattern


@pytest.mark.parametrize('pattern_text,path,does_match', [
    # Match name only
    ('*.cpp', 'foo.cpp', True),
    ('*.cpp', 'dir/foo.cpp', True),
    ('*.cpp', 'dir/foo.h', False),
    ('dir', 'dir/foo.cpp', True),
    ('dir', 'sub/dir/foo.cpp', True),

    # Match dirs at start
    ('dir/*.cpp', 'dir/foo.cpp', True),
    ('dir/*.cpp', 'sub/dir/foo.cpp', False),

    ('sub/dir', 'sub/dir/foo.cpp', True),
    ('sub/dir/foo', 'sub/dir/foo.cpp', False),
    ('sub/dir', 'root/sub/dir/foo.cpp', False),

    ('sub/*/foo.cpp', 'sub/dir/foo.cpp', True),
    ('sub/*/foo.cpp', 'sub/dir1/dir2/foo.cpp', False),
    ('sub/*/foo.cpp', 'root/sub/dir/foo.cpp', False),

    # Trailing **
    ('sub/**', 'sub/dir/foo.cpp', True),
    ('sub/**', 'root/sub/dir/foo.cpp', False),
])
def test_match(pattern_text, path, does_match):
    pattern = Pattern(pattern_text)
    path_components = path.split('/')
    assert pattern.match(path_components) == does_match
