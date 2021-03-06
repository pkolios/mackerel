import os
import shutil
from pathlib import Path

import click
from livereload import Server

import mackerel


@click.group()
@click.version_option(message=f'{mackerel.__title__} {mackerel.__version__}')  # type: ignore # noqa
@click.pass_context
def cli(ctx: click.core.Context) -> None:
    """
    Mackerel is a minimal static site generator written in typed Python 3.6+.
    """
    ctx.obj = {}


@cli.command()
@click.argument('SITE_PATH', type=click.Path(exists=False, resolve_path=True))
@click.pass_context
def init(ctx: click.core.Context, site_path: str) -> None:
    """Create an new mackerel site"""
    output_path = Path(site_path)
    sample_site_path = Path(os.path.dirname(
        os.path.realpath(mackerel.__file__))) / 'site'
    try:
        shutil.copytree(src=sample_site_path, dst=output_path)
    except FileExistsError as e:
        ctx.fail(f'Initialize failed, file {e.filename} already exists')

    click.echo(f'Initialized empty mackerel site in {output_path}')


@cli.command()
@click.argument('SITE_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--dry-run', default=False, is_flag=True,
              help='Make a build without persisting any files.')
@click.pass_context
def build(ctx: click.core.Context, site_path: str, dry_run: bool) -> None:
    """Build the contents of SITE_PATH"""
    site = mackerel.site.Site(path=Path(site_path))

    if site.output_path.exists():
        click.confirm(
            f'Directory {str(site.output_path)} already exists, do you want '
            'to overwrite?', abort=True)

    build = mackerel.build.Build(site=site)
    build.execute(dry_run=dry_run)
    click.echo('Build finished.')


@cli.command()
@click.argument('SITE_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=8000,
              help='The port to bind to.')
@click.pass_context
def develop(ctx: click.core.Context, site_path: str, host: str,
            port: int) -> None:
    """Runs a local development server"""
    def rebuild_site() -> mackerel.site.Site:
        site = mackerel.site.Site(path=Path(site_path))
        build = mackerel.build.Build(site=site)
        build.execute()
        return site

    site = rebuild_site()
    server = Server()
    server.watch(str(site.content_path), rebuild_site)
    server.watch(str(site.template_path), rebuild_site)
    server.serve(host=host.strip(), port=port, root=str(site.output_path))


if __name__ == '__main__':
    cli()
