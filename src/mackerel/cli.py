"""Mackerel CLI."""

# import shutil
# from pathlib import Path
#
# import click
# import tomli_w
# from livereload import Server
#
# import mackerel
# from mackerel import config
# from mackerel.build import Build
# from mackerel.site import Site
#
#
# @click.group()
# @click.version_option(message=f"{mackerel.__title__} {mackerel.__version__}")
# @click.pass_context
# def cli(ctx: click.core.Context) -> None:
#     """Mackerel is a minimal static site generator."""
#     ctx.obj = {}
#
#
# @cli.command()
# @click.argument(
#     "SITE_PATH",
#     type=click.Path(exists=False, resolve_path=True, path_type=Path),
# )
# @click.pass_context
# def init(ctx: click.core.Context, site_path: Path) -> None:
#     """Create an new mackerel site."""
#     sample_site_path = Path(mackerel.__file__).parent / "site"
#
#     try:
#         shutil.copytree(src=sample_site_path, dst=site_path)
#     except FileExistsError as e:
#         ctx.fail(f"Initialize failed, file {e.filename} already exists")
#
#     # Generate mackerelconfig.toml with default settings
#     default_config = config.AppConfig()
#     config_dict = default_config.model_dump(mode="json")
#     config_file_path = site_path / "mackerelconfig.toml"
#     with config_file_path.open("wb") as f:
#         tomli_w.dump(config_dict, f)
#
#     click.echo(f"Initialized empty mackerel site in {site_path}")
#
#
# @cli.command()
# @click.option(
#     "--dry-run",
#     default=False,
#     is_flag=True,
#     help="Run build without persisting any files.",
# )
# @click.option(
#     "--config",
#     "-c",
#     "config_path",
#     type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
#     default="mackerelconfig.toml",
#     help="Path to mackerel configuration file.",
# )
# @click.pass_context
# def build(ctx: click.core.Context, config_path: Path, dry_run: bool) -> None:
#     """Build the contents of SITE_PATH."""
#     site = Site(config_path=config_path)
#
#     if site.config.mackerel.build_path.exists():
#         click.confirm(
#             (
#                 f"Directory {site.config.mackerel.build_path!s} already exists, "
#                 "do you want to overwrite?"
#             ),
#             abort=True,
#         )
#
#     build = Build(site=site)
#     build.execute(dry_run=dry_run)
#     click.echo("Build finished.")
#
#
# @cli.command()
# @click.option(
#     "--config",
#     "-c",
#     "config_path",
#     type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
#     default="mackerelconfig.toml",
#     help="Path to mackerel configuration file.",
# )
# @click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")
# @click.option("--port", "-p", default=8000, help="The port to bind to.")
# @click.pass_context
# def develop(ctx: click.core.Context, config_path: Path, host: str, port: int) -> None:
#     """Runs a local development server."""
#
#     def rebuild_site() -> Site:
#         site = Site(config_path=config_path)
#         build = Build(site=site)
#         build.execute()
#         return site
#
#     site = rebuild_site()
#     server = Server()
#     server.watch(site.config.mackerel.content_path, func=rebuild_site)
#     server.watch(site.config.mackerel.template_path, func=rebuild_site)
#     server.serve(host=host.strip(), port=port, root=site.config.mackerel.build_path)
#
#
# if __name__ == "__main__":
#     cli()
