"""Tests for the mackerel config module."""

from dataclasses import asdict
from functools import partial
from pathlib import Path

import pytest

from mackerel import __url__
from mackerel import config
from mackerel import types as t


def test_mackerel_config_defaults() -> None:
    """Test the default settings of MackerelConfig."""
    cfg = asdict(config.MackerelConfig())
    assert cfg == {
        "build_path": Path("_build"),
        "build_suffix": ".html",
        "content_path": Path("content"),
        "doc_suffix": ".md",
        "navigation": [
            {"children": [], "label": "Home", "url": "/"},
            {"children": [], "label": "mackerel", "url": __url__},
        ],
        "template_path": Path("templates/starter"),
        "template_suffix": ".html",
        "content_renderer": "MarkdownRenderer",
        "template_renderer": "Jinja2Renderer",
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("build_suffix", t.BuildSuffix("invalid")),
        ("doc_suffix", t.DocSuffix("invalid")),
        ("template_suffix", t.TemplateSuffix("invalid")),
    ],
)
def test_mackerel_config_validation(
    field: str, value: t.BuildSuffix | t.DocSuffix | t.TemplateSuffix
) -> None:
    """Test MackerelConfig suffix validation."""
    with pytest.raises(
        ValueError, match="Invalid file suffix: 'invalid'. It must start with '.'"
    ):
        partial(config.MackerelConfig, **{field: value})()


def test_jinja2_renderer_config_defaults() -> None:
    """Test the default settings of Jinja2RendererConfig."""
    cfg = asdict(config.Jinja2RendererConfig())
    assert cfg == {
        "trim_blocks": True,
        "lstrip_blocks": True,
    }


def test_markdown_renderer_config_defaults() -> None:
    """Test the default settings of MarkdownRendererConfig."""
    cfg = asdict(config.MarkdownRendererConfig())
    assert cfg == {
        "output_format": "html",
        "extensions": ["markdown.extensions.meta", "markdown.extensions.extra"],
    }


def test_app_config_defaults() -> None:
    """Test the default settings of AppConfig."""
    cfg = asdict(config.AppConfig())
    assert cfg == {
        "mackerel": asdict(config.MackerelConfig()),
        "template_renderer": asdict(config.Jinja2RendererConfig()),
        "content_renderer": asdict(config.MarkdownRendererConfig()),
        "user": {},
    }


def test_app_config_to_dict() -> None:
    """Test converting AppConfig to dictionary."""
    cfg = config.AppConfig().to_dict()
    assert cfg == {
        "Jinja2Renderer": {"lstrip_blocks": True, "trim_blocks": True},
        "MarkdownRenderer": {
            "extensions": ["markdown.extensions.meta", "markdown.extensions.extra"],
            "output_format": "html",
        },
        "mackerel": {
            "build_path": "_build",
            "build_suffix": ".html",
            "content_path": "content",
            "content_renderer": "MarkdownRenderer",
            "doc_suffix": ".md",
            "navigation": [
                {"children": [], "label": "Home", "url": "/"},
                {"children": [], "label": "mackerel", "url": "https://mackerel.sh"},
            ],
            "template_path": "templates/starter",
            "template_renderer": "Jinja2Renderer",
            "template_suffix": ".html",
        },
        "user": {},
    }


def test_load_config_with_navigation(tmp_path: Path) -> None:
    """Test loading config with navigation items."""
    cfg_file = tmp_path / "mackerelconfig.toml"
    Path(tmp_path / "content").mkdir()
    Path(tmp_path / "templates" / "starter").mkdir(parents=True)
    user_toml = """
    [mackerel]
    build_path = "custom_build"
    navigation = [
      { label = "Test", url = "content/test.md" },
      { label = "Ext", url = "http://example.com" },
      { label = "Parent", url = "content/parent/index.md", children = [
        { label = "Child1", url = "content/parent/child1.md" },
        { label = "Child2", url = "content/parent/child2.md" }
      ] },
    ]
    """
    cfg_file.write_text(user_toml)
    cfg = config.load_config(cfg_file)
    assert cfg.mackerel.build_path == tmp_path / Path("custom_build")
    assert len(cfg.mackerel.navigation) == 3
    assert cfg.mackerel.navigation[0].label == "Test"
    assert cfg.mackerel.navigation[0].url == "content/test.md"
    assert cfg.mackerel.navigation[1].label == "Ext"
    assert cfg.mackerel.navigation[1].url == "http://example.com"
    assert cfg.mackerel.navigation[2].label == "Parent"
    assert cfg.mackerel.navigation[2].url == "content/parent/index.md"
    assert cfg.mackerel.navigation[2].children[0].label == "Child1"
    assert cfg.mackerel.navigation[2].children[0].url == "content/parent/child1.md"
    assert cfg.mackerel.navigation[2].children[1].label == "Child2"
    assert cfg.mackerel.navigation[2].children[1].url == "content/parent/child2.md"


def test_load_config_partial_override(tmp_path: Path) -> None:
    """Test loading user config that partially overrides defaults."""
    cfg_file = tmp_path / "mackerelconfig.toml"
    Path(tmp_path / "content").mkdir()
    Path(tmp_path / "templates" / "starter").mkdir(parents=True)
    user_toml = """
    [mackerel]
    build_path = "custom_build"

    [Jinja2Renderer]
    trim_blocks = false
    """
    cfg_file.write_text(user_toml)
    cfg = config.load_config(cfg_file)
    assert cfg.mackerel.build_path == tmp_path / Path("custom_build")
    assert cfg.mackerel.build_suffix == ".html"  # Default should remain unchanged

    assert cfg.template_renderer.trim_blocks is False  # User override applied
    assert (
        cfg.template_renderer.lstrip_blocks is True
    )  # Default should remain unchanged


def test_load_config_no_file(tmp_path: Path) -> None:
    """Test loading config with no file, should return defaults."""
    cfg_file = tmp_path / "mackerelconfig.toml"
    Path(tmp_path / "content").mkdir()
    Path(tmp_path / "templates" / "starter").mkdir(parents=True)
    assert not cfg_file.exists()

    cfg = config.load_config(cfg_file)

    assert cfg.mackerel.build_path == tmp_path / "_build"
    assert cfg.mackerel.content_path == tmp_path / "content"
    assert cfg.mackerel.template_path == tmp_path / "templates/starter"


def test_load_config_paths_exist(tmp_path: Path) -> None:
    """Test loading config raises error if paths do not exist."""
    cfg_file = tmp_path / "mackerelconfig.toml"
    content_path = tmp_path / "content"
    template_path = tmp_path / "templates/starter"

    with pytest.raises(
        FileNotFoundError, match=f"Path '{content_path}' does not exist."
    ):
        config.load_config(cfg_file)

    content_path.mkdir()
    with pytest.raises(
        FileNotFoundError, match=f"Path '{template_path}' does not exist."
    ):
        config.load_config(cfg_file)


def test_user_section(tmp_path: Path) -> None:
    """Test loading user section in config."""
    cfg_file = tmp_path / "mackerelconfig.toml"
    Path(tmp_path / "content").mkdir()
    Path(tmp_path / "templates" / "starter").mkdir(parents=True)
    user_toml = """
    [user]
    name = "Test User"
    email = "test@example.com"
    """
    cfg_file.write_text(user_toml)

    cfg = config.load_config(cfg_file)

    assert cfg.user["name"] == "Test User"
    assert cfg.user["email"] == "test@example.com"
