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


def test_make_config(site_path):
    config = helpers.make_config(site_path=site_path)
    assert 'mackerel' in config
    for key in ('OUTPUT_PATH', 'CONTENT_PATH', 'TEMPLATE_PATH', 'DOC_EXT'):
        assert key in config['mackerel']
    assert config['mackerel']['TEMPLATE_PATH'] == 'template'
    assert config['mackerel']['OUTPUT_PATH'] == '_build'
    assert config['mackerel']['CONTENT_PATH'] == 'content'
    assert config['mackerel']['DOC_EXT'] == '.md'
