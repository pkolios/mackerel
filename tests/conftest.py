import shutil
from pathlib import Path
from unittest import mock

import pytest

from mackerel import (
    build as build_module, site as site_module, content, renderers)


@pytest.yield_fixture
def document_path():
    yield Path(__file__).parent / 'site' / 'content' / 'about.md'


@pytest.yield_fixture
def document_content(document_path):
    with document_path.open() as f:
        data = f.read()
    yield data


@pytest.yield_fixture
def document(document_path):
    doc = content.Document(
        document_path=document_path,
        renderer=renderers.MarkdownRenderer(site=mock.Mock()))
    yield doc


@pytest.yield_fixture
def site_path():
    yield Path(__file__).parent / 'site'


@pytest.yield_fixture
def site(site_path, output_path):
    yield site_module.Site(site_path)


@pytest.yield_fixture
def template_path():
    yield Path(__file__).parent / 'site' / 'template'


@pytest.yield_fixture
def output_path(site_path):
    path = Path(__file__).parent / 'site' / '_build'
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
    yield build_module.Build(site=site)


@pytest.yield_fixture
def context(build):
    yield build.context
