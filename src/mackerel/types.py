"""The types and protocols of Mackerel."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Literal
from typing import NewType
from typing import Protocol


# Files
# Using subclasses for type distinction since NewType does not support
# isinstance checks and structural pattern matching.
class StaticFile(Path):
    """A static file that is not processed by the content renderer."""


class DocumentFile(Path):
    """A document file that is processed by the content renderer."""


class TemplateAsset(Path):
    """A template asset file that is used for rendering documents."""


ContentFile = StaticFile | DocumentFile

# Content
Title = NewType("Title", str)
CreatedAt = NewType("CreatedAt", str)
ModifiedAt = NewType("ModifiedAt", str)
HTML = NewType("HTML", str)
Excerpt = NewType("Excerpt", str)
Category = NewType("Category", str)

ContentPath = NewType("ContentPath", Path)


@dataclass(frozen=True, slots=True)
class CategoryList:
    """Represents the list of categories available to render."""

    name: Category
    sort_by: Literal["title", "created_at", "modified_at"] = "title"
    order: Literal["asc", "desc"] = "desc"


@dataclass(frozen=True, slots=True)
class DocumentMetadata:
    """Represents the document metadata."""

    title: Title
    template: Path
    created_at: CreatedAt | None = None
    modified_at: ModifiedAt | None = None
    draft: bool = False
    excerpt: Excerpt | None = None
    categories: list[Category] = field(default_factory=list)
    category_lists: list[CategoryList] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RenderedDocument:
    """Represents a document rendered content and parsed metadata."""

    url: RelativeURL
    html: HTML
    metadata: DocumentMetadata


@dataclass(frozen=True, slots=True)
class BuildCategoryList(CategoryList):
    """Represents a category list for building the site."""

    items: list[RenderedDocument] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class BuildDocument(RenderedDocument):
    """Represents a document ready for template rendering."""

    category_lists: list[BuildCategoryList] = field(default_factory=list)


# Navigation
Label = NewType("Label", str)
AbsoluteURL = NewType("AbsoluteURL", str)
RelativeURL = NewType("RelativeURL", str)
URL = AbsoluteURL | RelativeURL


@dataclass(frozen=True, slots=True)
class NavItem:
    """Represents a navigation item in the site structure."""

    label: Label
    url: URL | None = None
    children: list[NavItem] = field(default_factory=list)


# Template
TemplatePath = NewType("TemplatePath", Path)
TemplateSuffix = NewType("TemplateSuffix", str)
UserConfig = NewType("UserConfig", dict[str, Any])


@dataclass(frozen=True, slots=True)
class TemplateContext:
    """Context for rendering templates."""

    user: UserConfig = field(default_factory=lambda: UserConfig({}))
    nav: list[NavItem] = field(default_factory=list)


class TemplateRenderer(Protocol):
    """Protocol for rendering templates."""

    @abstractmethod
    def render(self, ctx: TemplateContext, document: BuildDocument) -> HTML:
        """Render the content with the given metadata using a template."""


# Renderers
DocSuffix = NewType("DocSuffix", str)
BuildSuffix = NewType("BuildSuffix", str)


class ContentRenderer(Protocol):
    """Protocol for rendering content files."""

    @abstractmethod
    def render(self, raw: str) -> HTML:
        """Render the raw content into HTML."""
        ...


class MetadataParser(Protocol):
    """Protocol for parsing metadata from content files."""

    @abstractmethod
    def parse(self, raw: str) -> DocumentMetadata:
        """Parse the metadata of the document into a DocumentMetadata object."""
        ...


# Build
BuildPath = NewType("BuildPath", Path)
