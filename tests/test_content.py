from mackerel import content, renderer


def test_document_init():
    input_content = """Title: Test post
Author: John Doe
Date: December 31, 2099

It's very easy to produce words **bold** and *italic* with Markdown.
You can even [link to Google!](http://google.com)"""
    doc = content.Document(
        content=input_content, renderer=renderer.MarkdownRenderer())

    assert doc.metadata == {
        'Title': 'Test post',
        'Author': 'John Doe',
        'Date': 'December 31, 2099'
    }

    assert doc.text == """
It's very easy to produce words **bold** and *italic* with Markdown.
You can even [link to Google!](http://google.com)"""

    assert doc.html == (
        '<p>It\'s very easy to produce words <strong>bold</strong> and '
        '<em>italic</em> with Markdown.\nYou can even '
        '<a href="http://google.com">link to Google!</a></p>\n')
