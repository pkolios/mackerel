"""The config module contains configuration classes and functions."""

import tomllib
from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Self

from mackerel import __title__
from mackerel import __url__
from mackerel import types as t


def _config_dict_factory(data: Any) -> dict[str, Any]:  # noqa: ANN401
    """Custom dict factory to handle Paths."""
    return {k: (v.as_posix() if isinstance(v, Path) else v) for k, v in data}


@dataclass
class MackerelConfig:
    """Configuration for Mackerel."""

    build_path: t.BuildPath = field(default_factory=lambda: t.BuildPath(Path("_build")))
    build_suffix: t.BuildSuffix = field(
        default_factory=lambda: t.BuildSuffix(".html"),
    )
    content_path: t.ContentPath = field(
        default_factory=lambda: t.ContentPath(Path("content")),
    )
    doc_suffix: t.DocSuffix = field(default_factory=lambda: t.DocSuffix(".md"))
    template_path: t.TemplatePath = field(
        default_factory=lambda: t.TemplatePath(Path("templates/starter")),
    )
    template_suffix: t.TemplateSuffix = field(
        default_factory=lambda: t.TemplateSuffix(".html"),
    )
    content_renderer: str = "MarkdownRenderer"
    template_renderer: str = "Jinja2Renderer"

    navigation: list[t.NavItem] = field(
        default_factory=lambda: [
            t.NavItem(
                label=t.Label("Home"),
                url=t.RelativeURL("/"),
                children=[],
            ),
            t.NavItem(
                label=t.Label(__title__),
                url=t.AbsoluteURL(__url__),
            ),
        ],
    )

    def __post_init__(self) -> None:
        """Post-initialization validation."""
        for suffix in (self.template_suffix, self.build_suffix, self.doc_suffix):
            if not suffix.startswith("."):
                msg = f"Invalid file suffix: '{suffix}'. It must start with '.'"
                raise ValueError(msg)


@dataclass
class Jinja2RendererConfig:
    """Configuration for Jinja2 renderer."""

    trim_blocks: bool = True
    lstrip_blocks: bool = True


@dataclass
class MarkdownRendererConfig:
    """Configuration for Markdown renderer."""

    output_format: Literal["html", "xhtml"] = "html"
    extensions: list[str] = field(
        default_factory=lambda: [
            "markdown.extensions.meta",
            "markdown.extensions.extra",
        ],
    )


@dataclass
class AppConfig:
    """Main application configuration that includes all other configurations."""

    mackerel: MackerelConfig = field(default_factory=MackerelConfig)
    content_renderer: MarkdownRendererConfig = field(
        default_factory=MarkdownRendererConfig,
    )
    template_renderer: Jinja2RendererConfig = field(
        default_factory=Jinja2RendererConfig,
    )
    user: t.UserConfig = field(default_factory=lambda: t.UserConfig({}))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create config from dict."""
        mackerel = MackerelConfig(**data.get("mackerel", {}))
        content_renderer = MarkdownRendererConfig(
            **data.get(mackerel.content_renderer, {}),
        )
        template_renderer = Jinja2RendererConfig(
            **data.get(mackerel.template_renderer, {}),
        )
        user = data.get("user", {})

        return cls(
            mackerel=mackerel,
            content_renderer=content_renderer,
            template_renderer=template_renderer,
            user=user,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to TOML compatible dictionary."""
        out: dict[str, Any] = {}
        for f in fields(self):
            key = (
                self.mackerel.content_renderer
                if f.name == "content_renderer"
                else self.mackerel.template_renderer
                if f.name == "template_renderer"
                else f.name
            )
            out[key] = (
                asdict(getattr(self, f.name), dict_factory=_config_dict_factory)
                if is_dataclass(getattr(self, f.name))
                else getattr(self, f.name)
            )
        return out


def _load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def _parse_nav_items(raw_items: Sequence[Mapping[str, Any]]) -> list[t.NavItem]:
    def parse(item: Mapping[str, Any]) -> t.NavItem:
        return t.NavItem(
            label=t.Label(item["label"]),
            url=item["url"],
            children=_parse_nav_items(item.get("children", [])),
        )

    return [parse(entry) for entry in raw_items]


def load_config(config_path: Path) -> AppConfig:
    """Load user-defined TOML config."""
    raw_data = _load_toml(config_path)
    config = AppConfig.from_dict(raw_data)

    # Resolve paths relative to the config file & navigation
    base_dir = config_path.parent.resolve()
    mcfg = config.mackerel
    raw_navigation = raw_data.get("mackerel", {}).get("navigation", [])

    build_path = t.BuildPath(base_dir / mcfg.build_path)
    content_path = t.ContentPath(base_dir / mcfg.content_path)
    template_path = t.TemplatePath(base_dir / mcfg.template_path)

    for path in (content_path, template_path):
        if not path.exists():
            msg = f"Path '{path}' does not exist."
            raise FileNotFoundError(msg)

    config.mackerel = MackerelConfig(
        **{
            **asdict(mcfg),
            "build_path": build_path,
            "content_path": content_path,
            "template_path": template_path,
            "navigation": _parse_nav_items(raw_navigation),
        },
    )

    return config
