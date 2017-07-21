from unittest import mock

from mackerel.renderers import document


class TestMistuneMarkdownRenderer:
    def test_init(self):
        with mock.patch('mackerel.renderers.document.mistune') as mistune:
            document.MistuneMarkdownRenderer(site=mock.Mock())

        mistune.Markdown.assert_called_with()

    def test_extract_metadata(self, document_content):
        with mock.patch('mackerel.renderers.document.mistune'):
            renderer = document.MistuneMarkdownRenderer(site=mock.Mock())

        assert renderer.extract_metadata(document_content) == {
            'title': 'About',
            'template': 'page.html',
            'body_class': 'post-template page-template page',
            'article_class': 'page'
        }

    def test_extract_text(self, document_content):
        with mock.patch('mackerel.renderers.document.mistune'):
            renderer = document.MistuneMarkdownRenderer(site=mock.Mock())

        assert renderer.extract_text(document_content) == (
            'This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.\n\nWe use this for '
            'testing and for reference!')

    def test_render(self, document_content):
        renderer = document.MistuneMarkdownRenderer(site=mock.Mock())
        text = renderer.extract_text(document_content)
        assert renderer.render(text) == (
            '<p>This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.</p>\n<p>We use this '
            'for testing and for reference!</p>\n')
