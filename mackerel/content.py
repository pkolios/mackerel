import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, Dict

from mackerel import helpers

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa
    from mackerel.renderers import DocumentRenderer  # noqa


class Document:
    def __init__(self, document_path: Path,
                 renderer: 'DocumentRenderer') -> None:
        self.document_path = document_path  # type: Path
        self.content = self.document_path.read_text()  # type: str
        self.checksum = self.__generate_checksum(self.content)  # type: str
        self.metadata = renderer.extract_metadata(
            text=self.content)  # type: Dict[str, str]
        self.text = renderer.extract_text(text=self.content)  # type: str
        self.template = self.metadata.get('template', 'post.html')  # type: str
        self.html = renderer.render(self.text)  # type: str
        self.title = self._get_title(self.metadata)  # type: str

    def __generate_checksum(self, content: str) -> str:
        h = hashlib.sha1(content.encode())
        return h.hexdigest()

    def _get_title(self, metadata: Dict[str, str]) -> str:
        try:
            return metadata['title']
        except KeyError:
            raise KeyError(
                'Document `{}` is missing a title'.format(
                    str(self.document_path)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Document):
            return False
        return self.checksum == other.checksum


class Source:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.config = helpers.make_config(source_path=path)  # type: ConfigParser # noqa
        self.content_path = path / Path(
            self.config['mackerel']['CONTENT_PATH'])  # type: Path # noqa
        self.output_path = path / Path(self.config['mackerel']['OUTPUT_PATH'])  # type: Path # noqa
        self.template_path = path / Path(
            self.config['mackerel']['TEMPLATE_PATH'])  # type: Path # noqa
        self.output_ext = self.config['mackerel']['OUTPUT_EXT']  # type: str
        self.doc_ext = self.config['mackerel']['DOC_EXT']  # type: str
        content_files = tuple(self.content_path.rglob('*'))  # type: Tuple[Path, ...] # noqa
        self.other_files = self._get_other_files(files=content_files)
        self.document_files = self._get_docs(files=content_files)

    def _get_docs(self, files: Tuple[Path, ...]) -> Tuple[Path, ...]:
        return tuple(f for f in files if f.suffix == self.doc_ext)

    def _get_other_files(self, files: Tuple[Path, ...]) -> Tuple[Path, ...]:
        return tuple(
            f for f in files if f.suffix != self.doc_ext and f.is_file())
