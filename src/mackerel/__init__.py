"""Mackerel - A static site generator."""

from importlib.metadata import metadata
from importlib.metadata import version

__version__ = version("mackerel")
_meta = metadata("mackerel")

__title__ = _meta.get("Name", "mackerel")
__description__ = _meta.get("Summary")
__author__ = _meta.get("Author")
__author_email__ = _meta.get("Author-email")
__license__ = _meta.get("License")
__url__ = _meta.get("Home-page", "http://mackerel.sh")

__all__ = [
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
]
