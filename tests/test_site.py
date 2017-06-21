from pathlib import Path

from mackerel.renderers import Jinja2Renderer, MarkdownRenderer
from mackerel.site import Site


def test_site_init(site_path):
    site = Site(site_path)
    assert site.config['mackerel']
    assert site.content_path == site_path / Path('content')
    assert site.output_path == site_path / Path('_build')
    assert site.template_path == site_path / Path('template')
    assert len(site.document_files) == 3
    assert len(site.other_content_files) == 1
    assert len(site.other_template_files) == 1
    assert isinstance(site.document_renderer, MarkdownRenderer)
    assert isinstance(site.template_renderer, Jinja2Renderer)
