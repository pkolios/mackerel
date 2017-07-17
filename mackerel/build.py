import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, NamedTuple
from urllib.parse import urljoin, urlparse

from mackerel import content, exceptions
from mackerel.navigation import Navigation
from mackerel.site import Site
from mackerel.helpers import cached_property, touch

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa
    from mackerel import renderers  # noqa


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class BuildPage(NamedTuple):
    path: Path
    content: str


class Context:
    """Context contains data that is relevant for all documents"""
    def __init__(self, documents: Tuple[content.Document, ...],
                 site: Site) -> None:
        self.nav = Navigation(documents=documents, site=site)
        self.cfg = site.config

    def url_for(self, resource: str, external: bool = False) -> str:
        site_url = urlparse(self.cfg.get('user', 'url', fallback='/'))
        if external:
            return urljoin(site_url.geturl(), resource)

        return urljoin(site_url.path, resource)


class Build:
    def __init__(self, site: Site) -> None:
        self.site = site

    def execute(self, dry_run: bool = False) -> None:
        if dry_run:
            return None

        try:
            shutil.rmtree(self.site.output_path)
        except FileNotFoundError:
            pass

        for page in self.pages:
            touch(page.path)
            page.path.write_text(page.content)

        logger.info(f'{len(self.pages)} pages were built')

        for f in self.site.other_content_files:
            path = self._absolute_other_file_output_path(f)
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            shutil.copyfile(src=f, dst=path)

        for f in self.site.other_template_files:
            path = self._absolute_template_file_output_path(f)
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            shutil.copyfile(src=f, dst=path)

    @cached_property
    def context(self) -> Context:
        return Context(documents=self.documents, site=self.site)

    @cached_property
    def documents(self) -> Tuple[content.Document, ...]:
        documents = []
        for file in self.site.document_files:
            try:
                documents.append(content.Document(
                    document_path=file, renderer=self.site.document_renderer))
            except exceptions.DocumentError as exc:
                logger.warning(str(exc))

        return tuple(documents)

    @cached_property
    def pages(self) -> Tuple[BuildPage, ...]:
        pages = []
        for document in self.documents:
            try:
                pages.append(BuildPage(
                    path=self._absolute_page_output_path(document),
                    content=self.site.template_renderer.render(
                        ctx=self.context, document=document)))
            except exceptions.RenderingError as exc:
                logger.warning(str(exc))

        return tuple(pages)

    def _absolute_page_output_path(self, document: content.Document) -> Path:
        return self.site.output_path / self.site.get_relative_doc_path(
            document).with_suffix(self.site.config['mackerel']['OUTPUT_EXT'])

    def _absolute_other_file_output_path(self, other_file: Path) -> Path:
        return self.site.output_path / other_file.relative_to(
            self.site.content_path)

    def _absolute_template_file_output_path(self, template_file: Path) -> Path:
        return self.site.output_path / template_file.relative_to(
            self.site.template_path)
