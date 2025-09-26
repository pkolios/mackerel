# Next

- Write docs
    - Add pymdownx to the doc group dependencies
    - Use https://github.com/asiffer/mkdocs-shadcn for theming
    - Look into https://mkdocstrings.github.io/ generating cli & api docs

- Adjust build cli to support multiple renderers
    - markdown-it-py renderer
        - https://markdown-it-py.readthedocs.io/en/latest/
        - Make the default one? Replaces need for separate metadata parser
    - htpy html renderer

# TODO

- [x] Remove template context specific settings from config?
- [x] Switch to using front matter for the content meta data
    - [x] Figure out expected front matter schema / model

- [x] Overhaul typing
    - [x] Turn Site into dataclass OR create a site protocol
    - [x] Use protocols for document and template render

- [x] Change the default template
    - [x] Use plain html default template with common use case examples
        - [x] Homepage
        - [x] Post page
        - [x] About page
        - [x] Page listing
        - [x] Navigation

- [x] Move default site to different path / name

- [ ] Make adding & configuring templates / themes easy
    - [ ] As simple as pip install mackerel-theme-name?
    - [ ] Dropping the files in the templates folder

- [ ] Update docs
    - [ ] Use / port https://github.com/lepture/shibuya theme
    - [ ] Add instructions on how to use without installing
        - [ ] uvx / pipx
        - [ ] docker with uv image and uvx command
        - [ ] nix / nix packages
        - [ ] Test installation methods automatically

- [ ] Replace travis with github actions
    - [ ] Update badges in README.md

- [ ] Add RSS support

- [ ] Add pagination support for collections
    - Consider page & date based versions

- [ ] Verify coveralls badge works
    - [ ] Use github action for coverage ?

- [ ] Update documentation site after overhaul
    - [ ] Find a nice theme
    - [ ] Release theme template as doc theme

- [ ] Rewrite README.md with updated instructions

- [ ] Change branch name from master to main

- [ ] Add / extend release to cheeseshop
    - [ ] Generate github release
    - [ ] Publish to pypi

- [ ] Create pretty mackerel template / theme
    - [ ] Installable via pip & configuration

- [ ] Add htpy template renderer

- [ ] Support assets pipelines (minify, bundle etc)

- [x] Add logging & cli verbosity flag

- [ ] Add linter support in generated site (markdown, template)

- [ ] Add exception handling
    - [ ] https://chatgpt.com/g/g-p-68720c48b3d88191a30af2ffd2f3b792-mackerel/c/687cabcf-5ba0-8001-a76b-5069f835f8f2

- [ ] Support serving sites from sub directories
    - [ ] Leverage web server rewrite logic instead of handling it on the mackerel side

- [ ] Add deploy command driven by config / env vars
    - [ ] Deploy to github pages
    - [ ] Cloudflare pages
    - [ ] Render static pages
    - [ ] Netlify

- First post ideas
    - [ ] How is this website made (article about mackerel)
    - [ ] Things that fit in a single file but probably shouldn't (article of presentation)

- [ ] Implement in go
