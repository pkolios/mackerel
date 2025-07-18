"""Mackerel CLI."""

import http.server
import logging
import shutil
from functools import partial
from pathlib import Path
from typing import Final

import click
import tomli_w
from watchfiles import run_process

import mackerel
from mackerel import config
from mackerel.build import build
from mackerel.parsers import PythonFrontmatterParser
from mackerel.renderers import Jinja2Renderer
from mackerel.renderers import MarkdownRenderer

logger = logging.getLogger(__name__)

LOG_FORMAT: Final[str] = "%(levelname)s:%(name)s:%(message)s"


def setup_logging(verbose: bool) -> None:  # noqa: FBT001
    """Setup logging configuration."""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format=LOG_FORMAT, force=True)


@click.group()
@click.version_option(message=f"{mackerel.__title__} {mackerel.__version__}")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(ctx: click.core.Context, verbose: bool) -> None:  # noqa: FBT001
    """Mackerel is a minimal static site generator."""
    ctx.obj = {"verbose": verbose}
    setup_logging(verbose)


@cli.command()
@click.argument(
    "SITE_PATH",
    type=click.Path(exists=False, resolve_path=True, path_type=Path),
)
@click.pass_context
def init(ctx: click.core.Context, site_path: Path) -> None:
    """Create an new mackerel site."""
    sample_site_path = Path(mackerel.__file__).parent / "site"

    logger.info("Copying sample site from %s to %s", sample_site_path, site_path)
    try:
        shutil.copytree(
            src=sample_site_path,
            dst=site_path,
            ignore=shutil.ignore_patterns(str(config.AppConfig().mackerel.build_path)),
        )
    except FileExistsError as e:
        ctx.fail(f"Initialize failed, file {e.filename} already exists")

    logger.info("Generating default mackerelconfig.toml")
    config_dict = config.AppConfig().to_dict()
    config_file_path = site_path / "mackerelconfig.toml"
    with config_file_path.open("wb") as f:
        tomli_w.dump(config_dict, f)

    click.echo(f"Initialized new mackerel site in {site_path}")


@cli.command(name="build")
@click.option(
    "--dry-run",
    default=False,
    is_flag=True,
    help="Run build without persisting any files.",
)
@click.option(
    "--config",
    "-c",
    "config_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    default="mackerelconfig.toml",
    help="Path to mackerel configuration file.",
)
@click.option(
    "--yes",
    "-y",
    default=False,
    is_flag=True,
    help=(
        "Automatic yes to prompts. "
        'Assume "yes" as answer to all prompts and run non-interactively.'
    ),
)
@click.pass_context
def build_(
    ctx: click.core.Context,
    config_path: Path,
    dry_run: bool,  # noqa: FBT001
    yes: bool,  # noqa: FBT001
) -> None:
    """Build the contents of SITE_PATH."""
    cfg = config.load_config(config_path)
    if cfg.mackerel.build_path.exists() and not yes:
        click.confirm(
            (
                f"Directory {cfg.mackerel.build_path!s} already exists, "
                "do you want to overwrite?"
            ),
            abort=True,
        )
    # TODO: Add support for multiple renderers & parsers here
    build(
        cfg=cfg,
        content_renderer=MarkdownRenderer(cfg.content_renderer),
        metadata_parser=PythonFrontmatterParser(),
        template_renderer=Jinja2Renderer(
            template_path=cfg.mackerel.template_path,
            template_suffix=cfg.mackerel.template_suffix,
            cfg=cfg.template_renderer,
        ),
        dry_run=dry_run,
    )
    click.echo("Mackerel build finished.")


@cli.command()
@click.option(
    "--config",
    "-c",
    "config_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    default="mackerelconfig.toml",
    help="Path to mackerel configuration file.",
)
@click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")
@click.option("--port", "-p", default=8000, help="The port to bind to.")
@click.pass_context
def develop(ctx: click.core.Context, config_path: Path, host: str, port: int) -> None:
    """Runs a local development server."""
    cfg = config.load_config(config_path)
    verbose = bool(ctx.obj and ctx.obj.get("verbose", False))
    run_process(
        config_path,
        cfg.mackerel.content_path,
        cfg.mackerel.template_path,
        target=run_server,
        args=(host, port, config_path, verbose),
    )


def run_server(host: str, port: int, config_path: Path, verbose: bool) -> None:  # noqa: FBT001
    """Run a simple HTTP server."""
    setup_logging(verbose)
    cfg = config.load_config(config_path)

    def rebuild_site() -> None:
        """Rebuild the site."""
        build(
            cfg=cfg,
            content_renderer=MarkdownRenderer(cfg.content_renderer),
            metadata_parser=PythonFrontmatterParser(),
            template_renderer=Jinja2Renderer(
                template_path=cfg.mackerel.template_path,
                template_suffix=cfg.mackerel.template_suffix,
                cfg=cfg.template_renderer,
            ),
        )

    rebuild_site()
    handler = partial(
        http.server.SimpleHTTPRequestHandler,
        directory=cfg.mackerel.build_path,
    )
    with http.server.ThreadingHTTPServer((host, port), handler) as httpd:
        click.echo(f"Serving mackerel at http://{host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down server.")
            httpd.server_close()


if __name__ == "__main__":
    cli()
