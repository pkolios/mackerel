"""A module for all provided renderers."""

from dataclasses import asdict

import jinja2
import markdown

from mackerel import types as t
from mackerel.config import Jinja2RendererConfig
from mackerel.config import MarkdownRendererConfig


class MarkdownRenderer(t.ContentRenderer):
    """Markdown-based content renderer."""

    def __init__(self, cfg: MarkdownRendererConfig) -> None:
        """Initialize the Markdown renderer with the given configuration."""
        self.md = markdown.Markdown(**asdict(cfg))

    def render(self, raw: str) -> t.HTML:
        """Render the raw Markdown content into HTML."""
        html = self.md.reset().convert(raw)
        return t.HTML(html)


class Jinja2Renderer(t.TemplateRenderer):
    """Jinja2-based template renderer."""

    def __init__(
        self,
        template_path: t.TemplatePath,
        template_suffix: t.TemplateSuffix,
        cfg: Jinja2RendererConfig,
    ) -> None:
        """Initialize the Jinja2 env."""
        self.template_suffix = template_suffix
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            autoescape=jinja2.select_autoescape(enabled_extensions=()),
            **asdict(cfg),
        )

    def render(self, ctx: t.TemplateContext, document: t.RenderedDocument) -> t.HTML:
        """Render the document using the Jinja2 template."""
        template = self.env.get_template(
            str(document.metadata.template.with_suffix(self.template_suffix))
        )
        return t.HTML(template.render(ctx=ctx, document=document))
