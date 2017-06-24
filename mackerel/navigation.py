from typing import NamedTuple, TYPE_CHECKING
from urllib.parse import urljoin

from mackerel.content import Document
from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from typing import Optional, Tuple  # noqa
    from mackerel.site import Site  # noqa


class Node(NamedTuple):
    url: str
    absolute_url: str
    document: Document


class Navigation:
    """Navigation provides methods to list and access the content"""
    def __init__(self, documents: 'Tuple[Document, ...]',
                 site: 'Site') -> None:
        self._documents = documents
        self._site = site

    def main(self) -> 'Optional[Tuple[Node, ...]]':
        # TODO: Return root level navigation nodes
        pass

    def loop(self, loop: str = None) -> 'Tuple':
        # TODO: Return nodes of the requested loop / condition / filter
        return tuple()

    @cached_property
    def nodes(self) -> 'Tuple[Node, ...]':
        return tuple(
            Node(url=self._build_url(document),
                 absolute_url=self._build_absolute_url(document),
                 document=document)
            for document in self._documents)

    def _build_url(self, document: Document) -> str:
        url = self._site.get_relative_doc_path(document).with_suffix(
            self._site.config['mackerel']['OUTPUT_EXT']).as_posix()
        return str(url)

    def _build_absolute_url(self, document: Document) -> str:
        return urljoin(self._site.config.get('user', 'url', fallback='/'),
                       self._build_url(document))
