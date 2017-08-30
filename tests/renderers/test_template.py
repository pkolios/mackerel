from unittest import mock

import pytest

from mackerel import exceptions
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

    def test_render(self, site, document_mocks):
        document = document_mocks.create(template='path/to/template')
        context = mock.Mock('context')

        renderer = template.Jinja2Renderer(site=site)
        render_func = mock.Mock()
        renderer.env.get_template = mock.Mock(
            return_value=mock.Mock(render=render_func))

        renderer.render(ctx=context, document=document)

        renderer.env.get_template.assert_called_once_with(document.template)
        render_func.assert_called_once_with(ctx=context, document=document)

    def test_render_template_not_found(self, site):
        document = mock.Mock('document')
        document.template = '/tmp/wrong/path/wrong_template.html'
        document.document_path = '/tmp/some/document/path.md'
        context = mock.Mock('context')

        renderer = template.Jinja2Renderer(site=site)

        with pytest.raises(exceptions.RenderingError) as excinfo:
            renderer.render(ctx=context, document=document)

        assert (f'Template file `{document.template}` for document '
                f'`{document.document_path}` not found') in str(excinfo.value)
