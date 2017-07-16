import hashlib
from pathlib import Path
from textwrap import shorten
from typing import TYPE_CHECKING, Dict, Optional

from mackerel import exceptions

if TYPE_CHECKING:
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
        self.template = self._get_metadata_value(
            key='template', metadata=self.metadata)  # type: str
        self.html = renderer.render(self.text)  # type: str
        self.title = self._get_metadata_value(
            key='title', metadata=self.metadata)  # type: str
        self._renderer = renderer

    def __generate_checksum(self, content: str) -> str:
        h = hashlib.sha1(content.encode())
        return h.hexdigest()

    def _get_metadata_value(self, key: str, metadata: Dict[str, str]) -> str:
        try:
            return metadata[key]
        except KeyError:
            raise exceptions.DocumentError(
                f'Document `{str(self.document_path)}` is missing a {key}')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Document):
            return False
        return self.checksum == other.checksum

    def excerpt(self, width: Optional[int] = 150,
                placeholder: Optional[str] = '...') -> str:
        text = self._renderer.strip_tags(self.html)
        return shorten(text, width=(width or 150)+len(placeholder),
                       placeholder=placeholder)
