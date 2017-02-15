from unittest import mock

from mackerel import content


def test_document_init(document_content):
    renderer = mock.Mock()
    renderer.extract_metadata.return_value = {'template': 'document.html'}
    doc = content.Document(content=document_content, renderer=renderer)

    renderer.extract_metadata.assert_called_with(text=document_content)
    renderer.extract_text.assert_called_with(text=document_content)
    renderer.render.assert_called_with(doc.text)

    assert doc.template == 'document.html'
    assert renderer.extract_metadata() == doc.metadata
    assert renderer.extract_text() == doc.text
    assert renderer.render() == doc.html


def test_source_init(source_path):
    src = content.Source(source_path)
    assert src.doc_ext == '.md'
    assert len(src.docs) == 3
    assert len(src.other_files) == 1


def test_build(source, output_path, markdown_renderer, jinja2renderer):
    build = content.Build(
        source=source, output_dir=output_path,
        document_renderer=markdown_renderer, template_renderer=jinja2renderer)
    # TODO: Expand the assertions
    assert len(build.documents) == 3
    assert len(build.pages) == 3
