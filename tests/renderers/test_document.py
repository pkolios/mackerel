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

    def test_render(self, document_content):
        renderer = document.MistuneMarkdownRenderer(site=mock.Mock())
        assert renderer.render(document_content) == (
            '<p>This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.</p>\n<p>We use this '
            'for testing and for reference!</p>\n')


class TestMarkdownMarkdownRenderer:
    def test_init(self, site):
        with mock.patch('mackerel.renderers.document.markdown') as markdown:
            document.MarkdownMarkdownRenderer(site=site)

        markdown.Markdown.assert_called_with(
            extensions=('markdown.extensions.meta',
                        'markdown.extensions.extra'),
            output_format='html5')

    def test_extract_metadata(self, site, document_content):
        renderer = document.MarkdownMarkdownRenderer(site=site)
        assert renderer.extract_metadata(document_content) == {
            'title': 'About',
            'template': 'page.html',
            'body_class': 'post-template page-template page',
            'article_class': 'page'
        }

    def test_render(self, document_content, site):
        renderer = document.MarkdownMarkdownRenderer(site=site)
        assert renderer.render(document_content) == (
            '<p>This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.</p>\n<p>We use this '
            'for testing and for reference!</p>')
