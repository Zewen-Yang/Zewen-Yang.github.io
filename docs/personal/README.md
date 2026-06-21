# Personal Academic Website — Setup & Maintenance Guide

A practical, task-oriented guide for turning this `al-folio` v1 starter into your own
personal academic website, and for maintaining it afterwards.

This guide is split into focused pages so you only read what you need:

| Page | When to read it |
| ---- | --------------- |
| [01 — Toolchain setup](01-toolchain-setup.md) | First time only. Install Ruby/Bundler/Node/Python and get a clean local build + dev server. |
| [02 — Content editing](02-content-editing.md) | Day-to-day. Edit the homepage, publications, CV, news, projects, and posts (with real gotchas we hit). |
| [03 — Theming & overrides](03-theming-overrides.md) | When you change colors/look, or edit any plugin-owned file. Covers the Dracula theme and the `.al-folio-overrides.yml` audit workflow. |

## Mental model (read this once)

In al-folio **v1**, this repository is a **thin starter**, not a theme. The runtime —
layouts, includes, Sass, Liquid tags, feature JS — lives in versioned **gems**
(`al_folio_core` and the `al_*` plugins). So:

- **Prefer editing config, data, content, and images** in this repo. They are yours.
- **Avoid copying plugin-owned files** (`_layouts`, `_includes`, `_sass`, JS) into the
  repo unless you *intentionally* want a local override — and if you do, you must run the
  override audit (see [page 03](03-theming-overrides.md)).

### Files and folders you will actually touch

```text
_config.yml              # main site configuration (name, urls, plugins, flags)
_pages/about.md          # homepage / about page (layout: about)
_pages/cv.md             # CV page wrapper (chooses rendercv vs jsonresume)
_data/cv.yml             # CV content (rendercv format)
_bibliography/papers.bib # publications in BibTeX
_news/                   # short news items (shown on homepage)
_posts/                  # blog posts
_projects/               # project pages
_pages/awards.md         # awards page
assets/img/              # images, including the profile photo
Gemfile                  # Ruby dependencies (pinned gem versions)
package.json             # Node tooling
.al-folio-overrides.yml  # tracks any plugin file you override locally (commit it!)
```

## Recommended editing order (new site)

1. Toolchain — see [page 01](01-toolchain-setup.md)
2. `_config.yml` — name, `url`, `baseurl`, socials, feature flags
3. `_pages/about.md` + profile photo in `assets/img/`
4. `_bibliography/papers.bib` — publications
5. `_data/cv.yml` — CV
6. `_news/` — news items
7. `_projects/` / `_posts/` — projects and blog
8. Theming — see [page 03](03-theming-overrides.md) (optional)
9. Deploy settings — see [page 01](01-toolchain-setup.md#deploy-with-github-pages)

## Validate before every commit / deploy

```bash
npm run lint:prettier
bundle exec jekyll build --baseurl /al-folio
bundle exec al-folio upgrade overrides audit   # only matters if you have local overrides
```
