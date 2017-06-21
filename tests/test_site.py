from pathlib import Path

from mackerel.site import Site


def test_site_init(site_path):
    src = Site(site_path)
    assert src.config['mackerel']
    assert src.content_path == site_path / Path('content')
    assert src.output_path == site_path / Path('_build')
    assert src.template_path == site_path / Path('template')
    assert src.output_ext == '.html'
    assert src.doc_ext == '.md'
    assert len(src.document_files) == 3
    assert len(src.other_content_files) == 1
    assert len(src.other_template_files) == 1
