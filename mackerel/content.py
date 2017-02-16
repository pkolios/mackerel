import hashlib
from typing import TYPE_CHECKING, List, Tuple, Dict, Any

if TYPE_CHECKING:
    from pathlib import Path
    from mackerel.renderers import DocumentRenderer, TemplateRenderer


class Context:
    """Context contains data that is relevant for all documents"""


class Document:
    def __init__(self, content: str, renderer: 'DocumentRenderer') -> None:
        self.checksum = self.__generate_checksum(content)  # type: str
        self.metadata = renderer.extract_metadata(text=content)  # type: Dict[str, str]
        self.template = self.metadata.get('template', 'post.html')  # type: str
        self.text = renderer.extract_text(text=content)  # type: str
        self.html = renderer.render(self.text)  # type: str

    def __generate_checksum(self, content: str) -> str:
        h = hashlib.sha1(content.encode())
        return h.hexdigest()

    def __eq__(self, other) -> bool:
        return self.checksum == other.checksum


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
    _cached_ctx = None  # type: Context

    def __init__(self, source: 'Source', output_dir: 'Path',
                 document_renderer: 'DocumentRenderer',
                 template_renderer: 'TemplateRenderer',
                 output_ext = '.html') -> None:
        self.source = source
        self.output_dir = output_dir
        self.document_renderer = document_renderer
        self.template_renderer = template_renderer
        self.output_ext = output_ext

    @property
    def context(self) -> 'Context':
        # TODO: Handle context object
        self._cached_ctx = self._cached_ctx or Context()
        return self._cached_ctx

    @property
    def documents(self) -> 'Tuple[Dict[str, Any], ...]':
        self._cached_documents = self._cached_documents or tuple({
            'path': doc,
            'document': Document(content=doc.read_text(),
                                 renderer=self.document_renderer)}
            for doc in self.source.docs)
        return self._cached_documents

    @property
    def pages(self) -> 'Tuple[Dict[str, Any], ...]':
        self._cached_pages = self._cached_pages or tuple({
            'title': self._get_title(doc),
            'metadata': doc['document'].metadata,
            'uri': self._build_uri(doc),
            'body': self.template_renderer.render(ctx=self.context,
                                                  doc=doc['document'])}
            for doc in self.documents)
        return self._cached_pages

    def _get_title(self, doc: 'Dict[str, Any]') -> str:
        try:
            return doc['document'].metadata['title']
        except KeyError:
            raise KeyError(
                'Document `{}` is missing a title'.format(str(doc['path'])))

    def _build_uri(self, doc: 'Dict[str, Any]') -> str:
        relative_path = doc['path'].relative_to(self.source.path)
        relative_path = relative_path.with_suffix(self.output_ext).as_posix()
        return '/{}'.format(str(relative_path))
