# 03 — Theming & Local Overrides

This page covers changing the site's look (colors, small CSS tweaks) and — critically —
the **override audit workflow** you must follow any time you edit a plugin-owned file.

## The two-layer rule (why overrides need care)

In v1 the runtime lives in gems. The theme CSS (`_sass/_themes.scss`), base layouts
(`_layouts/*.liquid`), and includes (`_includes/*.liquid`) are owned by `al_folio_core`,
**not** by this repo. When you copy one of those files into the repo to customize it, you
create a **local override** that _shadows_ the gem's version.

Local overrides are allowed, but they are **tracked** so that a future `bundle update`
can warn you when the upstream gem version drifts from what you forked. The tracking file
is `.al-folio-overrides.yml`, and **it must be committed**.

This site currently overrides three files (all owned by `al_folio_core`):

| File                    | Why                                                        |
| ----------------------- | ---------------------------------------------------------- |
| `_sass/_themes.scss`    | Dracula palette + spec role assignment + back-to-top tweak |
| `_includes/head.liquid` | head customization + dark-only theme shim                  |
| `_layouts/about.liquid` | homepage layout tweak                                      |

## Changing the theme color (Dracula)

There is **no simple config key** for the accent color, so it's done via a local override
of `_sass/_themes.scss`.

The site is **dark-only**: `enable_darkmode: false` in `_config.yml` hides the light/dark
toggle, so the [Dracula palette](https://draculatheme.com) lives directly in `:root` and
there is no `html[data-theme="dark"]` block. Dark-only is a deliberate choice — every
Dracula hue is designed for a dark background and fails contrast on white (pink is 2.4:1
against `#fff`, well under the 4.5:1 needed for body text), so a light variant would have
to abandon the palette anyway.

### Role assignment follows the official spec

al-folio funnels nearly every accent through a single token, `--global-theme-color`, which
collapses a 11-color palette onto one hue. The override splits the roles back out using
[the official Dracula spec](https://spec.draculatheme.com), section 2.2 "Markup (Markdown,
RST, etc.)" — a web page _is_ markup, so the mapping is taken from the spec rather than
invented:

| Spec scope                 | Color             | Applied to                       |
| -------------------------- | ----------------- | -------------------------------- |
| `MarkupLinkText`           | Pink `#ff79c6`    | links (`--global-theme-color`)   |
| `MarkupLinkUrl`            | Cyan `#8be9fd`    | hover (`--global-hover-color`)   |
| `MarkupHeading`            | Purple `#bd93f9`  | `h1`-`h6` inside `.post article` |
| `MarkupInlineCode`         | Green `#50fa7b`   | inline `` `code` ``              |
| `MarkupBlockquote`         | Yellow `#f1fa8c`  | `blockquote`, italic             |
| `MarkupBold`               | Orange `#ffb86c`  | `strong` / `b` in prose          |
| `MarkupListBulletOrNumber` | Cyan `#8be9fd`    | list markers                     |
| `MarkupHorizontalRule`     | Comment `#6272a4` | `hr`                             |
| `Error` (section 2)        | Red `#ff5555`     | danger blocks                    |

Cyan for hover is not arbitrary: it is ~10:1 against the background versus pink's ~6:1, so
hovering reads as a brightness step. Swapping pink for purple (5.9:1) would be a hue change
at the same lightness and barely register.

Two surfaces deviate from a naive reading of the spec, both for contrast:

- **Code background** uses AnsiBlack `#21222c` (spec section 1.2.2), not Selection
  `#44475a`. Comment `#6272a4` only reaches 1.9:1 against Selection, which makes code
  comments unreadable; against AnsiBlack it is 3.4:1.
- **`--global-divider-color`** stays on Selection. `MarkupHorizontalRule` (Comment) is
  applied to `hr` alone, because that token also drives table borders and card edges, and
  Comment there lights up every box on the page.

To use a **different** palette, swap the `$dracula-*` hex values in `_sass/_themes.scss` and
the `--dracula-*` custom properties in `assets/css/dracula-syntax.css`, then rebuild.

### Syntax highlighting

`assets/css/dracula-syntax.css` is a starter-owned (not an override) Rouge theme written
directly against the spec — each rule carries the spec section it implements, so it can be
diffed against the document when it changes. It replaces al_folio_core's shipped
light/dark Pygments pair, which `theme.js` would otherwise swap at runtime.

One trap worth knowing: al_folio_core declares `code { color: var(--global-theme-color) }`
directly on the `<code>` element. That beats the color inherited from `.highlight`, so any
text Rouge does **not** wrap in a token span (a fenced block with no language, for
instance) renders in the link accent unless explicitly overridden. The stylesheet handles
this at the end of its container block.

### Dark-only requires a `determineComputedTheme` shim

Turning off `enable_darkmode` stops `theme.js` from loading, and two things depend on it:

1. `al_charts`' mermaid/echarts/plotly/vega/diff2html setup scripts call
   `determineComputedTheme()` **unguarded** — with no definition that is a `ReferenceError`
   and the chart silently never renders.
2. `al_search` and core's `common.js` / `no_defer.js` guard the call but fall back to
   `"light"`, which would give a light palette on a dark page.

The `{% else %}` branch of the `enable_darkmode` block in `_includes/head.liquid` therefore
sets `data-theme="dark"` statically and defines `determineComputedTheme()` to return
`"dark"`. If you ever re-enable the toggle, that branch simply stops being emitted.

### Small CSS tweaks live here too

The override also carries a couple of layout fixes, e.g. the back-to-top button is lifted
above the fixed-bottom footer so it isn't obscured:

```scss
#back-to-top {
  bottom: 45px; // clear the ~35px fixed-bottom footer (Bootstrap z-index 1030)
  z-index: 1031;
}
```

When you add a tweak like this, prefer editing **CSS variables / rules already present in
the override** rather than introducing a brand-new override file, to keep the audit
surface small.

### Gotcha: a style works locally but looks wrong on GitHub Pages (PurgeCSS)

If a rule looks correct under `jekyll serve` but is **missing/ugly on the deployed site**,
the culprit is almost always **PurgeCSS**. The deploy workflow (`.github/workflows/deploy.yml`)
runs an extra `purgecss -c purgecss.config.js` step **after** the build — local `serve` does
not. PurgeCSS scans the static HTML and deletes any CSS selector it can't find there.

The trap: elements that a JS library **injects at runtime** never appear in the static HTML,
so PurgeCSS strips their styles and they fall back to the library's defaults. We hit this with
the back-to-top button — `vanilla-back-to-top` creates `#back-to-top` (and its inner `<svg>`)
in the browser, so our Dracula pink rules in `_sass/_themes.scss` were purged and the button
turned the library's default black on the live site.

The fix is to **safelist** the selector in `purgecss.config.js` so it survives the purge:

```js
safelist: [
  // ...
  // vanilla-back-to-top injects #back-to-top at runtime → safelist it.
  "back-to-top",
  // medium-zoom injects these at runtime too.
  "medium-zoom-overlay",
  "medium-zoom-image--opened",
],
```

safelist entries match any selector **containing** that string (so `"back-to-top"` keeps both
`#back-to-top` and `#back-to-top svg`). `purgecss.config.js` is **starter-owned**, so this is a
normal config edit — it is _not_ a plugin override and needs **no** audit. Rule of thumb: any
runtime-injected element whose styling disappears after deploy belongs in this safelist.

## The override audit workflow (do this every time)

Whenever you create or edit a file that a gem owns, run the audit and acknowledge the
change so `.al-folio-overrides.yml` records the owner gem, gem version, and upstream/local
SHA256:

```bash
# 1. See what overrides exist and whether any drifted from upstream
bundle exec al-folio upgrade overrides audit

# 2. Inspect the diff between your local file and the gem's upstream version
bundle exec al-folio upgrade overrides diff _sass/_themes.scss

# 3. Acknowledge the current state (updates local_sha256 + acknowledged_at)
bundle exec al-folio upgrade overrides accept _sass/_themes.scss

# 4. Commit the tracking file
git add .al-folio-overrides.yml _sass/_themes.scss
git commit -m "Theme: tweak Dracula accent colors"
```

`.al-folio-overrides.yml` looks like this (one block per overridden file):

```yaml
version: 1
overrides:
  _sass/_themes.scss:
    owner: al_folio_core
    gem_version: 1.0.11
    upstream_path: _sass/_themes.scss
    upstream_sha256: <hash of the gem's version>
    local_sha256: <hash of your version>
    acknowledged_at: "2026-06-20"
```

### After upgrading gems (`bundle update`)

A gem upgrade can change the upstream file you forked. Re-run the audit — if it reports
**drift** (upstream SHA changed), open the diff, port any upstream improvements into your
local copy, then `accept` again and commit. This is how you avoid silently missing
upstream bug fixes.

> **Best practice:** if a fix is generally useful (not site-specific), port it to the
> owning gem instead of keeping a local override forever. Overrides are a deliberate,
> tracked exception — not the default.

## Validate

```bash
npm run lint:prettier
bundle exec jekyll build --baseurl /al-folio
bundle exec al-folio upgrade overrides audit
```
