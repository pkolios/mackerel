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
    assert doc.checksum == '960d1eea96bf8d50547d917b768ed964077c1e1f'
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


def test_document_excerpt(document):
    assert document.excerpt(width=1) == '...'
    assert document.excerpt(width=4, placeholder='... more') == 'This... more'
    assert document.excerpt() == document.excerpt(0) == (
        'This is a demo site for Mackerel, it contains dummy content which '
        'allows you to click around and see what a Mackerel blog running '
        'Ghost\'s Casper theme...')
