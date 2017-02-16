from unittest import mock

import pytest

from mackerel import content


def test_document_init(document_content):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    doc = content.Document(content=document_content, renderer=renderer)

    renderer.extract_metadata.assert_called_with(text=document_content)
    renderer.extract_text.assert_called_with(text=document_content)
    renderer.render.assert_called_with(doc.text)

    assert doc.checksum == '6a9fa1fce2e95979cbbb5b949ad0f3a2810af133'
    assert doc.template == 'document.html'
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.extract_text() == doc.text
    assert renderer.render() == doc.html


def test_document_eq(document_content):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    doc1 = content.Document(content=document_content, renderer=renderer)
    doc2 = content.Document(content=document_content, renderer=renderer)

    assert doc1 == doc2


def test_source_init(source_path):
    src = content.Source(source_path)
    assert src.doc_ext == '.md'
    assert len(src.docs) == 3
    assert len(src.other_files) == 1


def test_build(source, output_path, markdown_renderer, jinja2renderer):
    build = content.Build(
        source=source, output_dir=output_path,
        document_renderer=markdown_renderer, template_renderer=jinja2renderer)

    assert len(build.documents) == 3
    assert len(build.pages) == 3

    for doc in build.documents:
        for key in ('path', 'document'):
            assert key in doc

    for page in build.pages:
        for key in ('title', 'metadata', 'uri', 'body'):
            assert key in page


def test_build_missing_title(build, document, document_path):
    document.metadata.pop('title')
    build._cached_documents = (dict(path=document_path, document=document),)
    with pytest.raises(KeyError) as excinfo:
        build.pages
    assert str(document_path) in str(excinfo.value)
    assert 'missing a title' in str(excinfo.value)


def test_build__build_uri(build, document, document_path):
    doc = dict(path=document_path, document=document)
    uri = build._build_uri(doc)
    assert uri == '/{}.html'.format(document_path.stem)
