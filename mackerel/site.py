from pathlib import Path
from typing import TYPE_CHECKING

from mackerel.helpers import make_config
from mackerel import renderers

if TYPE_CHECKING:
    from typing import Tuple  # noqa
    from configparser import ConfigParser  # noqa
    from mackerel.content import Document  # noqa


class Site:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.config = make_config(site_path=path)  # type: ConfigParser

        # Site paths
        self.content_path = self.path / Path(
            self.config['mackerel']['CONTENT_PATH'])  # type: Path
        self.output_path = self.path / Path(
            self.config['mackerel']['OUTPUT_PATH'])  # type: Path
        self.template_path = self.path / Path(
            self.config['mackerel']['TEMPLATE_PATH'])  # type: Path

        # Site files
        self.document_files = tuple(
            f for f in self.content_path.rglob('*')
            if f.suffix == self.config['mackerel']['DOC_EXT'])  # type: Tuple[Path, ...] # noqa
        self.other_content_files = tuple(
            f for f in self.content_path.rglob('*')
            if f.suffix != self.config['mackerel']['DOC_EXT'] and
            f.is_file())  # type: Tuple[Path, ...]
        self.other_template_files = tuple(
            f for f in self.template_path.rglob('*')
            if f.suffix != self.config['mackerel']['TEMPLATE_EXT'] and
            f.is_file())  # type: Tuple[Path, ...]

        # Site renderers
        self.document_renderer = getattr(
            renderers.document,
            self.config['mackerel']['DOCUMENT_RENDERER'])(site=self)  # type: renderers.base.DocumentRenderer # noqa
        self.template_renderer = getattr(
            renderers.template,
            self.config['mackerel']['TEMPLATE_RENDERER'])(site=self)  # type: renderers.base.TemplateRenderer # noqa

    def get_relative_doc_path(self, document: 'Document') -> Path:
        return document.document_path.relative_to(self.content_path)
