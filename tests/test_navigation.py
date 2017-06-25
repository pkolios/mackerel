import pytest

from mackerel.navigation import Navigation


@pytest.yield_fixture
def navigation(build, site):
    yield Navigation(build.documents, site)


def test_navigation_init(build, site):
    navigation = Navigation(build.documents, site)
    assert navigation._documents == build.documents
    assert navigation._site == site


def test_navigation_nodes(navigation):
    assert len(navigation.nodes) == 5


def test_build_url(navigation):
    url = navigation._build_url(navigation._documents[0])
    assert url == 'about.html'


def test_build_absolute_url(navigation):
    url = navigation._build_absolute_url(navigation._documents[0])
    assert url == 'http://localhost:8000/blog/about.html'


def test_get_node(navigation):
    assert navigation.get_node('unknown_node.md') is None
    nodes = (navigation.get_node('about.md'),
             navigation.get_node(navigation._documents[0]))
    for node in nodes:
        assert node.document == navigation._documents[0]
        assert node.url == 'about.html'
        assert node.absolute_url == 'http://localhost:8000/blog/about.html'


def test_get_menu(navigation):
    assert navigation.get_menu('unknown_menu') == tuple()
    index, about = navigation.get_menu('main')
    assert index.url == 'index.html'
    assert about.url == 'about.html'
