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
            'title': 'Test post',
            'author': 'John Doe',
            'date': 'December 31, 2099',
            'template': 'document.html',
            'custom_meta': 'Nyancat',
        }

    def test_markdown_renderer_extract_text(self, document_content):
        with mock.patch('mackerel.renderers.mistune'):
            renderer = renderers.MarkdownRenderer(site=mock.Mock())

        assert renderer.extract_text(document_content) == (
            "It's very easy to produce words **bold** and *italic* with "
            "Markdown.\nYou can even [link to Google!](http://google.com)")

    def test_markdown_renderer_render(self, document_content):
        renderer = renderers.MarkdownRenderer(site=mock.Mock())
        text = renderer.extract_text(document_content)
        assert renderer.render(text) == (
            "<p>It\'s very easy to produce words <strong>bold</strong> and "
            "<em>italic</em> with Markdown.\nYou can even "
            "<a href=\"http://google.com\">link to Google!</a></p>\n")


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
        assert html == (
            '<html><head><title>Test</title></head><body><p>It\'s very easy '
            'to produce words <strong>bold</strong> and <em>italic</em> with '
            'Markdown.\nYou can even <a href="http://google.com">link to '
            'Google!</a></p>\n</body></html>')
