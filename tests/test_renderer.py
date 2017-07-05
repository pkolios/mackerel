from unittest import mock

from mackerel import renderers


class TestMarkdownRenderer:
    def test_markdown_renderer_init(self):
        with mock.patch('mackerel.renderers.mistune') as mistune:
            renderers.MarkdownRenderer(site=mock.Mock())

        mistune.Markdown.assert_called_with()

    def test_markdown_renderer_extract_metadata(self, document_content):
        with mock.patch('mackerel.renderers.mistune'):
            renderer = renderers.MarkdownRenderer(site=mock.Mock())

        assert renderer.extract_metadata(document_content) == {
            'title': 'About',
            'template': 'page.html',
            'body_class': 'post-template page-template page',
            'article_class': 'page'
        }

    def test_markdown_renderer_extract_text(self, document_content):
        with mock.patch('mackerel.renderers.mistune'):
            renderer = renderers.MarkdownRenderer(site=mock.Mock())

        assert renderer.extract_text(document_content) == (
            'This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.\n\nWe use this for '
            'testing and for reference!')

    def test_markdown_renderer_strip_tags(self):
        renderer = renderers.MarkdownRenderer(site=mock.Mock())
        assert renderer.strip_tags('<em>Foo &amp; Bar</em>') == 'Foo & Bar'
        assert renderer.strip_tags('Foo & Bar') == 'Foo & Bar'

    def test_markdown_renderer_render(self, document_content):
        renderer = renderers.MarkdownRenderer(site=mock.Mock())
        text = renderer.extract_text(document_content)
        assert renderer.render(text) == (
            '<p>This is a demo site for Mackerel, it contains dummy content '
            'which allows you to click around and see what a Mackerel blog '
            'running Ghost\'s Casper theme looks like.</p>\n<p>We use this '
            'for testing and for reference!</p>\n')


class TestJinja2Renderer:
    def test_jinja2_renderer_init(self, site):
        with mock.patch('mackerel.renderers.jinja2') as jinja2:
            renderers.Jinja2Renderer(site=site)
        jinja2.FileSystemLoader.assert_called_with(
            str(site.template_path.resolve()))

        with mock.patch('mackerel.renderers.jinja2') as jinja2:
            renderers.Jinja2Renderer(site=site)
        jinja2.Environment.assert_called_with(
            loader=mock.ANY, lstrip_blocks=True, trim_blocks=True)

    def test_jinja2_renderer_render(self, site, document, context):
        renderer = renderers.Jinja2Renderer(site=site)
        html = renderer.render(ctx=context, document=document)
        assert '<!DOCTYPE html>' in html
        assert '<a href="/about.html">About</a>' in html
        assert '<h1 class="post-title">About</h1>' in html
