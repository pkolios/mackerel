from typing import TYPE_CHECKING

import jinja2

from mackerel import exceptions
from mackerel.renderers.base import TemplateRenderer

if TYPE_CHECKING:
    from mackerel.site import Site  # noqa
    from mackerel import build, content  # noqa


class Jinja2Renderer(TemplateRenderer):
    def __init__(self, site: 'Site') -> None:
        template_path = site.template_path  # Type: Path
        trim_blocks = site.config.getboolean('Jinja2Renderer', 'TRIM_BLOCKS')
        lstrip_blocks = site.config.getboolean(
            'Jinja2Renderer', 'LSTRIP_BLOCKS')
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_path.resolve())),
            trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks,)

    def render(self, ctx: 'build.Context',
               document: 'content.Document') -> str:
        try:
            template = self.env.get_template(document.template)
        except jinja2.exceptions.TemplateNotFound:
            raise exceptions.RenderingError(
                f'Template file `{document.template}` for document '
                f'`{document.document_path}` not found')
        return template.render(ctx=ctx, document=document)
