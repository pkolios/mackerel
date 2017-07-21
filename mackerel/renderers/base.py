from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from mackerel import build, content  # noqa
    from mackerel.site import Site  # noqa


class DocumentRenderer:
    def __init__(self, site: 'Site') -> None:
        raise NotImplementedError

    def extract_metadata(self, text: str) -> Dict[str, str]:
        """
        Extract the metadata from the top of the document and return a
        dictionary with lower cased keys.
        """
        raise NotImplementedError

    def render(self, text: str) -> str:
        raise NotImplementedError


class TemplateRenderer:
    def __init__(self, site: 'Site') -> None:
        raise NotImplementedError

    def render(self, ctx: 'build.Context',
               document: 'content.Document') -> str:
        raise NotImplementedError
