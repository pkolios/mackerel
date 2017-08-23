import logging
from pathlib import Path
from typing import TYPE_CHECKING

from mackerel import exceptions, renderers
from mackerel.content import Document
from mackerel.helpers import cached_property, make_config

if TYPE_CHECKING:
    from typing import Tuple  # noqa
    from configparser import ConfigParser  # noqa


class Site:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.config = make_config(site_path=path)  # type: ConfigParser
        self.logger = logging.getLogger('mackerel')  # type: logging.Logger

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

    @cached_property
    def documents(self) -> 'Tuple[Document, ...]':
        documents = []
        for file in self.document_files:
            try:
                documents.append(Document(
                    document_path=file, renderer=self.document_renderer))
            except exceptions.DocumentError as exc:
                self.logger.warning(str(exc))

        return tuple(documents)

    def get_relative_doc_path(self, document: 'Document') -> Path:
        return document.document_path.relative_to(self.content_path)
