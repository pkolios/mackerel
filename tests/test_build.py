from pathlib import Path

from mackerel import build
from mackerel.site import Site


def test_build(site):
    test_build = build.Build(site=site)

    assert test_build.site == site

    assert len(test_build.documents) == 3
    assert len(test_build.pages) == 3

    for page in test_build.pages:
        assert page.path
        assert page.content

    for doc in test_build.build_documents:
        assert doc.document
        assert doc.uri

    assert isinstance(test_build.context, build.Context)
    assert isinstance(test_build.site, Site)


def test_build__build_page_path(build, document):
    page_path = build._build_page_path(document)
    assert page_path == build.site.output_path / Path('document.html')


def test_build__build_uri(build, document):
    uri = build._build_uri(document)
    assert uri == '/document.html'


def test_build_execute(build):
    build.execute()
    output_pages = [
        page.relative_to(build.site.output_path)
        for page in build.site.output_path.rglob(
            f"*{build.site.config['mackerel']['OUTPUT_EXT']}")]
    for src_file in build.site.document_files:
        assert src_file.relative_to(
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
    assert build.context.nav
    assert build.context.cfg
