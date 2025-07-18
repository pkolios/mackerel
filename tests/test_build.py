"""Tests for the build module."""

from pathlib import Path

import pytest

from mackerel import types as t
from mackerel.build import build
from mackerel.build import copy_static_file
from mackerel.build import create_category_items
from mackerel.build import fetch_content_files
from mackerel.build import fetch_template_assets
from mackerel.build import read_document
from mackerel.build import write_documents
from mackerel.config import AppConfig
from mackerel.config import MackerelConfig


class MockContentRenderer(t.ContentRenderer):
    """A simple content renderer for testing purposes."""

    def render(self, raw: str) -> t.HTML:
        """Render the content by wrapping it in HTML tags."""
        return t.HTML(f"<span>{raw}</span>")


class MockMetadataParser(t.MetadataParser):
    """A simple metadata parser for testing purposes."""

    def parse(self, raw: str) -> t.DocumentMetadata:
        """Parse metadata from a static file (no-op for this test)."""
        return t.DocumentMetadata(
            title=t.Title("Test Document"),
            template=Path("default.html"),
        )


class MockTemplateRenderer(t.TemplateRenderer):
    """A simple template renderer for testing purposes."""

    def render(self, ctx: t.TemplateContext, document: t.RenderedDocument) -> t.HTML:
        """Render the content with metadata using a simple template."""
        return t.HTML(
            f"<html><head><title>{document.metadata.title}</title></head>"
            f"<body>{document.html}</body></html>",
        )


@pytest.mark.parametrize(
    ("relative_dir", "expected_content", "dry_run"),
    [
        (None, "This is a static file.", False),
        ("subdir", "This is a static file in a subdirectory.", False),
        (None, "This is a static file.", True),
        ("subdir", "This is a static file in a subdirectory.", True),
    ],
    ids=[
        "no_subdir",
        "with_subdir",
        "no_subdir_dry_run",
        "with_subdir_dry_run",
    ],
)
def test_copy_static(
    tmp_path: Path,
    relative_dir: str | None,
    expected_content: str,
    dry_run: bool,
) -> None:
    """Ensure the function copies static files correctly."""
    content_path = tmp_path
    build_path = tmp_path / "build"

    static_dir = content_path / relative_dir if relative_dir else content_path
    static_dir.mkdir(parents=True, exist_ok=True)

    file_path = static_dir / "static.txt"
    file_path.write_text(expected_content)

    copy_static_file(
        f=t.StaticFile(file_path),
        relative_path=t.ContentPath(content_path),
        build_path=t.BuildPath(build_path),
        dry_run=dry_run,
    )

    expected_path = build_path / file_path.relative_to(content_path)
    assert (dry_run and not expected_path.exists()) or (
        not dry_run and expected_path.exists()
    )
    if not dry_run:
        assert expected_path.read_text() == expected_content


@pytest.mark.parametrize(
    ("relative_dir", "expected_heading"),
    [
        (None, "# Heading"),
        ("subdir", "# Heading in subdir"),
    ],
    ids=["no_subdir", "with_subdir"],
)
def test_read_document(
    tmp_path: Path,
    relative_dir: str | None,
    expected_heading: str,
) -> None:
    """Ensure function reads document files correctly."""
    content_path = tmp_path
    build_path = tmp_path / "build"

    doc_dir = content_path / relative_dir if relative_dir else content_path
    doc_dir.mkdir(parents=True, exist_ok=True)

    file_path = doc_dir / "document.md"
    file_path.write_text(expected_heading)

    cfg = AppConfig(
        mackerel=MackerelConfig(
            build_path=t.BuildPath(build_path),
            content_path=t.ContentPath(content_path),
            template_path=t.TemplatePath(tmp_path / "templates"),
        ),
    )

    target_path, doc = read_document(
        f=t.DocumentFile(file_path),
        cfg=cfg,
        content_renderer=MockContentRenderer(),
        metadata_parser=MockMetadataParser(),
    )
    assert target_path == build_path / file_path.relative_to(content_path).with_suffix(
        ".html",
    )
    assert isinstance(doc, t.RenderedDocument)
    assert doc.metadata.title == t.Title("Test Document")
    assert doc.html == t.HTML(f"<span>{expected_heading}</span>")


@pytest.mark.parametrize("dry_run", [True, False], ids=["dry_run", "not_dry_run"])
def test_write_documents(tmp_path: Path, dry_run: bool) -> None:
    """Test the write_documents function."""
    content_path = tmp_path
    build_path = t.BuildPath(tmp_path / "build")

    cfg = AppConfig(
        mackerel=MackerelConfig(
            build_path=t.BuildPath(build_path),
            content_path=t.ContentPath(content_path),
            template_path=t.TemplatePath(tmp_path / "templates"),
        ),
    )
    docs = {
        build_path / "doc1.html": t.RenderedDocument(
            url=t.RelativeURL("/doc1.html"),
            metadata=t.DocumentMetadata(
                title=t.Title("Doc 1"),
                template=Path("default.html"),
            ),
            html=t.HTML("<p>Content of Doc 1</p>"),
        ),
        build_path / "subdir" / "doc2.html": t.RenderedDocument(
            url=t.RelativeURL("/subdir/doc2.html"),
            metadata=t.DocumentMetadata(
                title=t.Title("Doc 2"),
                template=Path("default.html"),
            ),
            html=t.HTML("<p>Content of Doc 2</p>"),
        ),
        build_path / "wip.html": t.RenderedDocument(
            url=t.RelativeURL("/wip.html"),
            metadata=t.DocumentMetadata(
                title=t.Title("wip"),
                template=Path("default.html"),
                draft=True,
            ),
            html=t.HTML("<p>wip</p>"),
        ),
    }
    write_documents(
        docs=docs,
        cfg=cfg,
        template_renderer=MockTemplateRenderer(),
        dry_run=dry_run,
    )

    expected_docs = {k: v for k, v in docs.items() if not v.metadata.draft}
    build_files = [f for f in build_path.glob("**/*") if f.is_file()]
    assert len(build_files) == (0 if dry_run else len(expected_docs))

    for target_path, doc in expected_docs.items():
        assert (dry_run and not target_path.exists()) or (
            not dry_run and target_path.exists()
        )
        if not dry_run:
            expected_html = (
                f"<html><head><title>{doc.metadata.title}</title></head>"
                f"<body>{doc.html}</body></html>"
            )
            assert target_path.read_text() == expected_html


def test_fetch_content_files(tmp_path: Path) -> None:
    """Test the fetch_content_files function."""
    content_path = tmp_path
    doc_file = content_path / "doc.md"
    doc_file.write_text("# Document")
    static_file = content_path / "static.txt"
    static_file.write_text("Static content")
    files = list(
        fetch_content_files(
            content_path=t.ContentPath(content_path),
            doc_suffix=t.DocSuffix(".md"),
        ),
    )
    assert len(files) == 2
    assert {type(f) for f in files} == {t.DocumentFile, t.StaticFile}
    assert {Path(f) for f in files} == {doc_file, static_file}


def test_fetch_content_files_empty(tmp_path: Path) -> None:
    """Test fetch_content_files with an empty directory."""
    content_path = tmp_path
    files = list(
        fetch_content_files(
            content_path=t.ContentPath(content_path),
            doc_suffix=t.DocSuffix(".md"),
        ),
    )
    # Expect no files to be found in an empty directory
    assert files == []


def test_fetch_template_assets(tmp_path: Path) -> None:
    """Test the fetch_template_assets function."""
    template_path = tmp_path / "templates"
    template_path.mkdir(parents=True, exist_ok=True)
    template_asset = template_path / "assets/asset.css"
    template_asset.parent.mkdir(parents=True, exist_ok=True)
    template_asset.write_text("body { background: #fff; }")
    files = list(
        fetch_template_assets(
            template_path=t.TemplatePath(template_path),
            template_suffix=t.TemplateSuffix(".html"),
        ),
    )
    assert len(files) == 1
    assert isinstance(files[0], t.TemplateAsset)
    assert files[0] == template_asset


def test_create_category_items_sorting_and_caching() -> None:
    """Test create_category_items with sorting and caching behavior."""
    # Create 3 rendered documents with different metadata
    doc1 = t.RenderedDocument(
        url=t.RelativeURL("/alpha.html"),
        html=t.HTML("<p>Alpha</p>"),
        metadata=t.DocumentMetadata(
            title=t.Title("Alpha"),
            template=Path("default.html"),
            created_at=t.CreatedAt("2024-01-01T10:00:00"),
            categories=[t.Category("blog")],
        ),
    )
    doc2 = t.RenderedDocument(
        url=t.RelativeURL("/beta.html"),
        html=t.HTML("<p>Beta</p>"),
        metadata=t.DocumentMetadata(
            title=t.Title("Beta"),
            template=Path("default.html"),
            created_at=t.CreatedAt("2024-02-01T10:00:00"),
            categories=[t.Category("blog")],
        ),
    )
    doc3 = t.RenderedDocument(
        url=t.RelativeURL("/gamma.html"),
        html=t.HTML("<p>Gamma</p>"),
        metadata=t.DocumentMetadata(
            title=t.Title("Gamma"),
            template=Path("default.html"),
            created_at=t.CreatedAt("2024-03-01T10:00:00"),
            categories=[t.Category("news")],  # Different category
        ),
    )

    # Build path keys are arbitrary here, only keys in the dict
    docs: dict[t.BuildPath, t.RenderedDocument] = {
        t.BuildPath(Path(f"{name}.html")): doc
        for name, doc in [("doc1", doc1), ("doc2", doc2), ("doc3", doc3)]
    }

    # Define a category list that targets "blog" and sorts by created_at
    category_list = t.CategoryList(
        name=t.Category("blog"),
        sort_by="created_at",
        order="desc",
    )

    result = create_category_items(category_list, docs)

    # Check that only doc2 and doc1 appear, and in descending order
    assert isinstance(result, t.BuildCategoryList)
    assert [doc.metadata.title for doc in result.items] == [
        t.Title("Beta"),
        t.Title("Alpha"),
    ]

    # Call again to ensure it's cached and returns same result
    result_cached = create_category_items(category_list, docs)
    assert result is result_cached  # Identity check confirms caching


@pytest.mark.parametrize("dry_run", [True, False], ids=["dry_run", "not_dry_run"])
def test_build(tmp_path: Path, dry_run: bool) -> None:
    """Test the build function with a simple configuration."""
    cfg = AppConfig(
        mackerel=MackerelConfig(
            build_path=t.BuildPath(tmp_path / "build"),
            content_path=t.ContentPath(tmp_path / "content"),
            template_path=t.TemplatePath(tmp_path / "templates"),
        ),
    )
    doc = tmp_path / "content" / "document.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Test Document")
    static_file = tmp_path / "content/static.txt"
    static_file.parent.mkdir(parents=True, exist_ok=True)
    static_file.write_text("This is a static file.")
    asset_file = tmp_path / "templates/assets/asset.css"
    asset_file.parent.mkdir(parents=True, exist_ok=True)
    asset_file.write_text("body { background: #fff; }")

    # Run the build process
    build(
        cfg=cfg,
        content_renderer=MockContentRenderer(),
        metadata_parser=MockMetadataParser(),
        template_renderer=MockTemplateRenderer(),
        dry_run=dry_run,
    )

    # Check if the document was processed correctly
    if not dry_run:
        expected_doc_path = cfg.mackerel.build_path / "document.html"
        assert expected_doc_path.exists()
        assert expected_doc_path.read_text() == (
            "<html><head><title>Test Document</title></head>"
            "<body><span># Test Document</span></body></html>"
        )
        # Check if the static file was copied correctly
        expected_static_path = cfg.mackerel.build_path / "static.txt"
        assert expected_static_path.exists()
        assert expected_static_path.read_text() == "This is a static file."
        # Check if the template asset was copied correctly
        expected_asset_path = cfg.mackerel.build_path / "assets/asset.css"
        assert expected_asset_path.exists()
        assert expected_asset_path.read_text() == "body { background: #fff; }"
    else:
        # In dry run, no files should be created
        assert not (cfg.mackerel.build_path / "document.html").exists()
        assert not (cfg.mackerel.build_path / "static.txt").exists()
        assert not (cfg.mackerel.build_path / "assets/asset.css").exists()
