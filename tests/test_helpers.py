from unittest import mock

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


def test_make_config():
    with mock.patch('configparser.ConfigParser.read') as cfg_read, \
            mock.patch('configparser.ConfigParser.read_file') as cfg_read_file:
        helpers.make_config(site_path='/random/path/')

    assert cfg_read_file.called
    cfg_read.assert_called_once_with('/random/path/.mackerelconfig')
