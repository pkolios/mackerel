from unittest import mock

import pytest

from mackerel import renderers


@pytest.yield_fixture
def document(document_mocks):
    content = (
        'Title: About\n'
        'Template: page.html\n'
        '\n'
        'Tales without end...')
    doc = document_mocks.create(content=content)
    yield doc


class TestMistuneMarkdownRenderer:
    def test_init(self):
        with mock.patch('mackerel.renderers.document.mistune') as mistune:
            renderers.document.MistuneMarkdownRenderer(site=mock.Mock())

        mistune.Markdown.assert_called_with()

    def test_extract_metadata(self, document):
        with mock.patch('mackerel.renderers.document.mistune'):
            renderer = renderers.document.MistuneMarkdownRenderer(
                site=mock.Mock())

        assert renderer.extract_metadata(document.content) == {
            'title': 'About',
            'template': 'page.html',
        }

    def test_render(self, document):
        renderer = renderers.document.MistuneMarkdownRenderer(site=mock.Mock())
        assert renderer.render(document.content) == (
            '<p>Tales without end...</p>\n')


class TestMarkdownMarkdownRenderer:
    def test_init(self, site):
        with mock.patch('mackerel.renderers.document.markdown') as markdown:
            renderers.document.MarkdownMarkdownRenderer(site=site)

        markdown.Markdown.assert_called_with(
            extensions=('markdown.extensions.meta',
                        'markdown.extensions.extra'),
            output_format='html5')

    def test_extract_metadata(self, site, document):
        renderer = renderers.document.MarkdownMarkdownRenderer(site=site)
        assert renderer.extract_metadata(document.content) == {
            'title': 'About',
            'template': 'page.html',
        }

    def test_render(self, site, document):
        renderer = renderers.document.MarkdownMarkdownRenderer(site=site)
        assert renderer.render(document.content) == (
            '<p>Tales without end...</p>')
