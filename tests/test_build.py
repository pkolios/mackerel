from pathlib import Path
from unittest import mock

from mackerel import build
from mackerel.site import Site


def test_build(site):
    test_build = build.Build(site=site)

    assert test_build.site == site

    assert len(test_build.pages) == 5

    for page in test_build.pages:
        assert page.path
        assert page.content

    assert isinstance(test_build.context, build.Context)
    assert isinstance(test_build.site, Site)


def test_build_absolute_page_output_path(build, document):
    page_path = build._absolute_page_output_path(document)
    assert page_path == build.site.output_path / Path('about.html')


def test_build_execute(build):
    build.execute()
    output_pages = [
        page.relative_to(build.site.output_path)
        for page in build.site.output_path.rglob(
            f"*{build.site.config['mackerel']['OUTPUT_EXT']}")]
    for doc in build.site.documents:
        if doc.title == 'Unknown Template':
            continue
        assert doc.document_path.relative_to(
            build.site.content_path).with_suffix(
                build.site.config['mackerel']['OUTPUT_EXT']) in output_pages

    for other_file in build.site.other_content_files:
        rel_of = other_file.relative_to(build.site.content_path)
        assert (build.site.output_path / rel_of).is_file()

    for template_file in build.site.other_template_files:
        rel_tf = template_file.relative_to(build.site.template_path)
        assert (build.site.output_path / rel_tf).is_file()


def test_build_execute_dry_run(build):
    build.execute(dry_run=True)
    output_pages = [
        page for page in build.site.content_path.rglob(
            f"*{build.site.config['mackerel']['OUTPUT_EXT']}")]
    assert len(output_pages) == 0


def test_build_context(build):
    # TODO: Test something more meaningful
    assert build.context.nav
    assert build.context.cfg


def test_context_url_for(build):
    assert build.context.url_for('css/style.css') == '/css/style.css'
    assert build.context.url_for('app.js') == '/app.js'
    assert build.context.url_for(
        'app.js', external=True) == 'http://localhost:8000/app.js'

    with mock.patch.dict(build.context.cfg,
                         {'user': {'url': 'http://test/blog/'}}):
        assert build.context.url_for('css/style.css') == '/blog/css/style.css'
        assert build.context.url_for('app.js') == '/blog/app.js'
