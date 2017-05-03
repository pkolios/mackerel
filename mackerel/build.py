from pathlib import Path
from typing import TYPE_CHECKING, Tuple, NamedTuple

from mackerel import content
from mackerel.helpers import cached_property, touch

if TYPE_CHECKING:
    from mackerel import renderers  # noqa


class BuildDocument(NamedTuple):
    document: content.Document
    uri: str


class BuildPage(NamedTuple):
    path: Path
    content: str


class Context:
    # TODO: Build navigation nodes
    """Context contains data that is relevant for all documents"""
    def __init__(self, build_documents: BuildDocument) -> None:
        self._build_documents = build_documents  # type: BuildDocument


class Build:
    def __init__(self, source: content.Source, output_path: Path,
                 document_renderer: 'renderers.DocumentRenderer',
                 template_renderer: 'renderers.TemplateRenderer',
                 output_ext: str = '.html') -> None:
        self.source = source
        self.output_path = output_path
        self.document_renderer = document_renderer
        self.template_renderer = template_renderer
        self.output_ext = output_ext

    def execute(self, dry_run: bool = False) -> None:
        if dry_run:
            return None

        for page in self.pages:
            touch(page.path)
            page.path.write_text(page.content)

    @cached_property
    def context(self) -> Context:
        return Context(self.build_documents)

    @cached_property
    def documents(self) -> Tuple[content.Document, ...]:
        return tuple(content.Document(
            document_path=document_file, renderer=self.document_renderer)
            for document_file in self.source.document_files)

    @cached_property
    def build_documents(self) -> Tuple[BuildDocument, ...]:
        return tuple(BuildDocument(
            document=document, uri=self._build_uri(document))
            for document in self.documents)

    @cached_property
    def pages(self) -> Tuple[BuildPage, ...]:
        return tuple(BuildPage(
            path=self._build_page_path(build_doc.document, self.output_path),
            content=self.template_renderer.render(
                ctx=self.context, document=build_doc.document))
            for build_doc in self.build_documents)

    def __get_relative_path(self, document: content.Document) -> Path:
        return document.document_path.relative_to(self.source.path)

    def _build_page_path(self, document: content.Document,
                         output_path: Path) -> Path:
        return output_path / self.__get_relative_path(
            document).with_suffix(self.output_ext)

    def _build_uri(self, document: content.Document) -> str:
        relative_path = self.__get_relative_path(
            document).with_suffix(self.output_ext).as_posix()
        return '/{}'.format(str(relative_path))
