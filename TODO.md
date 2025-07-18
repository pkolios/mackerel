# Next

- Update cli module
    - test build cmd
    - make "-v" option work regardless where it is placed?
    - develop cmd
        - use more modern dev server / file watch?
    - fix typing errors on cli

- Add minimal demo site
    - With minimal base template (little to no css, but acceptable look)
    - Demo content for all supported features

- Handle listing of pages
    - Pass url to the page listing for linking

- Adjust build cli to support multiple renderers

- Use protocols instead of dataclasses in types
    - This way types is purely about typing

- Add pagination support for collections

- Add exception handling
    - https://chatgpt.com/g/g-p-68720c48b3d88191a30af2ffd2f3b792-mackerel/c/687cabcf-5ba0-8001-a76b-5069f835f8f2

- Check / remove MANIFEST.in

# Other

- [x] Remove template context specific settings from config?
- [x] Switch to using front matter for the content meta data
    - [x] Figure out expected front matter schema / model

- [x] Overhaul typing
    - [x] Turn Site into dataclass OR create a site protocol
    - [x] Use protocols for document and template render

- [ ] Change the default template
    - [ ] Use plain html default template with common use case examples
        - [ ] Homepage
        - [ ] Post page
        - [ ] About page
        - [ ] Page listing
        - [ ] Navigation

- [ ] Move default site to different path / name
- [ ] Make adding & configuring templates / themes easy
    - [ ] As simple as pip install mackerel-theme-name?
    - [ ] Dropping the files in the templates folder

- [ ] Add instructions on how to use without installing
    - [ ] uvx / pipx
    - [ ] docker with uv image and uvx command
    - [ ] nix / nix packages
    - [ ] Test installation methods automatically

- [ ] Replace travis with github actions
    - [ ] Update badges in README.md
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
- [x] Add professional logging & cli verbosity flag
- [ ] Add linter support in generated site (markdown, template)

- [ ] Add deploy command driven by config / env vars
    - [ ] Deploy to github pages
    - [ ] Cloudflare pages
    - [ ] Render static pages
    - [ ] Netlify

- First post ideas
    - [ ] How is this website made (article about mackerel)
    - [ ] Things that fit in a single file but probably shouldn't (article of presentation)

- [ ] Implement in go
