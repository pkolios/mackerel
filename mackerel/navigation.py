from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple  # noqa
    from mackerel.build import BuildDocument  # noqa


class Navigation:
    """Navigation provides methods to list and access the content"""
    def __init__(self, build_documents: 'Tuple[BuildDocument, ...]') -> None:
        self._build_documents = build_documents
