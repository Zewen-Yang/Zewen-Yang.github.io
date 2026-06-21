# 02 — Content Editing

Day-to-day editing of the homepage, publications, CV, news, projects, and posts. The
gotchas below are real ones encountered while building this site.

## Homepage / About (`_pages/about.md`)

`_pages/about.md` uses `layout: about` and has `permalink: /`, so it **is** your
homepage. The front matter controls the page; the Markdown body below it is your bio.

Front matter you will actually change:

```yaml
subtitle: AI Researcher ｜ Robotic Control Engineer   # tagline under your name
profile:
  align: right
  image: prof_pic_zewen.jpg     # file in assets/img/ (see "Profile photo" below)
  image_circular: false
  more_info: false
selected_papers: true           # shows papers marked selected={true} in papers.bib
social: true                    # social icons at the bottom
announcements:
  enabled: true                 # the News list (from _news/)
  scrollable: true
  limit: 5
latest_posts:
  enabled: true                 # latest blog posts (from _posts/)
  limit: 3
```

Body tips that worked well here:

- Link names inline with Markdown: `supervised by Prof. [Sandra Hirche](https://en.wikipedia.org/wiki/Sandra_Hirche)`
  and `worked closely with Dr. [Stefan Sosnowski](https://scholar.google.com/...)`.
- Bold the themes you want to stand out: `**Machine Learning**` and `**Robotics**`.
- Keep the tone professional — avoid filler phrases like "quiet interest"; describe
  concrete work and motivation instead.

### Profile photo

The photo referenced by `profile.image` (and by `_data/cv.yml`'s `image`/`photo`) lives
in `assets/img/`. To swap it:

1. Drop your file into `assets/img/` (e.g. `prof_pic_zewen.jpg`).
2. Point `profile.image` in `_pages/about.md` at the **filename only** (no `assets/img/` prefix).
3. In `_data/cv.yml`, set `image: prof_pic_zewen.jpg` and `photo: ../assets/img/prof_pic_zewen.jpg`.

> Filenames are case-sensitive on the deployed Linux server even though macOS is
> case-insensitive. `prof_pic.JPG` vs `prof_pic.jpg` will build locally but 404 in
> production — keep the extension consistent with the actual file.

## Publications (`_bibliography/papers.bib`)

Publications are generated from BibTeX. Paste standard `@article` / `@inproceedings`
entries. al-folio reads a few **non-standard helper fields**:

```bibtex
@INPROCEEDINGS{Yang_ACC_2024_cooperative,
  author    = {Yang, Zewen and ... and Hirche, Sandra},
  booktitle = {2024 American Control Conference (ACC)},
  title     = {{Cooperative Learning with Gaussian Processes ...}},
  year      = {2024},
  doi       = {10.23919/ACC60939.2024.10644832},  # renders a DOI button
  abbr      = {ACC},                                # venue badge on the left
  note      = {<strong>Oral presentation</strong>},# small note under the entry
  selected  = {true},                               # show on homepage selected list
}
```

### Gotcha: a paper with no DOI but you still want a clickable link

Use the `html` field (or `url`) — it renders the same kind of link button as `doi`, so
the title/badge becomes clickable even when there's no DOI:

```bibtex
html = {https://dl.acm.org/doi/10.5555/3635637.3663066},
```

### Gotcha: importing from RIS (`TY  - JOUR ...`)

A RIS export is **not** BibTeX. Convert it (the `TY  - JOUR` / `AU  -` / `TI  -` block)
into a proper `@article{...}` entry before pasting into `papers.bib`, mapping:
`TY JOUR → @article`, `AU → author` (one `and`-joined list), `TI → title`,
`JO/T2 → journal`, `PY → year`, `DO → doi`.

## CV

The CV page is **data-driven**, not a Markdown page. Two pieces:

- `_pages/cv.md` — just a wrapper. The key field is `cv_format`:

```yaml
layout: cv
cv_format: rendercv   # options: rendercv, jsonresume
cv_pdf: /assets/pdf/example_pdf.pdf
toc:
  sidebar: left
```

- `_data/cv.yml` — the actual content (rendercv format). `jsonresume` would instead read
  `assets/json/resume.json`. Pick one with `cv_format`; edit the matching file.

### Section order

Section order on the rendered page **follows the key order under `sections:`** in
`_data/cv.yml`. To reorder (e.g. put Experience above Education), just move the whole
YAML block up/down — there is no separate ordering config.

```yaml
cv:
  sections:
    Education:   [...]
    Experience:  [...]
    Skills:      [...]
    Languages:   [...]
    Publications:
      - summary: "See the full list on my [Publications page](../publications/)."
    Awards:
      - summary: "See the full list on my [Awards page](../awards/)."
    Interests:   [...]
```

### Gotchas

- **Keep your "current position" in sync in three places:** `_data/cv.yml` (`label`,
  `summary`, and the top `Experience` entry), `_pages/about.md` body, and `_config.yml`
  description if it mentions a role.
- **`end_date: present`** for the current job; use ISO dates (`2026-01-01`) otherwise.
  Watch for invalid dates like `2022-11-31` (November has 30 days) — they can break
  date rendering.
- **A `url:` that doesn't open** is usually a typo or a missing scheme. Use a full
  `https://...` URL; a bare domain or a relative path may not render as a link.
- **Multi-line highlights** use YAML block scalars (`|`) and can contain Markdown,
  including links and nested bullet lists (see the project highlights in `cv.yml`).
- Sections you don't want are commented out at the bottom of `cv.yml` (Volunteer,
  Certificates, Projects, References) — uncomment to enable.

## News (`_news/`)

Each file is a short, dated item shown in the homepage "News" list. Name files so they
sort chronologically (e.g. `202605_ICRA_Finalist.md`). Minimal `inline` item:

```markdown
---
layout: post
date: 2026-05-15 12:00:00+0800
inline: true
related_posts: false
---

Our paper [RCM Constraint-Consistent Dynamic Control in Surgical Robots](https://arxiv.org/abs/2509.14075)
has been selected as a finalist for the **Best Paper Award in Medical Robotics** at
ICRA 2026! 🏆 ([see the award finalists](https://2026.ieee-icra.org/awards/))
```

- `inline: true` renders the body directly in the list (good for one-liners).
- `date` controls ordering; the homepage `announcements.limit` in `about.md` caps how
  many show.
- Inline Markdown links and bold work; keep each item to one or two sentences.

## Projects, posts, awards

```text
_projects/      # research/software/project pages
_posts/         # blog posts (e.g. 2026-06-20-ppo-vs-sac.md)
_pages/awards.md  # awards list page (linked from the CV)
```

Follow the format of existing example files: YAML front matter first, then Markdown.
Blog posts are named `YYYY-MM-DD-slug.md`.

## Validate

```bash
npm run lint:prettier
bundle exec jekyll build --baseurl /al-folio
```
