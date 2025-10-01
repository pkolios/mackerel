"""Test cases for the CLI commands."""

import shutil
from pathlib import Path
from unittest import mock

import pytest
from click.testing import CliRunner

import mackerel
from mackerel.cli import cli
from mackerel.cli import run_server


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    """Fixture for creating a Click CLI runner."""
    return CliRunner()


def test_help(runner: CliRunner) -> None:
    """Test the base CLI command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.output == (
        "Usage: cli [OPTIONS] COMMAND [ARGS]...\n"
        "\n"
        "  Mackerel is a minimal static site generator.\n"
        "\n"
        "Options:\n"
        "  --version      Show the version and exit.\n"
        "  -v, --verbose  Enable verbose output.\n"
        "  --help         Show this message and exit.\n"
        "\n"
        "Commands:\n"
        "  build    Build the static site.\n"
        "  develop  Runs a local development server.\n"
        "  init     Create an new mackerel site.\n"
    )


def test_version(runner: CliRunner) -> None:
    """Test the version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"{mackerel.__title__} {mackerel.__version__}\n"


def test_init(runner: CliRunner, tmp_path: Path) -> None:
    """Test the init command."""
    site_path = tmp_path / "my_site"
    result = runner.invoke(cli, ["init", str(site_path)])
    assert result.exit_code == 0
    assert result.output == f"Initialized new mackerel site in {site_path}\n"

    config_file = site_path / "mackerelconfig.toml"
    assert config_file.exists()
    assert config_file.is_file()

    content_files = {p.name for p in (site_path / "content").iterdir()}
    assert "index.md" in content_files
    template_files = {p.name for p in (site_path / "templates" / "starter").iterdir()}
    assert "page.html" in template_files


def test_init_file_exists_error(runner: CliRunner, tmp_path: Path) -> None:
    """Test the init command with an existing directory."""
    result = runner.invoke(cli, ["init", str(tmp_path)])
    assert result.exit_code != 0
    assert (
        f"Error: Initialize failed, file {tmp_path!s} already exists" in result.output
    )


def test_build(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the build command."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)

    monkeypatch.chdir(site_path)
    with caplog.at_level("INFO"):
        result = runner.invoke(cli, ["build"], input="y\n")
    assert result.exit_code == 0
    assert "Mackerel build finished." in result.output
    assert (
        f"Error reading document {site_path / 'content' / 'bad_document.md'}"
        in result.output
    )


def test_build_custom_config(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the build command with a custom config path."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)
    shutil.move(site_path / "mackerelconfig.toml", site_path / "custom_config.toml")

    monkeypatch.chdir(site_path)
    result = runner.invoke(
        cli,
        ["build", "--config", "custom_config.toml"],
        input="y\n",
    )
    assert result.exit_code == 0


def test_build_overwrite_build(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the build command with existing _build directory and overwrite prompt."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)
    build_path = site_path / "_build"
    build_path.mkdir(exist_ok=True)
    monkeypatch.chdir(site_path)
    result = runner.invoke(cli, ["build"], input="y\n")
    assert result.exit_code == 0
    assert (
        f"Directory {build_path!s} already exists, do you want to overwrite?"
        in result.output
    )
    assert "Mackerel build finished." in result.output


def test_build_auto_yes(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the build command with --yes flag to auto-confirm overwrite."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)
    build_path = site_path / "_build"
    build_path.mkdir(exist_ok=True)

    monkeypatch.chdir(site_path)
    result = runner.invoke(cli, ["build", "--yes"])
    assert result.exit_code == 0
    assert "Mackerel build finished." in result.output


def test_build_no_config_error(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the build command with missing mackerelconfig."""
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(cli, ["build"])
    assert result.exit_code != 0
    assert "File 'mackerelconfig.toml' does not exist" in result.output


def test_build_starter_site(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the build command with the starter site."""
    starter_site = Path(__file__).parent.parent / "src" / "mackerel" / "site"
    site_path = tmp_path / "starter_site"
    shutil.copytree(starter_site, site_path)
    monkeypatch.chdir(site_path)
    result = runner.invoke(cli, ["-v", "build"], input="y\n")
    assert result.exit_code == 0
    assert "Mackerel build finished." in result.output


def test_develop(
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the develop command."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)
    monkeypatch.chdir(site_path)
    with mock.patch("mackerel.cli.run_process") as watcher:
        result = runner.invoke(cli, ["develop", "-h 0.0.0.0", "-p 8080"])
    assert result.exit_code == 0
    watcher.assert_called_once()


def test_run_server(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test the run_server function directly."""
    example_site = Path(__file__).parent / "site"
    site_path = tmp_path / "my_site"
    shutil.copytree(example_site, site_path)
    monkeypatch.chdir(site_path)
    with mock.patch("mackerel.cli.http.server") as server:
        run_server(
            host="127.0.0.42",
            port=8080,
            config_path=site_path / "mackerelconfig.toml",
            verbose=False,
        )
    captured = capsys.readouterr()
    assert "Serving mackerel at http://127.0.0.42:8080" in captured.out
    server.ThreadingHTTPServer.assert_called_once()
