from typing import Dict

from mackerel.renderer import Renderer


class Document:
    def __init__(self, content: str, renderer: Renderer) -> None:
        self.metadata = renderer.extract_metadata(text=content)  # type: Dict[str, str]
        self.text = renderer.extract_text(text=content)  # type: str
        self.html = renderer.render(self.text)  # type: str
