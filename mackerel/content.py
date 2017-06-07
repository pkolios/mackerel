import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, Dict

from mackerel.helpers import cached_property, make_config

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
        self.config = make_config(source_path=path)  # type: ConfigParser # noqa
        self.template_ext = self.config['mackerel']['TEMPLATE_EXT']  # type: str # noqa
        self.output_ext = self.config['mackerel']['OUTPUT_EXT']  # type: str
        self.doc_ext = self.config['mackerel']['DOC_EXT']  # type: str

    @property
    def content_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['CONTENT_PATH'])

    @property
    def output_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['OUTPUT_PATH'])

    @property
    def template_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['TEMPLATE_PATH'])

    @cached_property
    def document_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.content_path.rglob('*')
                     if f.suffix == self.doc_ext)

    @cached_property
    def other_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.content_path.rglob('*')
                     if f.suffix != self.doc_ext and f.is_file())

    @cached_property
    def other_template_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.template_path.rglob('*')
                     if f.suffix != self.template_ext and f.is_file())
