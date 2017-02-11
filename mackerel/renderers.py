from typing import Dict, TYPE_CHECKING

import jinja2
import mistune
from mistune_contrib import meta

if TYPE_CHECKING:
    from pathlib import Path
    from mackerel import content


class DocumentRenderer:
    def extract_metadata(self, text: str) -> Dict[str, str]:
        """Extract the metadata from the top of the document and return a
        dictionary with lower cased keys.
        """
        raise NotImplementedError

    def extract_text(self, text: str) -> str:
        raise NotImplementedError

    def render(self, text: str) -> str:
        raise NotImplementedError


class MarkdownRenderer(DocumentRenderer):
    def __init__(self) -> None:
        self.markdown = mistune.Markdown()

    def extract_metadata(self, text: str) -> Dict[str, str]:
        metadata, _ = meta.parse(text)
        return {key.lower(): metadata[key] for key in metadata.keys()}

    def extract_text(self, text: str) -> str:
        _, text = meta.parse(text)
        return text.strip()

    def render(self, text: str) -> str:
        return self.markdown(text)


class TemplateRenderer:
    def render(self, ctx: 'content.Context', doc: 'content.Document') -> str:
        raise NotImplementedError


class Jinja2Renderer(TemplateRenderer):
    def __init__(self, template_dir: 'Path') -> None:
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir.resolve())))

    def render(self, ctx: 'content.Context', doc: 'content.Document') -> str:
        template = self.env.get_template(
            doc.metadata.get('template', doc.default_template))
        return template.render(ctx=ctx, doc=doc)
