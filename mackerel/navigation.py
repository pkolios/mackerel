from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING
from urllib.parse import urljoin

from mackerel.content import Document
from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from typing import Optional, Tuple, Union  # noqa
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

    def get_menu(self, menu: str) -> 'Tuple[Node, ...]':
        menu = self._site.config.get('navigation', menu, fallback='')
        menu_entries = tuple(
            item.strip() for item in menu.split(',') if menu)
        nodes = []
        for entry in menu_entries:
            nodes.append(self.get_node(entry))
        return tuple(nodes)

    def get_node(self, document: 'Union[str, Document]') -> 'Optional[Node]':
        if isinstance(document, str):
            for node in self.nodes:
                node_rel_path = self._site.get_relative_doc_path(node.document)
                if node_rel_path == Path(document):
                    return node

        elif isinstance(document, Document):
            for node in self.nodes:
                if node.document == document:
                    return node
        return None

    def loop(self, loop: 'Optional[str]' = None) -> 'Tuple':
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
        # TODO: Parse the config user.url to extract potential path
        # ex. http://localhost:8000/blog/  'blog' path should be added
        url = self._site.get_relative_doc_path(document).with_suffix(
            self._site.config['mackerel']['OUTPUT_EXT']).as_posix()
        return str(url)

    def _build_absolute_url(self, document: Document) -> str:
        return urljoin(self._site.config.get('user', 'url', fallback='/'),
                       self._build_url(document))
