# 04 — Own the Repo & Pull al-folio Updates

This page documents the one-time git setup that makes this site **your own repository**
while keeping the ability to **pull upstream al-folio updates**. It is a record of exactly
what was done, plus the day-to-day commands you use afterwards.

## The mental model: two remotes

When you start from al-folio, your only git remote (`origin`) points at the original
project. To own the site without losing upstream updates, split the two roles:

| Remote     | Points at                                            | Used for                                      |
| ---------- | ---------------------------------------------------- | --------------------------------------------- |
| `origin`   | `git@github.com:Zewen-Yang/Zewen-Yang.github.io.git` | **Your** repo. Daily `push`/`pull`.           |
| `upstream` | `https://github.com/alshedivat/al-folio.git`         | The original al-folio. **Pull updates only.** |

For a personal user page the repo name **must** equal your GitHub username:
`Zewen-Yang.github.io` → served at `https://zewen-yang.github.io`.

## One-time setup (what we ran)

This assumes you already created an **empty** repo on GitHub (no README/.gitignore/license).

```bash
# 1. Commit your personalizations first
git add -A
git commit -m "Personalize al-folio site"

# 2. Rename the original al-folio remote to "upstream"
git remote rename origin upstream

# 3. Add YOUR repo as the new "origin"
git remote add origin git@github.com:Zewen-Yang/Zewen-Yang.github.io.git

# 4. Normalize the branch name and push, setting up tracking
git branch -M main
git push -u origin main
```

Verify the result:

```bash
git remote -v
# origin    git@github.com:Zewen-Yang/Zewen-Yang.github.io.git (fetch/push)
# upstream  https://github.com/alshedivat/al-folio.git           (fetch/push)
```

> SSH note: the first `git push` can appear to hang with no output while it uploads the
> full git history. That is normal. If it truly blocks, test the key with
> `ssh -T git@github.com` — a `Hi <username>!` reply means auth works.

## Site config for a user page

A `username.github.io` user page is served from the domain root, so in `_config.yml`:

```yaml
url: https://zewen-yang.github.io # your domain
baseurl: # leave EMPTY for a user page (only project pages use a subpath like /al-folio)
```

A non-empty `baseurl` on a user page breaks CSS/links, so keep it blank.

## Day-to-day: pushing your own changes

```bash
git add -A
git commit -m "describe your change"
git push            # tracking is already set, no need for -u again
```

## Pulling al-folio updates later

Do this every few months, or when [alshedivat/al-folio](https://github.com/alshedivat/al-folio/releases)
publishes a new release. There are **two layers**. Gems are the theme; `upstream/main`
is only the thin starter (CI, docs, sample posts). Follow gems first. Do not habitually
`git merge upstream/main` onto your personalized `main`.

### 1) Theme / feature updates (usual path)

```bash
./bin/show_upstream_plugin_pins.sh
```

Copy the upstream `:al_folio_plugins` pins into your `Gemfile`. If upstream added gems (`al_rtl`, `al_marimo`, …),
add the same names under `plugins:` in `_config.yml`.

1. Keep your personal `_config.yml` values (`url`, `baseurl`, name, socials).
2. Install and check:

```bash
bundle install
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8   # audit CLI needs UTF-8
bundle exec al-folio upgrade audit --no-fail
bundle exec al-folio upgrade overrides audit
```

3. If an override is **stale**, port upstream into your local copy while keeping your
   customization, then acknowledge:

```bash
bundle exec al-folio upgrade overrides diff _includes/head.liquid
# edit the local file, then:
bundle exec al-folio upgrade overrides accept PATH
```

You currently override `_includes/head.liquid` (default dark theme), `_layouts/about.liquid`,
and `_sass/_themes.scss`. See [03 — Theming & overrides](03-theming-overrides.md).

`bundle update` alone will **not** bump `al_*` gems: they are pinned with `= 1.0.x`.

### 2) Starter / CI / docs (only when you need it)

Merge on a **side branch**, never straight onto `main`:

```bash
git checkout -b sync-al-folio
git merge upstream/main
```

Keep yours: `_pages`, `_news`, `_bibliography`, `_data`, personal `_config.yml` values,
and the three override files. Take upstream's: `Gemfile` pins, `.github/workflows` if
deploy/tests broke, `docs/` if you care. Skip if you do not want them: `readme_preview/`,
star-history SVGs, official `_posts` demos, README showcase, dummy Scholar citation bumps.

After conflicts are resolved, merge the branch into `main` and `git push origin main`.

GitHub's **Sync fork** button is the same as merging `upstream/main`. Use the gem path
above instead for day-to-day updates.

## GitHub Pages

The bundled `.github/workflows/deploy.yml` builds the site and **pushes the result to a
`gh-pages` branch** (via `JamesIves/github-pages-deploy-action`). So Pages must be told to
serve that branch:

1. Go to **Settings → Pages → Build and deployment**.
2. Set **Source** to `Deploy from a branch`.
3. Set **Branch** to `gh-pages` / `(root)`, then **Save**.

The site goes live at `https://zewen-yang.github.io` a few minutes later.

> Common 404 cause: the build succeeded and `gh-pages` exists with a valid `index.html`,
> but **Source** is not pointing at `gh-pages` (e.g. left on `GitHub Actions` or `main`).
> Fix it with the steps above — no code change needed.

### Re-running a deploy

`deploy.yml` ignores `README.md` (and a few docs) in its path filters, so editing only those
files will **not** trigger a deploy. To force a rebuild, either edit a content/config file
and push, or run the **Deploy site** workflow manually from the **Actions** tab
(`workflow_dispatch`).
