from pathlib import Path
from typing import TYPE_CHECKING, Tuple

from mackerel.helpers import cached_property, make_config
from mackerel import renderers

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa
    from mackerel.content import Document  # noqa


class Site:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.config = make_config(site_path=path)  # type: ConfigParser

    def get_relative_doc_path(self, document: 'Document') -> Path:
        return document.document_path.relative_to(self.content_path)

    @property
    def content_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['CONTENT_PATH'])

    @property
    def output_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['OUTPUT_PATH'])

    @property
    def template_path(self) -> Path:
        return self.path / Path(self.config['mackerel']['TEMPLATE_PATH'])

    @cached_property
    def document_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.content_path.rglob('*')
                     if f.suffix == self.config['mackerel']['DOC_EXT'])

    @cached_property
    def other_content_files(self) -> Tuple[Path, ...]:
        return tuple(
            f for f in self.content_path.rglob('*')
            if f.suffix != self.config['mackerel']['DOC_EXT'] and f.is_file())

    @cached_property
    def other_template_files(self) -> Tuple[Path, ...]:
        return tuple(
            f for f in self.template_path.rglob('*')
            if f.suffix != self.config['mackerel']['TEMPLATE_EXT'] and
            f.is_file())

    @cached_property
    def document_renderer(self) -> renderers.DocumentRenderer:
        renderer = getattr(
            renderers, self.config['mackerel']['DOCUMENT_RENDERER'])
        return renderer(site=self)

    @cached_property
    def template_renderer(self) -> renderers.TemplateRenderer:
        renderer = getattr(
            renderers, self.config['mackerel']['TEMPLATE_RENDERER'])
        return renderer(site=self)
