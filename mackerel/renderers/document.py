from typing import Dict, TYPE_CHECKING

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

    def extract_text(self, text: str) -> str:
        _, text = meta.parse(text)
        return text.strip()

    def render(self, text: str) -> str:
        return self.markdown(text)
