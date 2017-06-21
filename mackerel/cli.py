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
@click.pass_context
def cli(ctx: click.core.Context, debug: bool, verbose: bool) -> None:
    # TODO: cli description text
    ctx.obj = {}
    ctx.obj['VERBOSE'] = verbose


@cli.command()
@click.argument('SITE_PATH', type=click.Path(exists=False, resolve_path=True))
@click.pass_context
def init(ctx: click.core.Context, site_path: str) -> None:
    """Create an empty mackerel site"""
    output_path = Path(site_path)
    if output_path.exists():
        raise click.UsageError('Directory {s} already exists.'.format(
            s=site_path))

    sample_site_path = Path(os.path.dirname(
        os.path.realpath(__file__))).parent / 'tests' / 'site'
    shutil.copytree(src=sample_site_path, dst=output_path)
    click.echo('Initialized empty mackerel site in {}'.format(output_path))


@cli.command()
@click.argument('SITE_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--dry-run', default=False, is_flag=True,
              help='Make a build without persisting any files.')
@click.pass_context
def build(ctx: click.core.Context, site_path: str, dry_run: bool) -> None:
    """Builds the contents of SITE_PATH"""
    site = mackerel.site.Site(path=Path(site_path))
    if ctx.obj.get('VERBOSE'):
        click.echo('- Configuration:')
        for key, value in site.config['mackerel'].items():
            click.echo(f'    - {key}: {value}')

    if site.output_path.exists():
        click.confirm(
            'Directory {b} already exists, do you want to overwrite?'.format(
                b=str(site.output_path)), abort=True)

    build = mackerel.build.Build(
        site=site, document_renderer=mackerel.renderers.MarkdownRenderer(),
        template_renderer=mackerel.renderers.Jinja2Renderer(
            template_path=Path(site.template_path)))
    build.execute(dry_run=dry_run)


if __name__ == '__main__':
    cli()
