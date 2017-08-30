from pathlib import Path
from unittest import mock

import pytest

from mackerel import content, exceptions


@pytest.yield_fixture
def document_path():
    yield Path('/tmp/mackerel/test/content/document.md')


@pytest.yield_fixture
def content_path():
    yield Path('/tmp/mackerel/test/content')


@pytest.yield_fixture
def renderer():
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {
        'template': 'document.html', 'title': 'Test post'}
    yield renderer


def test_document_init(document_path, content_path, renderer):
    with mock.patch('pathlib.Path.read_text') as read_mock:
        doc = content.Document(document_path=document_path,
                               content_path=content_path, renderer=renderer)

    read_mock.assert_called_once_with()

    renderer.extract_metadata.assert_called_with(text=doc.content)
    renderer.render.assert_called_with(doc.content)

    assert doc.document_path == document_path
    assert doc.relative_path == Path('document.md')
    assert doc.template == 'document.html'
    assert doc.title == 'Test post'
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.render() == doc.html


def test_document_eq(document_path, content_path, renderer):
    with mock.patch('pathlib.Path.read_text') as read_mock:
        doc1 = content.Document(document_path=document_path,
                                content_path=content_path, renderer=renderer)
        doc2 = content.Document(document_path=document_path,
                                content_path=content_path, renderer=renderer)

    assert read_mock.call_count == 2
    assert doc1 == doc2
    assert doc1 != 'some_string'


def test_document_missing_title(document_path, content_path, renderer):
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    with mock.patch('pathlib.Path.read_text'):
        with pytest.raises(exceptions.DocumentError) as excinfo:
            content.Document(document_path=document_path,
                             content_path=content_path, renderer=renderer)

    assert f'Document `{str(document_path)}` is missing a title' in str(
        excinfo.value)


def test_document_excerpt(document_path, content_path, renderer):
    with mock.patch('pathlib.Path.read_text'):
        doc = content.Document(document_path=document_path,
                               content_path=content_path, renderer=renderer)
    doc.html = (
        'Tales without end are told of these massive, lonely figures who bore '
        'half-seriously, half-mockingly a motto adopted from one of Salvor '
        'Hardin\'s epigrams, "Never let your sense of morals prevent you from '
        'doing what is right!"')

    assert doc.excerpt(width=1) == '...'
    assert doc.excerpt(width=5, placeholder='... more') == 'Tales... more'
    assert doc.excerpt() == doc.excerpt(0) == (
        'Tales without end are told of these massive, lonely figures who bore '
        'half-seriously, half-mockingly a motto adopted from one of Salvor '
        'Hardin\'s...')
