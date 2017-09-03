import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, NamedTuple
from urllib.parse import urljoin, urlparse

from mackerel import content, exceptions
from mackerel.navigation import Navigation
from mackerel.site import Site
from mackerel.helpers import cached_property

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa
    from mackerel import renderers  # noqa


class BuildPage(NamedTuple):
    path: Path
    content: str


class Context:
    """Context contains data that is relevant for all documents"""
    def __init__(self, site: Site) -> None:
        self.nav = Navigation(site=site)
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
            self.touch(page.path)
            page.path.write_text(page.content)

        self.site.logger.info(f'{len(self.pages)} pages were built')

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

    @staticmethod
    def touch(path: Path) -> bool:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.touch()
        return True

    @cached_property
    def context(self) -> Context:
        return Context(site=self.site)

    @cached_property
    def pages(self) -> Tuple[BuildPage, ...]:
        pages = []
        for document in self.site.documents:
            try:
                pages.append(BuildPage(
                    path=self._absolute_page_output_path(document),
                    content=self.site.template_renderer.render(
                        ctx=self.context, document=document)))
            except exceptions.RenderingError as exc:
                self.site.logger.warning(str(exc))

        return tuple(pages)

    def _absolute_page_output_path(self, document: content.Document) -> Path:
        return self.site.output_path / document.relative_path.with_suffix(
            self.site.config['mackerel']['OUTPUT_EXT'])

    def _absolute_other_file_output_path(self, other_file: Path) -> Path:
        return self.site.output_path / other_file.relative_to(
            self.site.content_path)

    def _absolute_template_file_output_path(self, template_file: Path) -> Path:
        return self.site.output_path / template_file.relative_to(
            self.site.template_path)
