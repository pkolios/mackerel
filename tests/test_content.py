from unittest import mock

import pytest

from mackerel import content


def test_document_init(document_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {
        'template': 'document.html', 'title': 'Test post'}
    doc = content.Document(document_path=document_path, renderer=renderer)

    renderer.extract_metadata.assert_called_with(text=doc.content)
    renderer.extract_text.assert_called_with(text=doc.content)
    renderer.render.assert_called_with(doc.text)

    assert doc.document_path == document_path
    assert doc.checksum == '25a3bb324f875a8c72562970ab28df8dffdf48bd'
    assert doc.template == 'document.html'
    assert doc.title == 'Test post'
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.extract_text() == doc.text
    assert renderer.render() == doc.html


def test_document_eq(document_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {
        'template': 'document.html', 'title': 'Test post'}
    doc1 = content.Document(document_path=document_path, renderer=renderer)
    doc2 = content.Document(document_path=document_path, renderer=renderer)

    assert doc1 == doc2


def test_document_missing_title(document_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    with pytest.raises(KeyError) as excinfo:
        content.Document(document_path=document_path, renderer=renderer)

    assert 'missing a title' in str(excinfo.value)
