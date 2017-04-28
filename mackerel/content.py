import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple, Dict, NamedTuple

from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from mackerel.renderers import DocumentRenderer, TemplateRenderer


class Document:
    def __init__(self, document_path: 'Path',
                 renderer: 'DocumentRenderer') -> None:
        self.document_path = document_path  # type: Path
        self.content = self.document_path.read_text()  # type: str
        self.checksum = self.__generate_checksum(self.content)  # type: str
        self.metadata = renderer.extract_metadata(text=self.content)  # type: Dict[str, str]
        self.text = renderer.extract_text(text=self.content)  # type: str
        self.template = self.metadata.get('template', 'post.html')  # type: str
        self.html = renderer.render(self.text)  # type: str
        self.title = self._get_title(self.metadata)  # type: str

    def __generate_checksum(self, content: str) -> str:
        h = hashlib.sha1(content.encode())
        return h.hexdigest()

    def _get_title(self, metadata: 'Dict[str, str]') -> str:
        try:
            return metadata['title']
        except KeyError:
            raise KeyError(
                'Document `{}` is missing a title'.format(
                    str(self.document_path)))

    def __eq__(self, other) -> bool:
        return self.checksum == other.checksum


class Source:
    def __init__(self, path: 'Path', doc_ext: str = '.md') -> None:
        self.path = path
        self.doc_ext = doc_ext
        all_files = tuple(self.path.glob('**/*'))  # type: Tuple[Path, ...]
        self.other_files = self._get_other_files(files=all_files)
        self.document_files = self._get_docs(files=all_files)

    def _get_docs(self, files: 'Tuple[Path, ...]') -> 'Tuple[Path, ...]':
        return tuple(f for f in files if f.suffix == self.doc_ext)

    def _get_other_files(self, files: 'Tuple[Path, ...]') -> 'Tuple[Path, ...]':
        return tuple(
            f for f in files if f.suffix != self.doc_ext and f.is_file())


class BuildDocument(NamedTuple):
    document: Document
    uri: str


class BuildPage(NamedTuple):
    path: Path
    content: str


class Context:
    # TODO: Build navigation nodes
    """Context contains data that is relevant for all documents"""
    def __init__(self, build_documents: 'BuildDocument') -> None:
        self._build_documents = build_documents  # type: BuildDocument


class Build:
    def __init__(self, source: 'Source', output_dir: 'Path',
                 document_renderer: 'DocumentRenderer',
                 template_renderer: 'TemplateRenderer',
                 output_ext: str = '.html') -> None:
        self.source = source
        self.output_dir = output_dir
        self.document_renderer = document_renderer
        self.template_renderer = template_renderer
        self.output_ext = output_ext

    @cached_property
    def context(self) -> 'Context':
        return Context(self.build_documents)

    @cached_property
    def documents(self) -> 'Tuple[Document, ...]':
        return tuple(Document(
            document_path=document_file, renderer=self.document_renderer)
            for document_file in self.source.document_files)

    @cached_property
    def build_documents(self) -> 'Tuple[BuildDocument, ...]':
        return tuple(BuildDocument(
            document=document, uri=self._build_uri(document))
            for document in self.documents)

    @cached_property
    def pages(self) -> 'Tuple[BuildPage, ...]':
        return tuple(BuildPage(
            path=self._build_page_path(build_doc.document, self.output_dir),
            content=self.template_renderer.render(
                ctx=self.context, document=build_doc.document))
            for build_doc in self.build_documents)

    def __get_relative_path(self, document: 'Document') -> 'Path':
        return document.document_path.relative_to(self.source.path)

    def _build_page_path(self, document: 'Document',
                         output_dir: 'Path') -> 'Path':
        return output_dir / self.__get_relative_path(
            document).with_suffix(self.output_ext)

    def _build_uri(self, document: 'Document') -> str:
        relative_path = self.__get_relative_path(
            document).with_suffix(self.output_ext).as_posix()
        return '/{}'.format(str(relative_path))
