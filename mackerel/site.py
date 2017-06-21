from pathlib import Path
from typing import TYPE_CHECKING, Tuple

from mackerel.helpers import cached_property, make_config

if TYPE_CHECKING:
    from configparser import ConfigParser  # noqa


class Site:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.config = make_config(site_path=path)  # type: ConfigParser # noqa
        self.template_ext = self.config['mackerel']['TEMPLATE_EXT']  # type: str # noqa
        self.output_ext = self.config['mackerel']['OUTPUT_EXT']  # type: str
        self.doc_ext = self.config['mackerel']['DOC_EXT']  # type: str

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
                     if f.suffix == self.doc_ext)

    @cached_property
    def other_content_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.content_path.rglob('*')
                     if f.suffix != self.doc_ext and f.is_file())

    @cached_property
    def other_template_files(self) -> Tuple[Path, ...]:
        return tuple(f for f in self.template_path.rglob('*')
                     if f.suffix != self.template_ext and f.is_file())
