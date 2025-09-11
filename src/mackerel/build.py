"""The build module contains functions for building the static site."""

import datetime as dt
import logging
import shutil
from collections.abc import Callable
from collections.abc import Generator
from functools import wraps
from itertools import chain
from pathlib import Path

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_datetime

from mackerel import types as t
from mackerel.config import AppConfig

logger = logging.getLogger(__name__)


def copy_static_file(
    f: t.StaticFile | t.TemplateAsset,
    relative_path: t.ContentPath | t.TemplatePath,
    build_path: t.BuildPath,
    dry_run: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """Copy a static file to the build directory."""
    # Plugin hook pre static file handling here
    logger.info("Copying static file: %s", f)
    target_path = build_path / f.relative_to(relative_path)
    if dry_run:
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=f, dst=target_path)
    # Plugin hook post static file handling here


def read_document(
    f: t.DocumentFile,
    cfg: AppConfig,
    content_renderer: t.ContentRenderer,
    metadata_parser: t.MetadataParser,
) -> tuple[t.BuildPath, t.RenderedDocument]:
    """Read and parse document files."""
    logger.info("Processing document file: %s", f)
    # Plugin hook pre document file parsing here
    raw = f.read_text()
    target_path = cfg.mackerel.build_path / f.relative_to(
        cfg.mackerel.content_path,
    ).with_suffix(
        cfg.mackerel.build_suffix,
    )
    url = t.RelativeURL(
        str(Path("/") / target_path.relative_to(cfg.mackerel.build_path).as_posix())
    )
    # Plugin hook post document file parsing here
    return target_path, t.RenderedDocument(
        url=url,
        html=content_renderer.render(raw),
        metadata=metadata_parser.parse(raw),
    )


def write_documents(
    docs: dict[t.BuildPath, t.RenderedDocument],
    cfg: AppConfig,
    template_renderer: t.TemplateRenderer,
    dry_run: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """Write the final documents html to the build path."""
    # Plugin hook pre documents file writing here
    ctx = t.TemplateContext(
        user=cfg.user,
        nav=cfg.mackerel.navigation,
    )
    for target_path, doc in docs.items():
        if doc.metadata.draft:
            logger.info("Skipping draft document: %s", target_path)
            continue
        logger.info("Writing document: %s", target_path)
        build_doc = t.BuildDocument(
            url=doc.url,
            html=doc.html,
            metadata=doc.metadata,
            category_lists=[
                create_category_items(category_list, docs)
                for category_list in doc.metadata.category_lists
            ],
        )
        html = template_renderer.render(ctx=ctx, document=build_doc)
        if dry_run:
            return
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(html)
    # Plugin hook post documents file writing here


def _parse_sort_value(doc: t.RenderedDocument, field: str) -> str | dt.datetime:
    meta = doc.metadata

    if field == "title":
        return meta.title

    if field in ("created_at", "modified_at"):
        raw_value = getattr(meta, field)
        if raw_value is not None:
            try:
                return parse_datetime(raw_value)
            except ParserError:
                return dt.datetime.min.replace(tzinfo=dt.UTC)

    return ""  # fallback for unknown field


def cache_by_category_signature(
    fn: Callable[
        [t.CategoryList, dict[t.BuildPath, t.RenderedDocument]],
        t.BuildCategoryList,
    ],
) -> Callable[
    [t.CategoryList, dict[t.BuildPath, t.RenderedDocument]],
    t.BuildCategoryList,
]:
    """Custom cache decorator that keys only by category name, sort_by, and order."""
    cache: dict[tuple[str, str | None, str], t.BuildCategoryList] = {}

    @wraps(fn)
    def wrapper(
        category_list: t.CategoryList,
        docs: dict[t.BuildPath, t.RenderedDocument],
    ) -> t.BuildCategoryList:
        key = (category_list.name, category_list.sort_by, category_list.order)
        if key in cache:
            return cache[key]

        result = fn(category_list, docs)
        cache[key] = result
        return result

    return wrapper


@cache_by_category_signature
def create_category_items(
    category_list: t.CategoryList,
    docs: dict[t.BuildPath, t.RenderedDocument],
) -> t.BuildCategoryList:
    """Create the sorted list of rendered documents for a category."""
    # Filter matching documents
    items = [
        doc for doc in docs.values() if category_list.name in doc.metadata.categories
    ]

    # Apply sorting if requested
    if category_list.sort_by:
        items.sort(
            key=lambda doc: _parse_sort_value(doc, category_list.sort_by),
            reverse=(category_list.order == "desc"),
        )

    return t.BuildCategoryList(
        name=category_list.name,
        sort_by=category_list.sort_by,
        order=category_list.order,
        items=items,
    )


def fetch_content_files(
    content_path: Path,
    doc_suffix: t.DocSuffix,
) -> Generator[t.ContentFile, None, None]:
    """Fetch content files from the specified path."""
    files = (f for f in content_path.rglob("*") if f.is_file())
    for f in files:
        yield t.DocumentFile(f) if f.suffix == doc_suffix else t.StaticFile(f)


def fetch_template_assets(
    template_path: t.TemplatePath,
    template_suffix: t.TemplateSuffix,
) -> Generator[t.TemplateAsset, None, None]:
    """Fetch template files from the specified path."""
    files = (f for f in template_path.rglob("*") if f.is_file())
    for f in files:
        if f.suffix != template_suffix:
            yield t.TemplateAsset(f)


def build(
    cfg: AppConfig,
    content_renderer: t.ContentRenderer,
    metadata_parser: t.MetadataParser,
    template_renderer: t.TemplateRenderer,
    dry_run: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """Build the site."""
    # Plugin hook pre build here
    docs: dict[t.BuildPath, t.RenderedDocument] = {}
    for f in chain(
        fetch_template_assets(
            template_path=cfg.mackerel.template_path,
            template_suffix=cfg.mackerel.template_suffix,
        ),
        fetch_content_files(
            content_path=cfg.mackerel.content_path,
            doc_suffix=cfg.mackerel.doc_suffix,
        ),
    ):
        match f:
            case t.StaticFile():
                copy_static_file(
                    f=f,
                    relative_path=cfg.mackerel.content_path,
                    build_path=cfg.mackerel.build_path,
                    dry_run=dry_run,
                )
            case t.TemplateAsset():
                copy_static_file(
                    f=f,
                    relative_path=cfg.mackerel.template_path,
                    build_path=cfg.mackerel.build_path,
                    dry_run=dry_run,
                )
            case t.DocumentFile():
                try:
                    target_path, document = read_document(
                        f=f,
                        cfg=cfg,
                        content_renderer=content_renderer,
                        metadata_parser=metadata_parser,
                    )
                except Exception:
                    logger.exception("Error reading document %s", f)
                else:
                    docs[target_path] = document
    write_documents(
        docs=docs,
        cfg=cfg,
        template_renderer=template_renderer,
        dry_run=dry_run,
    )
    # Plugin hook post build here
