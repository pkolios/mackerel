from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING
from urllib.parse import urljoin, urlparse

from mackerel.content import Document
from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from typing import Optional, Tuple, Union  # noqa
    from mackerel.site import Site  # noqa


class Node(NamedTuple):
    url: str
    external_url: str
    document: Document


class Navigation:
    """Navigation provides methods to list and access the content"""
    def __init__(self, site: 'Site') -> None:
        self.site = site

    def get_menu(self, menu: str) -> 'Tuple[Node, ...]':
        menu = self.site.config.get('navigation', menu, fallback='')
        menu_entries = tuple(
            item.strip() for item in menu.split(',') if menu)
        nodes = []
        for entry in menu_entries:
            nodes.append(self.get_node(entry))
        return tuple(nodes)

    def get_node(self, rel_path: 'Union[str, Path]') -> 'Optional[Node]':
        if isinstance(rel_path, str):
            rel_path = Path(rel_path)

        for node in self.nodes:
            if node.document.relative_path == rel_path:
                return node
        return None

    def loop(self, path: 'Optional[str]' = '.') -> 'Tuple':
        loop_path = self.site.content_path / path.lstrip('/')
        loop_docs = tuple(
            f for f in loop_path.rglob('*')
            if f.suffix == self.site.config['mackerel']['DOC_EXT'])
        nodes = []
        for doc_path in loop_docs:
            node = self.get_node(doc_path.relative_to(self.site.content_path))
            if node:
                nodes.append(node)
        return tuple(nodes)

    @cached_property
    def nodes(self) -> 'Tuple[Node, ...]':
        return tuple(
            Node(url=self._build_url(document),
                 external_url=self._build_external_url(document),
                 document=document)
            for document in self.site.documents)

    def _build_url(self, document: Document) -> str:
        site_url = urlparse(
            self.site.config.get('user', 'url', fallback='/'))
        doc_url = document.relative_path.with_suffix(
            self.site.config['mackerel']['OUTPUT_EXT']).as_posix()
        return urljoin(site_url.path, doc_url)

    def _build_external_url(self, document: Document) -> str:
        return urljoin(self.site.config.get('user', 'url', fallback='/'),
                       self._build_url(document))
