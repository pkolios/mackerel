from pathlib import Path

import pytest

from mackerel import helpers


def test_cached_property():
    class TestClass:
        counter = 0

        @helpers.cached_property
        def some_property(self):
            self.counter += 1
            return self.counter

    test_object = TestClass()
    assert test_object.counter == 0
    assert test_object.some_property == 1
    assert test_object.some_property == 1


@pytest.mark.parametrize('path', [
    'root.html',
    'foo/bar.html',
    'foo/bar/xyz.html',
])
def test_touch(tmpdir, path):
    tmp_dir = Path(str(tmpdir.mkdir('_helper_tests')))
    path = Path(tmp_dir, path)
    assert path.exists() is False
    helpers.touch(path)
    assert path.exists()
