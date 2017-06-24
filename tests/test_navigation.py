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
    uri = navigation._build_url(navigation._documents[0])
    assert uri == 'about.html'


def test_build_absolute_url(navigation):
    uri = navigation._build_absolute_url(navigation._documents[0])
    assert uri == 'http://localhost:8000/blog/about.html'
