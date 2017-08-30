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


def test_make_config(site_path):
    config = helpers.make_config(site_path=site_path)
    assert 'mackerel' in config
    for key in ('OUTPUT_PATH', 'CONTENT_PATH', 'TEMPLATE_PATH', 'DOC_EXT'):
        assert key in config['mackerel']
    assert config['mackerel']['TEMPLATE_PATH'] == 'template'
    assert config['mackerel']['OUTPUT_PATH'] == '_build'
    assert config['mackerel']['CONTENT_PATH'] == 'content'
    assert config['mackerel']['DOC_EXT'] == '.md'
