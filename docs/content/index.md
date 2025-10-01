---
title: Welcome
template: base
---

![Mackerel Logo](/assets/mackerel.svg "Mackerel Logo"){.logo}

# Mackerel

Mackerel is a minimal, typed static site generator built with Python.

Turn Markdown content into static sites, using templates for flexible presentation.


[![PyPI](https://img.shields.io/pypi/v/mackerel.svg)](https://pypi.org/project/mackerel/)
[![CI](https://github.com/pkolios/mackerel/actions/workflows/ci.yml/badge.svg)](https://github.com/pkolios/mackerel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![codecov](https://codecov.io/gh/pkolios/mackerel/branch/main/graph/badge.svg)](https://codecov.io/gh/pkolios/mackerel)

---

## Table of Contents

[TOC]

---

## Installation

### With pip

```bash
pip install mackerel
```

### With uv

```bash
uv add mackerel
```

### Use as tool (pipx, uvx)

Run directly without installing globally:

pipx:

```bash
pipx run mackerel --help
```

uvx:

```bash
uvx mackerel --help
```

---

## Usage

### Initialize a site

```bash
mackerel init my-site
```

Creates a new directory `my-site/` with a starter config, content, and templates.

### Build the site

```bash
cd my-site
mackerel build
```

This renders your content and templates into static HTML inside `_build/`.

Options:

* `--config PATH` – specify a config file (default: `mackerelconfig.toml`)
* `--yes` – overwrite existing `_build/` without confirmation
* `--dry-run` – run without writing files

### Run the development server

```bash
mackerel develop
```

Serves the built site at [http://127.0.0.1:8000](http://127.0.0.1:8000), with live rebuilds when content or templates change.

---

## Site Structure

A Mackerel site typically looks like this:

```
my-site/
├── content/                # Markdown content files
│   ├── index.md
│   ├── about.md
│   └── posts/
│       └── hello-world.md
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── page.html
│   └── list.html
├── mackerelconfig.toml     # Site configuration
└── _build/                 # Generated HTML output (after build)
```

---

## Configuration

The `mackerelconfig.toml` defines how your site is built:

```toml
[mackerel]
build_path = "_build"
build_suffix = ".html"
content_path = "content"
doc_suffix = ".md"
template_path = "templates/starter"
template_suffix = ".html"
content_renderer = "MarkdownRenderer"
template_renderer = "Jinja2Renderer"
navigation = [
    { label = "Home", url = "/", children = [] },
    { label = "About", url = "/about.html", children = [] },
]

[MarkdownRenderer]
output_format = "html"
extensions = ["markdown.extensions.meta", "markdown.extensions.extra"]

[Jinja2Renderer]
trim_blocks = true
lstrip_blocks = true

[user]
title = "My Site"
description = "A site built with Mackerel"
copyright = "2025 Me"
powered = "http://mackerel.sh"
```

### Key sections

* **[mackerel]**: core build settings (paths, suffixes, navigation)
* **[MarkdownRenderer]**: Markdown parser settings
* **[Jinja2Renderer]**: Template engine settings
* **[user]**: Custom fields available in templates (site title, description, etc.)

---

## Content Documents

Content lives in `content/` as Markdown files (`.md`):

```markdown
---
title: My First Post
template: page
created_at: 2025-01-01
categories: ["posts"]
excerpt: A short preview of my post.
---

# Hello World

Welcome to my site powered by **Mackerel**!
```

* **Front matter** (between `---`) defines metadata (`title`, `template`, `created_at`, etc.).
* **Body** is written in Markdown and gets rendered into HTML.
* Metadata supports drafts, categories, and lists of posts.

---

## Template Development

Templates are written in [Jinja2](https://jinja.palletsprojects.com/):

Inside templates you can access:

* `document`: the current page (HTML + metadata)
* `ctx.user`: values from `[user]` in config
* `ctx.nav`: navigation items
* `document.category_lists`: auto-generated lists of posts

Example snippet:

```html
<ul>
  {% for item in ctx.nav %}
    <li><a href="{{ item.url }}">{{ item.label }}</a></li>
  {% endfor %}
</ul>
```

See starter site & template for more.

---

Happy publishing with mackerel.
