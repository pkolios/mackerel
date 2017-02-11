from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mackerel.renderers import DocumentRenderer


class Context:
    """Context contains data that is relevant for all documents"""


class Document:
    default_template = None  # type: str

    def __init__(self, content: str, renderer: 'DocumentRenderer') -> None:
        self.metadata = renderer.extract_metadata(text=content)  # type: Dict[str, str]
        self.text = renderer.extract_text(text=content)  # type: str
        self.html = renderer.render(self.text)  # type: str
