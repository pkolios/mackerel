from typing import Dict, TYPE_CHECKING

import jinja2
import mistune
from markupsafe import Markup
from mistune_contrib import meta

if TYPE_CHECKING:
    from mackerel import build, content  # noqa
    from mackerel.site import Site  # noqa
    from pathlib import Path  # noqa


class DocumentRenderer:
    def __init__(self, site: 'Site') -> None:
        raise NotImplementedError

    def extract_metadata(self, text: str) -> Dict[str, str]:
        """
        Extract the metadata from the top of the document and return a
        dictionary with lower cased keys.
        """
        raise NotImplementedError

    def extract_text(self, text: str) -> str:
        """Extract the text that follows the metadata of the document."""
        raise NotImplementedError

    def strip_tags(self, text: str) -> str:
        """Strip the html tags of the given string."""
        raise NotImplementedError

    def render(self, text: str) -> str:
        raise NotImplementedError


class MarkdownRenderer(DocumentRenderer):
    def __init__(self, site: 'Site') -> None:
        self.markdown = mistune.Markdown()

    def extract_metadata(self, text: str) -> Dict[str, str]:
        metadata, _ = meta.parse(text)
        return {key.lower(): metadata[key] for key in metadata.keys()}

    def extract_text(self, text: str) -> str:
        _, text = meta.parse(text)
        return text.strip()

    def strip_tags(self, text: str) -> str:
        return Markup(text).striptags()

    def render(self, text: str) -> str:
        return self.markdown(text)


class TemplateRenderer:
    def __init__(self, site: 'Site') -> None:
        raise NotImplementedError

    def render(self, ctx: 'build.Context',
               document: 'content.Document') -> str:
        raise NotImplementedError


class Jinja2Renderer(TemplateRenderer):
    def __init__(self, site: 'Site') -> None:
        template_path = site.template_path  # Type: Path
        trim_blocks = site.config.getboolean('Jinja2Renderer', 'TRIM_BLOCKS')
        lstrip_blocks = site.config.getboolean(
            'Jinja2Renderer', 'LSTRIP_BLOCKS')
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_path.resolve())),
            trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks,)

    def render(self, ctx: 'build.Context',
               document: 'content.Document') -> str:
        template = self.env.get_template(document.template)
        return template.render(ctx=ctx, document=document)
