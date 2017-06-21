from pathlib import Path

from mackerel import build


def test_build(source, output_path, markdown_renderer, jinja2renderer):
    test_build = build.Build(
        source=source, document_renderer=markdown_renderer,
        template_renderer=jinja2renderer)

    assert test_build.source == source

    assert test_build.document_renderer == markdown_renderer
    assert test_build.template_renderer == jinja2renderer
    assert len(test_build.documents) == 3
    assert len(test_build.pages) == 3

    for page in test_build.pages:
        assert page.path
        assert page.content

    for doc in test_build.build_documents:
        assert doc.document
        assert doc.uri

    assert isinstance(test_build.context, build.Context)


def test_build__build_page_path(build, document):
    page_path = build._build_page_path(document)
    assert page_path == build.source.output_path / Path('document.html')


def test_build__build_uri(build, document):
    uri = build._build_uri(document)
    assert uri == '/document.html'


def test_build_execute(build):
    build.execute()
    output_pages = [
        page.relative_to(build.source.output_path)
        for page in build.source.output_path.rglob(
            f'*{build.source.output_ext}')]
    for src_file in build.source.document_files:
        assert src_file.relative_to(
            build.source.content_path).with_suffix(
                build.source.output_ext) in output_pages

    for other_file in build.source.other_content_files:
        rel_of = other_file.relative_to(build.source.content_path)
        assert (build.source.output_path / rel_of).is_file()

    for template_file in build.source.other_template_files:
        rel_tf = template_file.relative_to(build.source.template_path)
        assert (build.source.output_path / rel_tf).is_file()


def test_build_execute_dry_run(build):
    build.execute(dry_run=True)
    output_pages = [
        page for page in build.source.content_path.rglob(
            f'*{build.source.output_ext}')]
    assert len(output_pages) == 0


def test_build_context(build):
    assert build.context.nav
    assert build.context.cfg


def test_navigation(build_documents):
    nav = build.Navigation(build_documents)
    assert nav._build_documents == build_documents


def test_navigation_nodes(build_documents):
    nav = build.Navigation(build_documents)
    nodes = nav.nodes
    assert len(nodes) == len(build_documents)
    uris = [doc.uri for doc in build_documents]
    for node in nodes:
        assert node.is_file is True
        assert node.is_dir is False
        assert node.uri in uris
