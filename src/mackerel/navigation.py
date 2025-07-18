# from functools import cached_property
# from pathlib import Path
# from typing import TYPE_CHECKING
# from typing import NamedTuple
# from urllib.parse import urljoin
# from urllib.parse import urlparse
#
# from mackerel.content import Document
#
# if TYPE_CHECKING:
#     from mackerel.site import Site
#
#
# class Node(NamedTuple):
#     url: str
#     external_url: str
#     document: Document
#
#
# class Navigation:
#     """Navigation provides methods to list and access the content."""
#
#     def __init__(self, site: "Site") -> None:
#         self.site = site
#
#     def get_menu(self, menu: str) -> tuple[Node | None, ...]:
#         nav_cfg = getattr(self.site.config, "navigation", {})
#         menu = nav_cfg.get(menu, "")
#         menu_entries = tuple(item.strip() for item in menu.split(",") if menu)
#         return tuple(self.get_node(entry) for entry in menu_entries if entry)
#
#     def get_node(self, rel_path: str | Path) -> Node | None:
#         if isinstance(rel_path, str):
#             rel_path = Path(rel_path)
#
#         for node in self.nodes:
#             if node.document.relative_path == rel_path:
#                 return node
#         return None
#
#     def loop(self, path: str | None = "/") -> "tuple":
#         path = path.rstrip("/") + "/"
#         path = "/" + path.lstrip("/")
#         nodes = [node for node in self.nodes if node.url.startswith(path)]
#         return tuple(nodes)
#
#     @cached_property
#     def nodes(self) -> tuple[Node, ...]:
#         return tuple(
#             Node(
#                 url=self._build_url(document),
#                 external_url=self._build_external_url(document),
#                 document=document,
#             )
#             for document in self.site.documents
#         )
#
#     def _build_url(self, document: Document) -> str:
#         user_cfg = getattr(self.site.config, "user", {})
#         site_url = urlparse(user_cfg.get("url", "/"))
#         doc_url = document.relative_path.with_suffix(
#             self.site.config.mackerel.build_ext,
#         ).as_posix()
#         return urljoin(site_url.path, doc_url)
#
#     def _build_external_url(self, document: Document) -> str:
#         return urljoin(
#             self.site.config.get("user", "url", fallback="/"),
#             self._build_url(document),
#         )
