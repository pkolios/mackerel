from pathlib import Path

import pytest

from mackerel import content, renderers


@pytest.yield_fixture
def document_path():
    yield Path(__file__).parent / 'content' / 'document.md'


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
    yield Path(__file__).parent / 'content'


@pytest.yield_fixture
def source(source_path):
    yield content.Source(source_path)


@pytest.yield_fixture
def template_path():
    yield Path(__file__).parent / 'templates'


@pytest.yield_fixture
def output_dir(tmpdir):
    tmp = tmpdir.mkdir('_build')
    yield Path(str(tmp))


@pytest.yield_fixture
def build(source, output_dir, markdown_renderer, jinja2renderer):
    build = content.Build(
        source=source, output_dir=output_dir,
        document_renderer=markdown_renderer, template_renderer=jinja2renderer)
    yield build


@pytest.yield_fixture
def context(build):
    yield build.context


@pytest.yield_fixture
def markdown_renderer():
    yield renderers.MarkdownRenderer()


@pytest.yield_fixture
def jinja2renderer(template_path):
    yield renderers.Jinja2Renderer(template_dir=template_path)
