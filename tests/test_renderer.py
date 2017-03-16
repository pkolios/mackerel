from unittest import mock

from mackerel import renderers


class TestMarkdownRenderer:
    def test_markdown_renderer_init(self):
        with mock.patch('mackerel.renderers.mistune') as mistune:
            renderers.MarkdownRenderer()

        mistune.Markdown.assert_called_with()

    def test_markdown_renderer_extract_metadata(self, document_content):
        with mock.patch('mackerel.renderers.mistune'):
            renderer = renderers.MarkdownRenderer()

        assert renderer.extract_metadata(document_content) == {
            'title': 'Test post',
            'author': 'John Doe',
            'date': 'December 31, 2099',
            'template': 'document.html',
        }

    def test_markdown_renderer_extract_text(self, document_content):
        with mock.patch('mackerel.renderers.mistune'):
            renderer = renderers.MarkdownRenderer()

        assert renderer.extract_text(document_content) == (
            "It's very easy to produce words **bold** and *italic* with "
            "Markdown.\nYou can even [link to Google!](http://google.com)")

    def test_markdown_renderer_render(self, document_content):
        renderer = renderers.MarkdownRenderer()
        text = renderer.extract_text(document_content)
        assert renderer.render(text) == (
            "<p>It\'s very easy to produce words <strong>bold</strong> and "
            "<em>italic</em> with Markdown.\nYou can even "
            "<a href=\"http://google.com\">link to Google!</a></p>\n")


def test_jinja2_renderer(template_path, document, context):
    renderer = renderers.Jinja2Renderer(template_path)
    html = renderer.render(ctx=context, document=document)
    assert html == (
        '<html><head><title>Test</title></head><body><p>It\'s very easy to '
        'produce words <strong>bold</strong> and <em>italic</em> with '
        'Markdown.\nYou can even <a href="http://google.com">link to Google!'
        '</a></p>\n</body></html>')
