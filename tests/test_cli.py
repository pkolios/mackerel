"""Test cases for the CLI commands."""

# import tomllib
# from pathlib import Path
# from unittest import mock
#
# import pytest
# from click.testing import CliRunner
#
# from mackerel import cli
#
#
# @pytest.fixture
# def runner() -> CliRunner:
#     """Fixture for creating a Click CLI runner."""
#     return CliRunner()
#
#
# @pytest.fixture
# def build_path(site_path: Path) -> Path:
#     """Fixture for the build path where the site will be built."""
#     return site_path / "_build"
#
#
# def test_cli_base(runner: CliRunner) -> None:
#     """Test the base CLI command."""
#     result = runner.invoke(cli.cli, ["--help"])
#     assert result.exit_code == 0
#     assert "build" in result.output
#
#
# def test_init_directory_exists(runner: CliRunner, site_path: Path) -> None:
#     """Test the init command with an existing directory."""
#     result = runner.invoke(cli.cli, ["init", str(site_path)])
#     assert result.exit_code == 2
#     assert f"Initialize failed, file {site_path!s}" in result.output
#
#
# def test_init_directory_success(
#     runner: CliRunner,
#     tmp_path_factory: pytest.TempPathFactory,
#     site_path: Path,
# ) -> None:
#     """Test the init command with a new directory."""
#     test_path = tmp_path_factory.mktemp("cli-test") / "test-site"
#     result = runner.invoke(cli.cli, ["init", str(test_path)])
#     assert result.exit_code == 0
#     assert result.output == f"Initialized empty mackerel site in {test_path}\n"
#
#     # Check that expected files/directories are copied
#     template_files = {p.name for p in site_path.iterdir()}
#     new_site_files = {p.name for p in test_path.iterdir()}
#
#     assert template_files.issubset(new_site_files)
#
#     # Check that mackerelconfig.toml exists
#     config_file = test_path / "mackerelconfig.toml"
#     assert config_file.exists()
#     assert config_file.is_file()
#
#     # Check content of mackerelconfig.toml
#     with config_file.open("rb") as f:
#         toml_data = tomllib.load(f)
#
#     # Spot check some keys
#     assert "mackerel" in toml_data
#     assert toml_data["mackerel"]["build_path"] == "_build"
#     assert toml_data["template_renderer"]["trim_blocks"] is True
#     assert toml_data["content_renderer"]["build_format"] in {"html", "xhtml"}
#
#
# def test_build_error(runner: CliRunner) -> None:
#     """Test the build command with missing mackerelconfig."""
#     result = runner.invoke(cli.cli, ["build"])
#     assert result.exit_code == 2
#     assert "File 'mackerelconfig.toml' does not exist" in result.output
#
#
# @pytest.mark.parametrize(
#     "use_config_flag",
#     [True, False],
#     ids=["with-config", "without-config"],
# )
# def test_build_success(
#     runner: CliRunner,
#     site_path: Path,
#     build_path: Path,
#     use_config_flag: bool,
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     """Test the build command with and without --config flag."""
#     # Make sure build dir exists to trigger overwrite prompt
#     build_path.mkdir(exist_ok=True)
#
#     if use_config_flag:
#         args = ["build", "--config", str(site_path / "mackerelconfig.toml")]
#     else:
#         args = ["build"]
#         monkeypatch.chdir(site_path)
#
#     result = runner.invoke(
#         cli.cli,
#         args,
#         input="y\n",
#     )
#
#     assert result.exit_code == 0
#     assert (
#         f"Directory {build_path!s} already exists, do you want to overwrite?"
#         in result.output
#     )
#     assert "\nBuild finished.\n" in result.output
#     assert list(build_path.iterdir())
#
#
# @pytest.mark.parametrize(
#     "use_config_flag",
#     [True, False],
#     ids=["with-config", "without-config"],
# )
# def test_develop(
#     runner: CliRunner,
#     site_path: Path,
#     build_path: Path,
#     use_config_flag: bool,
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     """Test the develop command."""
#     if use_config_flag:
#         args = [
#             "develop",
#             "-h 0.0.0.0",
#             "-p 8080",
#             "--config",
#             str(site_path / "mackerelconfig.toml"),
#         ]
#     else:
#         args = ["develop", "-h 0.0.0.0", "-p 8080"]
#         monkeypatch.chdir(site_path)
#     with (
#         mock.patch("mackerel.cli.Server") as server,
#         mock.patch("mackerel.cli.Build") as build,
#     ):
#         runner.invoke(cli.cli, args)
#
#     assert build.called
#     build().execute.assert_called_with()
#
#     server.assert_called_with()
#     watch_calls = (
#         mock.call(site_path / "content", func=mock.ANY),
#         mock.call(site_path / "template", func=mock.ANY),
#     )
#     server().watch.assert_has_calls(watch_calls, any_order=True)
#     server().serve.assert_called_with(
#         host="0.0.0.0",
#         port=8080,
#         root=build_path,
#     )
