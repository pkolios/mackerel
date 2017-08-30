import configparser
import logging
import shutil
from pathlib import Path
from unittest import mock

import pytest

import mackerel


@pytest.yield_fixture
def content_path():
    yield Path(mackerel.__file__).parent / 'site' / 'content'


@pytest.yield_fixture
def document_path():
    yield Path(mackerel.__file__).parent / 'site' / 'content' / 'about.md'


@pytest.yield_fixture
def document_content(document_path):
    with document_path.open() as f:
        data = f.read()
    yield data


@pytest.yield_fixture
def document(document_path, content_path):
    doc = mackerel.content.Document(
        document_path=document_path,
        content_path=content_path,
        renderer=mackerel.renderers.document.MistuneMarkdownRenderer(
            site=mock.Mock()))
    yield doc


@pytest.yield_fixture
def site_path():
    yield Path(mackerel.__file__).parent / 'site'


# New fixtures
class DocumentMock:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


@pytest.yield_fixture
def document_mocks():
    class DocumentFactory:
        def create(self, **kwargs):
            return DocumentMock(**kwargs)
    return DocumentFactory()


@pytest.yield_fixture
def site(document_mocks):
    site = mock.Mock(spec=mackerel.site.Site)
    site.config = configparser.ConfigParser()
    site.config.read_dict({
        'mackerel': {'OUTPUT_EXT': '.html'},
        'user': {'url': 'http://localhost:8000/'},
        'navigation': {'main': 'index.md, about.md'},
        'Jinja2Renderer': {
            'TRIM_BLOCKS': True,
            'LSTRIP_BLOCKS': True,
        },
        'MarkdownMarkdownRenderer': {
            'OUTPUT_FORMAT': 'html5',
            'EXTENSIONS': 'markdown.extensions.meta, markdown.extensions.extra'
        }
    })
    site.content_path = Path('/tmp/mackerel/content')
    site.documents = (
        document_mocks.create(relative_path=Path('about.md')),
        document_mocks.create(relative_path=Path('index.md')),
        document_mocks.create(relative_path=Path('posts/hello.md')),
        document_mocks.create(relative_path=Path('posts/world.md')),
    )
    site.logger = mock.Mock(spec=logging.Logger)
    site.other_content_files = (
        Path('/tmp/mackerel/content/logo.svg'),
        Path('/tmp/mackerel/content/posts/image.png'),
    )
    site.other_template_files = (
        Path('/tmp/mackerel/templates/example/favicon.ico'),
        Path('/tmp/mackerel/templates/example/css/style.css'),
        Path('/tmp/mackerel/templates/example/js/app.js'),
    )
    site.output_path = Path('/tmp/mackerel/_build')
    site.path = Path('/tmp/mackerel')
    site.template_path = Path('/tmp/mackerel/templates/example')
    site.template_renderer = mock.Mock(
        spec=mackerel.renderers.base.TemplateRenderer)
    yield site
# End new fixtures


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
