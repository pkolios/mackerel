import shutil
from pathlib import Path

import pytest

from mackerel import build as build_module, content, renderers


@pytest.yield_fixture
def document_path():
    yield Path(__file__).parent / 'site' / 'content' / 'document.md'


@pytest.yield_fixture
def document_content(document_path):
    with document_path.open() as f:
        data = f.read()
    yield data


@pytest.yield_fixture
def document(document_path):
    doc = content.Document(
        document_path=document_path, renderer=renderers.MarkdownRenderer())
    yield doc


@pytest.yield_fixture
def source_path():
    yield Path(__file__).parent / 'site'


@pytest.yield_fixture
def source(source_path):
    yield content.Source(source_path)


@pytest.yield_fixture
def template_path():
    yield Path(__file__).parent / 'site' / 'template'


@pytest.yield_fixture
def output_path(source_path, tmpdir):
    path = Path(__file__).parent / 'site' / '_build'
    yield path
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


@pytest.yield_fixture
def build(source, markdown_renderer, jinja2renderer):
    b = build_module.Build(
        source=source, document_renderer=markdown_renderer,
        template_renderer=jinja2renderer)
    yield b


@pytest.yield_fixture
def build_documents(build):
    yield build.build_documents


@pytest.yield_fixture
def context(build):
    yield build.context


@pytest.yield_fixture
def markdown_renderer():
    yield renderers.MarkdownRenderer()


@pytest.yield_fixture
def jinja2renderer(template_path):
    yield renderers.Jinja2Renderer(template_path=template_path)
