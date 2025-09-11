"""A module for all provided parsers."""

from pathlib import Path
from typing import Any
from typing import cast

import frontmatter  # type: ignore[import-untyped]  # TODO: remove when frontmatter gets types

from mackerel import types as t


class PythonFrontmatterParser(t.MetadataParser):
    """Python frontmatter based parser."""

    def parse(self, raw: str) -> t.DocumentMetadata:
        """Parse the frontmatter from a document file."""
        # TODO: Allow extra custom attributes
        raw_metadata, _ = frontmatter.parse(raw)
        metadata = cast("dict[str, Any]", raw_metadata)
        return t.DocumentMetadata(
            title=t.Title(metadata["title"]),
            template=Path(metadata["template"]),
            created_at=t.CreatedAt(str(metadata["created_at"]))
            if "created_at" in metadata
            else None,
            modified_at=t.ModifiedAt(str(metadata["modified_at"]))
            if "modified_at" in metadata
            else None,
            draft=bool(metadata.get("draft", False)),
            excerpt=t.Excerpt(metadata.get("excerpt", ""))
            if "excerpt" in metadata
            else None,
            categories=[t.Category(cat) for cat in metadata.get("categories", [])],
            category_lists=[
                t.CategoryList(
                    name=t.Category(cat["name"]),
                    sort_by=cat.get("sort_by"),
                    order=cat.get("order", "desc"),
                )
                for cat in metadata.get("category_lists", [])
            ],
        )
