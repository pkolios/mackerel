Title: Welcome
Copyright: 2017 Paris Kolios
Template: layout.html

# Mackerel

Mackerel is a minimal static site generator written in typed Python 3.6+.

[![Latest Version](https://img.shields.io/pypi/v/mackerel.svg)](https://pypi.python.org/pypi/mackerel/)
[![Build Status](https://travis-ci.org/pkolios/mackerel.svg?branch=master)](https://travis-ci.org/pkolios/mackerel)
[![Coverage Status](https://coveralls.io/repos/pkolios/mackerel/badge.svg?branch=master)](https://coveralls.io/r/pkolios/mackerel)

## Installation

This part of the documentation covers the installation of Mackerel.

### pip install

To install Mackerel, simply run this command in your terminal of choice:

```
$ pip install mackerel
```

If you don't have pip installed, this [pip installation guide](https://pip.pypa.io/en/stable/installing/) can guide you through the process.

### Get the Source Code

Mackerel is developed on GitHub, where the [source code is available](https://github.com/pkolios/mackerel).

You can clone the public repository:

```
$ git clone git@github.com:pkolios/mackerel.git
```

Once you have a copy of the repository you can install it:

```
$ cd mackerel
$ pip install -e .
```

## Basic Usage

After succesfully installing mackerel you can use the mackerel cli to initialize a new site or build an existing one.

### Start a new site

Mackerel's cli provides with an `init` command that generates a new site under the given directory name.

```
$ mackerel init ~/my_site
```

The mackerel directory structure looks like this:

```
.
├── .mackerelconfig  # The configuration file of this site
├── content  # The site's content
└── template  # The site's template
```

You can have a look at the generated `.mackerelconfig` file and `content` directory and alter them to your liking.
For further documentation regarding the template development see the Template development section.

### Build your site

The new site already contains some demo content and a template. The `build` command will build the site.

```
$ mackerel build ~/my_site
```

The static site will be generated inside the `_build` directory of the site.
You can use python's simple http server to preview the site locally.

```
$ cd ~/my_site/_build
$ python -m SimpleHTTPServer
```

### Create a new page or post

Using your favorite editor, create a new `.md` file anywhere in the site's `content` directory.
Make sure the new file has the `.md` file extension. The content file has two sections.
The top section that contains metadata keys and values related to this document.

```
Title: New page
Author: John Doe
Date: December 31, 2099
Template: page.html
Custom_meta: Nyancat

...
```

And the main section that contains the actual content.

```
...

This is the main content of this document written in Markdown.
```

## Configuration

The `.mackerelconfig` file contains the configuration for the site

```
[mackerel]
    OUTPUT_PATH = _build  # Sets the build output directory
    CONTENT_PATH = content  # Specifies the site's content directory
    TEMPLATE_PATH = template  # Specifies the site's template directory

[navigation]  # This section is used to define navigation menus for the template
    main = index.md, about.md  # The main navigation consists of the index and the about documents

[user]  # This section contains all the user / template site-wide settings
    title = Mackerel Example Site  # The site's title
    description = A beautiful narrative written with Mackerel. The story begins here.  # The site's description
    logo = img/logo.svg  # The path to the site's logo inside the content directory
    url = http://localhost:8000/  # The site's url (supports sub directories ex. /blog/)
    copyright = 2017 Paris Kolios  # Site-wide copyright string
    powered = https://github.com/pkolios/mackerel  # Site-wide powered-by string
```

## Template development

Currently the chosen template engine is [Jinja2](http://jinja.pocoo.org/).
When rendering the content files, Mackerel passes the following objects to the template:

* `document` - the document that is currently being generated
* `ctx` - the context object that contains the navigation & config objects
    * `ctx.nav` - the navigation object
    * `ctx.cfg` - the config parser object


## Built With

* [Python 3](https://www.python.org/)
* [mypy](http://mypy.readthedocs.io) Static type checker
* [Jinja2](http://jinja.pocoo.org/) Template engine
* [mistune](http://mistune.readthedocs.io) Markdown parser in pure Python

## Changelog

### Version 0.1

First preview release.

## License

See the [LICENSE](https://raw.githubusercontent.com/pkolios/mackerel/master/LICENSE) file for details.
