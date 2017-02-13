from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from mackerel.renderers import DocumentRenderer


class Context:
    """Context contains data that is relevant for all documents"""


class Document:
    def __init__(self, content: str, renderer: 'DocumentRenderer') -> None:
        self.metadata = renderer.extract_metadata(text=content)  # type: Dict[str, str]
        self.template = self.metadata.get('template', 'post.html')  # type: str
        self.text = renderer.extract_text(text=content)  # type: str
        self.html = renderer.render(self.text)  # type: str


class Source:
    def __init__(self, path: 'Path', doc_ext: str = '.md') -> None:
        self.path = path
        self.doc_ext = doc_ext
        all_files = tuple(self.path.glob('**/*'))
        self.other_files = tuple(
            f for f in all_files if f.suffix != self.doc_ext and f.is_file())
        self.docs = tuple(
            f for f in all_files if f.suffix == self.doc_ext)
