import os
import shutil
from pathlib import Path

import click

import mackerel


@click.group()
@click.option('--debug', '-d', default=False, is_flag=True,
              help='Enable the debug mode.')
@click.option('--verbose', '-v', default=False, is_flag=True,
              help='Enable the verbose mode.')
@click.version_option(message=f'{mackerel.__title__} {mackerel.__version__}')  # type: ignore # noqa
@click.pass_context
def cli(ctx: click.core.Context, debug: bool, verbose: bool) -> None:
    """
    Mackerel is a minimal static site generator written in typed Python 3.6+.
    """
    ctx.obj = {}
    ctx.obj['VERBOSE'] = verbose


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
    if ctx.obj.get('VERBOSE'):
        click.echo('- Configuration:')
        for key, value in site.config['mackerel'].items():
            click.echo(f'    - {key}: {value}')

    if site.output_path.exists():
        click.confirm(
            f'Directory {str(site.output_path)} already exists, do you want '
            'to overwrite?', abort=True)

    build = mackerel.build.Build(site=site)
    build.execute(dry_run=dry_run)
    click.echo('Build finished.')


if __name__ == '__main__':
    cli()
