# mackerel

## Installation

Supported installation methods:

- uvx / pipx
- docker
- nix package

## Usage

CLI commands:

- init
- build
- develop
- deploy
- plugins
    - install
    - uninstall
    - list

## Core Features

### Templates

Supported template engines:

- Jinja
- htpy

### Content Languages

Supported content languages:

- Markdown

### Content Management with Front Matter

Supported metadata:

- YAML
- TOML
- JSON

Supported schema:

[WIP schema]: #

- title
- date
- modified
- template
- tags
- draft

### Static Asset Handling

-  Copying files directly in the build folder
-  Minifying css / js
-  Bundling assets into fewer files
-  Optimizing images automatically

### Navigation

- Folder / file based
- Metadata (front matter) based
- Pagination
    - Use front matter in an index.md file to specify which content to list,
      template to use, what to paginate over and how many items per page.
- Linking content to content
- Linking assets in content

### RSS & Atom Feed Generation

- As a plugin

## Advanced Features

### Content & Template Checks

- Broken links
- Content linting
- Template linting
- Optional pre-commit hook installation for project dir (plugin)

### Incremental Builds

- Detect and rebuild only changed content / templates / assets

### Deployment Hooks

- Direct deploy via cli command
- CI/CD pipeline definition for building & deploying on push

Services to support:

- Github pages
- Cloudflare pages
- Render static pages


## Plugin System

To support extending / hooking into the execution of mackerel. Use Simon Willison's llm plugins approach.

- Templates engines
- Content languages
- CLI commands
- Asset handlers
