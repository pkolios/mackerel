from pathlib import Path
from unittest import mock

import pytest

from mackerel import content, exceptions


def test_document_init(document_path, content_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {
        'template': 'document.html', 'title': 'Test post'}
    doc = content.Document(document_path=document_path,
                           content_path=content_path, renderer=renderer)

    renderer.extract_metadata.assert_called_with(text=doc.content)
    renderer.render.assert_called_with(doc.content)

    assert doc.document_path == document_path
    assert doc.relative_path == Path('about.md')
    assert doc.template == 'document.html'
    assert doc.title == 'Test post'
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.render() == doc.html


def test_document_eq(document_path, content_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {
        'template': 'document.html', 'title': 'Test post'}
    doc1 = content.Document(document_path=document_path,
                            content_path=content_path, renderer=renderer)
    doc2 = content.Document(document_path=document_path,
                            content_path=content_path, renderer=renderer)

    assert doc1 == doc2
    assert doc1 != 'some_string'


def test_document_missing_title(document_path, content_path):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    with pytest.raises(exceptions.DocumentError) as excinfo:
        content.Document(document_path=document_path,
                         content_path=content_path, renderer=renderer)

    assert f'Document `{str(document_path)}` is missing a title' in str(
        excinfo.value)


def test_document_excerpt(document):
    assert document.excerpt(width=1) == '...'
    assert document.excerpt(width=4, placeholder='... more') == 'This... more'
    assert document.excerpt() == document.excerpt(0) == (
        'This is a demo site for Mackerel, it contains dummy content which '
        'allows you to click around and see what a Mackerel blog running '
        'Ghost\'s Casper theme...')
