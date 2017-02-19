import hashlib
from typing import TYPE_CHECKING, List, Tuple, Dict, Union

from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from pathlib import Path
    from mackerel.renderers import DocumentRenderer, TemplateRenderer


class Context:
    """Context contains data that is relevant for all documents"""

#    def _build_uri(self, document: 'Dict[str, Any]') -> str:
#        relative_path = document['path'].relative_to(self.source.path)
#        relative_path = relative_path.with_suffix(self.output_ext).as_posix()
#        return '/{}'.format(str(relative_path))


class Document:
    def __init__(self, document_path: 'Path',
                 renderer: 'DocumentRenderer') -> None:
        self.document_path = document_path# type: Path
        self.content = self.document_path.read_text()
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
        # TODO: Handle context object
        return Context()

    @cached_property
    def documents(self) -> 'Tuple[Document, ...]':
        return tuple(
            Document(
                document_path=document_file, renderer=self.document_renderer)
            for document_file in self.source.document_files)

    @cached_property
    def pages(self) -> 'Tuple[Dict[str, Union[Path, str]], ...]':
        return tuple({
            'page_path': self._build_page_path(document, self.output_dir),
            'page_content': self.template_renderer.render(
                ctx=self.context, document=document)}
            for document in self.documents)

    def _build_page_path(self, document: 'Document',
                         output_dir: 'Path') -> 'Path':
        relative_path = document.document_path.relative_to(self.source.path)
        return output_dir / relative_path.with_suffix(self.output_ext)

