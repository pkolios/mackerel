from unittest import mock

from mackerel import content


def test_document_init(document_content):
    renderer = mock.Mock()
    doc = content.Document(content=document_content, renderer=renderer)

    renderer.extract_metadata.assert_called_with(text=document_content)
    renderer.extract_text.assert_called_with(text=document_content)
    renderer.render.assert_called_with(doc.text)

    assert doc.default_template is None
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.extract_text() == doc.text
    assert renderer.render() == doc.html
