# 03 — Theming & Local Overrides

This page covers changing the site's look (colors, small CSS tweaks) and — critically —
the **override audit workflow** you must follow any time you edit a plugin-owned file.

## The two-layer rule (why overrides need care)

In v1 the runtime lives in gems. The theme CSS (`_sass/_themes.scss`), base layouts
(`_layouts/*.liquid`), and includes (`_includes/*.liquid`) are owned by `al_folio_core`,
**not** by this repo. When you copy one of those files into the repo to customize it, you
create a **local override** that *shadows* the gem's version.

Local overrides are allowed, but they are **tracked** so that a future `bundle update`
can warn you when the upstream gem version drifts from what you forked. The tracking file
is `.al-folio-overrides.yml`, and **it must be committed**.

This site currently overrides three files (all owned by `al_folio_core`):

| File | Why |
| ---- | --- |
| `_sass/_themes.scss` | Dracula accent colors + back-to-top tweak |
| `_includes/head.liquid` | head customization |
| `_layouts/about.liquid` | homepage layout tweak |

## Changing the theme color (Dracula)

There is **no simple config key** for the accent color, so it's done via a local override
of `_sass/_themes.scss`. The override keeps everything identical to upstream **except**
the CSS custom properties for the accent/hover/footer colors, which are set to the
[Dracula palette](https://draculatheme.com):

```scss
// Dracula palette
$dracula-background: #282a36;
$dracula-current-line: #44475a;
$dracula-foreground: #f8f8f2;
$dracula-comment: #6272a4;
$dracula-purple: #bd93f9;
$dracula-pink: #ff79c6;

:root {
  --global-theme-color: #{$dracula-pink};   // main accent
  --global-hover-color: #{$dracula-pink};
  --global-footer-bg-color: #{$dracula-background};
  --global-footer-text-color: #{$dracula-purple};
  --global-footer-link-color: #{$dracula-pink};
  // ... everything else mirrors upstream ...
}

html[data-theme="dark"] {
  --global-bg-color: #{$dracula-background};
  // ... dark-mode variants ...
}
```

To use a **different** palette: keep this file, swap the `$dracula-*` hex values (or add
your own palette variables), and rebuild. Set both the `:root` (light) **and**
`html[data-theme="dark"]` blocks since `enable_darkmode: true` in `_config.yml` lets
visitors toggle modes — each visitor may land in either mode.

### Small CSS tweaks live here too

The override also carries a couple of layout fixes, e.g. the back-to-top button is lifted
above the fixed-bottom footer so it isn't obscured:

```scss
#back-to-top {
  bottom: 45px;     // clear the ~35px fixed-bottom footer (Bootstrap z-index 1030)
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
normal config edit — it is *not* a plugin override and needs **no** audit. Rule of thumb: any
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
    acknowledged_at: '2026-06-20'
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
