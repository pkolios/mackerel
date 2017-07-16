from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING
from urllib.parse import urljoin, urlparse

from mackerel import exceptions
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
            doc_path = self._site.content_path / Path(document)
            try:
                document = Document(
                    document_path=doc_path,
                    renderer=self._site.document_renderer)
            except (FileNotFoundError, exceptions.DocumentError):
                return None

        for node in self.nodes:
            if node.document == document:
                return node
        return None

    def loop(self, path: 'Optional[str]' = '.') -> 'Tuple':
        loop_path = self._site.content_path / path.lstrip('/')
        loop_docs = tuple(
            f for f in loop_path.rglob('*')
            if f.suffix == self._site.config['mackerel']['DOC_EXT'])
        nodes = []
        for doc in loop_docs:
            node = self.get_node(str(doc))
            if node:
                nodes.append(node)
        return tuple(nodes)

    @cached_property
    def nodes(self) -> 'Tuple[Node, ...]':
        return tuple(
            Node(url=self._build_url(document),
                 absolute_url=self._build_absolute_url(document),
                 document=document)
            for document in self._documents)

    def _build_url(self, document: Document) -> str:
        site_url = urlparse(
            self._site.config.get('user', 'url', fallback='/'))
        doc_url = self._site.get_relative_doc_path(document).with_suffix(
            self._site.config['mackerel']['OUTPUT_EXT']).as_posix()
        return urljoin(site_url.path, doc_url)

    def _build_absolute_url(self, document: Document) -> str:
        return urljoin(self._site.config.get('user', 'url', fallback='/'),
                       self._build_url(document))
