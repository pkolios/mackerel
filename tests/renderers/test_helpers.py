from mackerel.renderers import helpers


def test_strip_tags():
    assert helpers.strip_tags('<em>Foo &amp; Bar</em>') == 'Foo & Bar'
    assert helpers.strip_tags('Foo & Bar') == 'Foo & Bar'
