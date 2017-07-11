import shutil
from pathlib import Path
from unittest import mock

import pytest

import mackerel


@pytest.yield_fixture
def document_path():
    yield Path(mackerel.__file__).parent / 'site' / 'content' / 'about.md'


@pytest.yield_fixture
def document_content(document_path):
    with document_path.open() as f:
        data = f.read()
    yield data


@pytest.yield_fixture
def document(document_path):
    doc = mackerel.content.Document(
        document_path=document_path,
        renderer=mackerel.renderers.MarkdownRenderer(site=mock.Mock()))
    yield doc


@pytest.yield_fixture
def site_path():
    yield Path(mackerel.__file__).parent / 'site'


@pytest.yield_fixture
def site(site_path, output_path):
    yield mackerel.site.Site(site_path)


@pytest.yield_fixture
def template_path():
    yield Path(mackerel.__file__).parent / 'site' / 'template'


@pytest.yield_fixture
def output_path(site_path):
    path = Path(mackerel.__file__).parent / 'site' / '_build'
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    yield path
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


@pytest.yield_fixture
def build(site):
    yield mackerel.build.Build(site=site)


@pytest.yield_fixture
def context(build):
    yield build.context
