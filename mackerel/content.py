from typing import TYPE_CHECKING, List, Tuple, Dict, Any

if TYPE_CHECKING:
    from pathlib import Path
    from mackerel.renderers import DocumentRenderer, TemplateRenderer


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
        all_files = tuple(self.path.glob('**/*'))  # type: Tuple[Path, ...]
        self.other_files = self._get_other_files(files=all_files)
        self.docs = self._get_docs(files=all_files)

    def _get_docs(self, files: 'Tuple[Path, ...]') -> 'Tuple[Path, ...]':
        return tuple(f for f in files if f.suffix == self.doc_ext)

    def _get_other_files(self, files: 'Tuple[Path, ...]') -> 'Tuple[Path, ...]':
        return tuple(
            f for f in files if f.suffix != self.doc_ext and f.is_file())


class Build:
    _cached_documents = None  # type: Tuple[Dict[str, Any], ...]
    _cached_pages = None  # type: Tuple[Dict[str, Any], ...]

    def __init__(self, source: 'Source', output_dir: 'Path',
                 document_renderer: 'DocumentRenderer',
                 template_renderer: 'TemplateRenderer') -> None:
        self.source = source
        self.output_dir = output_dir
        self.document_renderer = document_renderer
        self.template_renderer = template_renderer

    @property
    def documents(self) -> 'Tuple[Dict[str, Any], ...]':
        self._cached_documents = self._cached_documents or tuple(
            {'path': doc, 'document': Document(
                content=doc.read_text(), renderer=self.document_renderer)}
            for doc in self.source.docs)
        return self._cached_documents

    @property
    def pages(self) -> 'Tuple[Dict[str, Any], ...]':
        # TODO: Handle context object
        self._cached_pages = self._cached_pages or tuple(
            {'url': 'TODO', 'page': self.template_renderer.render(
                ctx=Context(), doc=doc['document'])} for doc in self.documents)
        return self._cached_pages
