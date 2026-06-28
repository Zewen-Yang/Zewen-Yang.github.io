# Personal Academic Website — Setup & Maintenance Guide

A practical, task-oriented guide for turning this `al-folio` v1 starter into your own
personal academic website, and for maintaining it afterwards.

This guide is split into focused pages so you only read what you need:

| Page                                                            | When to read it                                                                                                                        |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| [01 — Toolchain setup](01-toolchain-setup.md)                   | First time only. Install Ruby/Bundler/Node/Python and get a clean local build + dev server.                                            |
| [02 — Content editing](02-content-editing.md)                   | Day-to-day. Edit the homepage, publications, CV, news, projects, and posts (with real gotchas we hit).                                 |
| [03 — Theming & overrides](03-theming-overrides.md)             | When you change colors/look, or edit any plugin-owned file. Covers the Dracula theme and the `.al-folio-overrides.yml` audit workflow. |
| [04 — Own the repo & pull updates](04-git-fork-and-upstream.md) | One-time git setup to make this your own repo while still pulling al-folio updates (`origin`/`upstream`), plus GitHub Pages.           |

## Mental model (read this once)

In al-folio **v1**, this repository is a **thin starter**, not a theme. The runtime —
layouts, includes, Sass, Liquid tags, feature JS — lives in versioned **gems**
(`al_folio_core` and the `al_*` plugins). So:

- **Prefer editing config, data, content, and images** in this repo. They are yours.
- **Avoid copying plugin-owned files** (`_layouts`, `_includes`, `_sass`, JS) into the
  repo unless you _intentionally_ want a local override — and if you do, you must run the
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

## Formatting (Prettier) — avoid the red CI run

The GitHub Actions deploy runs `npx prettier . --check` as a gate. It only **checks**
formatting (indentation, quotes, line wrapping, etc.) — it never edits files. Any file
that doesn't match the rules in `.prettierrc` makes that step exit non-zero and turns the
whole workflow red. This is the most common "my deploy failed first try" cause, and it
usually happens after hand-editing `_config.yml`, `_data/cv.yml`, posts, or docs.

### Fix existing formatting issues

```bash
npx prettier . --write   # auto-format every file in place
npm run lint:prettier    # confirm it now passes (same check CI runs)
```

### Format on save (so it never happens again)

This repo ships `.vscode/settings.json` enabling **format on save** with Prettier for
Markdown, YAML, and Liquid files. To use it:

1. Install the **Prettier - Code formatter** extension (`esbenp.prettier-vscode`) in
   Cursor / VS Code.
2. Reload the editor. From then on, saving a file (⌘S) auto-formats it to match
   `.prettierrc`, so you never push unformatted files.

If you edit files outside the editor (scripts, other tools), still run
`npm run lint:prettier` before committing.
