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
@click.argument('SOURCE_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--dry-run', default=False, is_flag=True,
              help='Make a build without persisting any files.')
@click.pass_context
def build(ctx: click.core.Context, source_path: str, dry_run: bool) -> None:
    """Builds the contents of SOURCE_PATH and stores them in OUTPUT_PATH"""
    source = mackerel.content.Source(path=Path(source_path))
    if ctx.obj.get('VERBOSE'):
        click.echo('- Configuration:')
        for key, value in source.config['mackerel'].items():
            click.echo(f'    - {key}: {value}')

    build = mackerel.build.Build(
        source=source, document_renderer=mackerel.renderers.MarkdownRenderer(),
        template_renderer=mackerel.renderers.Jinja2Renderer(
            template_path=Path(source.template_path)))
    build.execute(dry_run=dry_run)


if __name__ == '__main__':
    cli()
