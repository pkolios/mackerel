import configparser
import logging
from pathlib import Path
from unittest import mock

import pytest

import mackerel


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
    site.content_path = Path('/tmp/mackerel/test/content')
    site.documents = (
        document_mocks.create(relative_path=Path('about.md')),
        document_mocks.create(relative_path=Path('index.md')),
        document_mocks.create(relative_path=Path('posts/hello.md')),
        document_mocks.create(relative_path=Path('posts/world.md')),
    )
    site.logger = mock.Mock(spec=logging.Logger)
    site.other_content_files = (
        Path('/tmp/mackerel/test/content/logo.svg'),
        Path('/tmp/mackerel/test/content/posts/image.png'),
    )
    site.other_template_files = (
        Path('/tmp/mackerel/test/templates/example/favicon.ico'),
        Path('/tmp/mackerel/test/templates/example/css/style.css'),
        Path('/tmp/mackerel/test/templates/example/js/app.js'),
    )
    site.output_path = Path('/tmp/mackerel/test/_build')
    site.path = Path('/tmp/mackerel/test')
    site.template_path = Path('/tmp/mackerel/test/templates/example')
    site.template_renderer = mock.Mock(
        spec=mackerel.renderers.base.TemplateRenderer)
    yield site


@pytest.yield_fixture
def site_path():
    yield Path(__file__).parent / 'site'
