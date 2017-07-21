from typing import Dict, TYPE_CHECKING

import markdown
import mistune
from mistune_contrib import meta

from mackerel.renderers.base import DocumentRenderer

if TYPE_CHECKING:
    from mackerel.site import Site  # noqa


class MistuneMarkdownRenderer(DocumentRenderer):
    def __init__(self, site: 'Site') -> None:
        self.markdown = mistune.Markdown()

    def extract_metadata(self, text: str) -> Dict[str, str]:
        metadata, _ = meta.parse(text)
        return {key.lower(): metadata[key] for key in metadata.keys()}

    def render(self, text: str) -> str:
        _, text = meta.parse(text)
        return self.markdown(text.strip())


class MarkdownMarkdownRenderer(DocumentRenderer):
    def __init__(self, site: 'Site') -> None:
        ext_list = site.config.get(
            'MarkdownMarkdownRenderer', 'extensions', fallback=None)
        extensions = tuple(
            item.strip() for item in ext_list.split(',') if ext_list)
        output_format = site.config.get(
            'MarkdownMarkdownRenderer', 'OUTPUT_FORMAT')
        self.markdown = markdown.Markdown(
            extensions=extensions, output_format=output_format)

    def extract_metadata(self, text: str) -> Dict[str, str]:
        self.render(text)
        for key in self.markdown.Meta:
            if len(self.markdown.Meta[key]) == 1:
                self.markdown.Meta[key] = self.markdown.Meta[key][0]
        return self.markdown.Meta

    def render(self, text: str) -> str:
        self.markdown.reset()
        return self.markdown.convert(text)
