import pytest
from unittest import mock

from mackerel.navigation import Navigation, Node


@pytest.yield_fixture
def navigation(site):
    yield Navigation(site)


def test_navigation_init(site):
    navigation = Navigation(site)
    assert navigation.site == site


def test_navigation_nodes(navigation):
    assert len(navigation.nodes) == 6


def test_build_url(navigation):
    url = navigation._build_url(navigation.site.documents[0])
    assert url == '/about.html'


def test_build_url_with_directory(navigation):
    with mock.patch.dict(navigation.site.config,
                         {'user': {'url': 'http://test/blog/'}}):
        url = navigation._build_url(navigation.site.documents[0])
        assert url == '/blog/about.html'


def test_build_url_with_missing_config_value(navigation):
    with mock.patch.dict(navigation.site.config, {'user': {}}):
        url = navigation._build_url(navigation.site.documents[0])
        assert url == '/about.html'


def test_build_external_url(navigation):
    url = navigation._build_external_url(navigation.site.documents[0])
    assert url == 'http://localhost:8000/about.html'


def test_build_external_url_with_directory(navigation):
    with mock.patch.dict(navigation.site.config,
                         {'user': {'url': 'http://test/blog/'}}):
        url = navigation._build_external_url(navigation.site.documents[0])
        assert url == 'http://test/blog/about.html'


def test_build_external_url_with_missing_config_value(navigation):
    with mock.patch.dict(navigation.site.config, {'user': {}}):
        url = navigation._build_external_url(navigation.site.documents[0])
        assert url == '/about.html'


def test_get_node(navigation):
    assert navigation.get_node('unknown_node.md') is None
    nodes = (navigation.get_node('about.md'),
             navigation.get_node(navigation.site.documents[0].relative_path))
    for node in nodes:
        assert node.document == navigation.site.documents[0]
        assert node.url == '/about.html'
        assert node.external_url == 'http://localhost:8000/about.html'


def test_get_menu(navigation):
    assert navigation.get_menu('unknown_menu') == tuple()
    index, about = navigation.get_menu('main')
    assert index.url == '/index.html'
    assert about.url == '/about.html'


def test_loop(navigation):
    nodes = navigation.loop()
    assert len(nodes) == 6
    for node in nodes:
        assert isinstance(node, Node)

    nodes = navigation.loop('about')
    assert len(nodes) == 0
    nodes = navigation.loop('/about')
    assert len(nodes) == 0

    nodes = navigation.loop('posts')
    assert len(nodes) == 2
    nodes = navigation.loop('/posts')
    assert len(nodes) == 2
