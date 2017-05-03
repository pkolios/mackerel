from pathlib import Path

from mackerel import build


def test_build(source, output_path, markdown_renderer, jinja2renderer):
    test_build = build.Build(
        source=source, output_path=output_path,
        document_renderer=markdown_renderer, template_renderer=jinja2renderer)

    assert test_build.source == source
    assert test_build.output_path == output_path

    assert test_build.document_renderer == markdown_renderer
    assert test_build.template_renderer == jinja2renderer
    assert test_build.output_ext == '.html'
    assert len(test_build.documents) == 3
    assert len(test_build.pages) == 3

    for page in test_build.pages:
        assert page.path
        assert page.content

    for doc in test_build.build_documents:
        assert doc.document
        assert doc.uri

    assert isinstance(test_build.context, build.Context)


def test_build__build_page_path(build, document, output_path):
    page_path = build._build_page_path(document, output_path)
    assert page_path == output_path / Path('document.html')


def test_build__build_uri(build, document):
    uri = build._build_uri(document)
    assert uri == '/document.html'