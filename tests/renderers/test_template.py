from unittest import mock

from mackerel.renderers import template


class TestJinja2Renderer:
    def test_init(self, site):
        with mock.patch('mackerel.renderers.template.jinja2') as jinja2:
            template.Jinja2Renderer(site=site)
        jinja2.FileSystemLoader.assert_called_with(
            str(site.template_path.resolve()))

        with mock.patch('mackerel.renderers.template.jinja2') as jinja2:
            template.Jinja2Renderer(site=site)
        jinja2.Environment.assert_called_with(
            loader=mock.ANY, lstrip_blocks=True, trim_blocks=True)

    def test_render(self, site, document, context):
        renderer = template.Jinja2Renderer(site=site)
        html = renderer.render(ctx=context, document=document)
        assert '<!DOCTYPE html>' in html
        assert '<a href="/about.html">About</a>' in html
        assert '<h1 class="post-title">About</h1>' in html
