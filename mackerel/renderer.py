from typing import Dict

import mistune
from mistune_contrib import meta


class Renderer:
    def extract_metadata(self, text: str) -> Dict[str, str]:
        raise NotImplementedError

    def extract_text(self, text: str) -> str:
        raise NotImplementedError

    def render(self, text: str) -> str:
        raise NotImplementedError


class MarkdownRenderer(Renderer):
    def __init__(self) -> None:
        self.markdown = mistune.Markdown()

    def extract_metadata(self, text: str) -> Dict[str, str]:
        metadata, _ = meta.parse(text)
        return metadata

    def extract_text(self, text: str) -> str:
        _, text = meta.parse(text)
        return text

    def render(self, text: str) -> str:
        return self.markdown(text)
