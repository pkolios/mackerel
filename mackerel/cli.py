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
    ctx.obj['DEBUG'] = debug
    ctx.obj['VERBOSE'] = verbose
    if ctx.obj.get('VERBOSE'):
        click.echo('- CLI Arguments')
        for key in ctx.obj:
            click.echo(f'    - {key}: {ctx.obj[key]}')


@cli.command()
@click.argument('CONTENT_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.argument('OUTPUT_PATH', type=click.Path(
    exists=False, file_okay=False, writable=True, resolve_path=True))
@click.argument('TEMPLATE_PATH', type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.option('--dry-run', default=False, is_flag=True,
              help='Make a build without persisting any files.')
@click.pass_context
def build(ctx: click.core.Context, content_path: str, output_path: str,
          template_path: str, dry_run: bool) -> None:
    """Builds the contents of CONTENT_PATH and stores them in OUTPUT_PATH"""
    ctx.obj['CONTENT_PATH'] = content_path
    ctx.obj['OUTPUT_PATH'] = output_path
    ctx.obj['TEMPLATE_PATH'] = template_path
    ctx.obj['DRY_RUN'] = dry_run
    config = mackerel.helpers.make_config(path=None, ctx=ctx)
    if ctx.obj.get('VERBOSE'):
        click.echo('- Configuration:')
        for key, value in config['mackerel'].items():
            click.echo(f'    - {key}: {value}')

    source = mackerel.content.Source(path=Path(content_path))
    build = mackerel.build.Build(
        source=source, output_path=Path(output_path),
        document_renderer=mackerel.renderers.MarkdownRenderer(),
        template_renderer=mackerel.renderers.Jinja2Renderer(
            template_path=Path(template_path)))
    build.execute(dry_run=dry_run)


if __name__ == '__main__':
    cli()
