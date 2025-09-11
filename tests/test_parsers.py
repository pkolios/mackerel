"""Tests for the parsers module."""

import textwrap
from pathlib import Path

from mackerel import types as t
from mackerel.parsers import PythonFrontmatterParser


def test_python_frontmatter_parser() -> None:
    """Test the PythonFrontmatterParser."""
    parser = PythonFrontmatterParser()
    raw = textwrap.dedent("""\
    ---
    title: Test Document
    template: default
    created_at: 2023-10-01 12:00:00
    modified_at: 2023-10-02 12:00:00
    draft: false
    categories:
      - test
      - example
    category_lists:
      - name: example
        sort_by: title
        order: asc
    ---

    This is the content of the document.
    """)
    metadata = parser.parse(raw)
    assert metadata.title == "Test Document"
    assert metadata.template == Path("default")
    assert metadata.created_at == t.CreatedAt("2023-10-01 12:00:00")
    assert metadata.modified_at == t.ModifiedAt("2023-10-02 12:00:00")
    assert metadata.categories == [t.Category("test"), t.Category("example")]
    assert metadata.category_lists == [
        t.CategoryList(
            name=t.Category("example"),
            sort_by="title",
            order="asc",
        ),
    ]
    assert not metadata.draft


def test_python_frontmatter_parser_missing_fields() -> None:
    """Test the PythonFrontmatterParser with missing fields."""
    parser = PythonFrontmatterParser()
    raw = textwrap.dedent("""\
    ---
    title: Test Document
    template: default
    ---
    This is the content of the document.
    """)
    metadata = parser.parse(raw)
    assert metadata.title == "Test Document"
    assert metadata.template == Path("default")
    assert metadata.created_at is None
    assert metadata.modified_at is None
    assert metadata.categories == []
    assert metadata.category_lists == []
    assert not metadata.draft
