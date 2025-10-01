"""Tests for the renderers module."""

import textwrap
from pathlib import Path

from mackerel import types as t
from mackerel.config import Jinja2RendererConfig
from mackerel.config import MarkdownRendererConfig
from mackerel.renderers import Jinja2Renderer
from mackerel.renderers import MarkdownRenderer


def test_markdown_renderer() -> None:
    """Test the MarkdownRenderer."""
    cfg = MarkdownRendererConfig(
        output_format="html",
        extensions=["markdown.extensions.meta", "markdown.extensions.extra"],
    )
    renderer = MarkdownRenderer(cfg)
    raw = textwrap.dedent("""\
    ---
    title: Test Document
    ---

    # Test Document

    This is the content of the document.
    """)
    rendered_content = renderer.render(raw)
    assert (
        rendered_content
        == "<h1>Test Document</h1>\n<p>This is the content of the document.</p>"
    )


def test_jinja2_renderer(tmp_path: Path) -> None:
    """Test the Jinja2Renderer."""
    # Create a simple Jinja2 template for testing
    test_template = textwrap.dedent("""\
    <!doctype html><meta charset=utf-8><title></title>{{document.html|safe}}
    """)
    template_path = t.TemplatePath(Path(tmp_path / "templates"))
    template_path.mkdir(parents=True, exist_ok=True)
    test_template_path = template_path / "test_template.html"
    test_template_path.write_text(test_template)

    # Initialize the Jinja2 renderer with the template path
    cfg = Jinja2RendererConfig()
    renderer = Jinja2Renderer(
        template_path=template_path,
        template_suffix=t.TemplateSuffix(".html"),
        cfg=cfg,
    )
    ctx = t.TemplateContext(user=t.UserConfig({}))

    # Create a RenderedDocument with metadata and content
    metadata = t.DocumentMetadata(
        title=t.Title("Test Document"),
        template=Path("test_template.html"),
    )
    document = t.RenderedDocument(
        url=t.RelativeURL("/test-document.html"),
        html=t.HTML("<h1>Test Document</h1>"),
        metadata=metadata,
    )

    # Render the document using the Jinja2 renderer
    rendered_html = renderer.render(ctx, document)

    # Assert the rendered HTML matches the expected output
    expected_html = (
        "<!doctype html><meta charset=utf-8><title></title><h1>Test Document</h1>"
    )
    assert rendered_html == t.HTML(expected_html)
