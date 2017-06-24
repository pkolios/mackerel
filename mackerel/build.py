import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, NamedTuple

from mackerel import content
from mackerel.navigation import Navigation
from mackerel.site import Site
from mackerel.helpers import cached_property, touch

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa
    from mackerel import renderers  # noqa


class BuildDocument(NamedTuple):
    document: content.Document
    uri: str


class BuildPage(NamedTuple):
    path: Path
    content: str


class Context:
    """Context contains data that is relevant for all documents"""
    def __init__(self, build_documents: Tuple[BuildDocument, ...],
                 config: 'ConfigParser') -> None:
        self.nav = Navigation(build_documents)
        self.cfg = config


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

        for f in self.site.other_content_files:
            path = self._build_other_file_path(f)
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            shutil.copyfile(src=f, dst=path)

        for f in self.site.other_template_files:
            path = self._build_template_file_path(f)
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            shutil.copyfile(src=f, dst=path)

    @cached_property
    def context(self) -> Context:
        return Context(
            build_documents=self.build_documents, config=self.site.config)

    @cached_property
    def documents(self) -> Tuple[content.Document, ...]:
        return tuple(content.Document(
            document_path=document_file, renderer=self.site.document_renderer)
            for document_file in self.site.document_files)

    @cached_property
    def build_documents(self) -> Tuple[BuildDocument, ...]:
        return tuple(BuildDocument(
            document=document, uri=self._build_uri(document))
            for document in self.documents)

    @cached_property
    def pages(self) -> Tuple[BuildPage, ...]:
        return tuple(BuildPage(
            path=self._build_page_path(build_doc.document),
            content=self.site.template_renderer.render(
                ctx=self.context, document=build_doc.document))
            for build_doc in self.build_documents)

    def __get_relative_doc_path(self, document: content.Document) -> Path:
        return document.document_path.relative_to(self.site.content_path)

    def _build_page_path(self, document: content.Document) -> Path:
        return self.site.output_path / self.__get_relative_doc_path(
            document).with_suffix(self.site.config['mackerel']['OUTPUT_EXT'])

    def _build_uri(self, document: content.Document) -> str:
        relative_path = self.__get_relative_doc_path(
            document).with_suffix(
                self.site.config['mackerel']['OUTPUT_EXT']).as_posix()
        return '/{}'.format(str(relative_path))

    def _build_other_file_path(self, other_file: Path) -> Path:
        return self.site.output_path / other_file.relative_to(
            self.site.content_path)

    def _build_template_file_path(self, template_file: Path) -> Path:
        return self.site.output_path / template_file.relative_to(
            self.site.template_path)
