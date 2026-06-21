# 01 — Toolchain Setup (macOS, first time only)

This whole page is a one-time setup. Once you have a clean build and the dev server
running, you can skip back to [content editing](02-content-editing.md).

> The macOS **system Ruby** (`/usr/bin/ruby`, version 2.6) is too old and read-only.
> It cannot run Bundler 4.x or modern Jekyll, and `gem install` into it fails with a
> permission error. Do **not** fight it — install your own modern Ruby instead.

## 1. Install Homebrew (if you don't have it)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then add it to your PATH (Apple Silicon path shown; run the lines Homebrew prints if different):

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
brew --version   # confirm it works
```

## 2. Install Ruby 3.3.5 via rbenv

Use `3.3.5` because it matches this repo's CI (`unit-tests.yml`, `deploy.yml`, etc.),
which avoids "works locally but breaks in CI" surprises.

```bash
brew install rbenv ruby-build
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
eval "$(rbenv init - zsh)"

rbenv install 3.3.5      # compiles Ruby; takes a few minutes
rbenv local 3.3.5        # run this INSIDE the repo to scope it to this project
ruby -v                  # must now show 3.3.5, NOT 2.6.x
```

If `ruby -v` still shows 2.6.x, open a fresh terminal (so `~/.zshrc` reloads) and `cd` back.

## 3. Install the pinned Bundler and gems

`Gemfile.lock` pins `BUNDLED WITH 4.0.6`, so install that exact Bundler version
(installing into rbenv Ruby now works — no permission errors):

```bash
gem install bundler -v 4.0.6
bundle install
```

> **Gotcha (seen in practice):** if you run `bundle install` while the macOS system Ruby
> 2.6 is still active, you get a Bundler version mismatch error — `Gemfile.lock` wants
> Bundler 4.0.6 but the system Ruby ships an old one. The fix is always the same: make
> sure `ruby -v` shows 3.3.5 first (steps above), then reinstall Bundler 4.0.6.

## 4. Install Node tooling

```bash
npm ci
```

## 5. Install optional dependencies (the starter's example content needs these)

The example content includes a Jupyter notebook post and responsive images, so the
build will **fail** without these:

```bash
# A modern Python (the macOS system Python 3.9 is old; use Homebrew's instead)
brew install python@3.12

# Jupyter / nbconvert — required to render the sample notebook post
# (Homebrew Python is PEP 668 "externally managed", hence --break-system-packages)
python3.12 -m pip install --user --break-system-packages jupyter nbconvert
# add the user script dir to PATH (match the Python version you installed)
echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zshrc

# ImageMagick — provides `convert`, used for responsive image variants
brew install imagemagick
```

> Tip: if you don't need the notebook example, you can instead delete
> `assets/jupyter/blog.ipynb` and its referencing post rather than installing Jupyter.

## 6. Verify the toolchain

Reload your shell (or open a new terminal), then confirm everything resolves to the
versions you just installed (not the macOS system ones):

```bash
source ~/.zshrc
which jupyter convert ruby
# expected:
#   ~/Library/Python/3.12/bin/jupyter   (Homebrew Python 3.12, NOT /usr/bin)
#   /opt/homebrew/bin/convert           (ImageMagick)
#   ~/.rbenv/shims/ruby                 (rbenv → resolves to 3.3.5 in this repo)
```

Then run a full production-style build as a final check:

```bash
cd ~/Documents/al-folio
bundle exec jekyll build --baseurl /al-folio
```

Success looks like a final `done in N seconds.` with no `Conversion error`. Along the
way you should see signs each optional tool worked:

- `Imagemagick: Adding static file ...-480/800/1400.webp` — ImageMagick generated the
  responsive image variants.
- `[NbConvertApp] Converting notebook ... to html` — Jupyter rendered the sample notebook.
- `AlImgTools: Successfully copied ... from ~/.rbenv/versions/3.3.5/...` — confirms the
  rbenv Ruby 3.3.5 and its gems are in use.

These messages are harmless and can be ignored:

- `DEPRECATION WARNING: to_time ... (Rails 8.0)` — an upstream dependency warning.
- `Imagemagick: Generated 0 file(s)` — the variants already exist (not an error).

The compiled site is written to the `_site/` folder.

## 7. Run the site locally

```bash
bundle exec jekyll serve
```

Then open (note the `/al-folio/` path — it comes from `baseurl` in `_config.yml`):

```text
http://127.0.0.1:4000/al-folio/
```

The bare `http://127.0.0.1:4000/` will 404 while `baseurl` is set. Once you change
`baseurl` to `""` (see below), the bare URL is the one that works.

## 8. Site identity in `_config.yml`

Open `_config.yml` and update personal fields such as:

```yaml
title:
first_name:
middle_name:
last_name:
email:
description:
url:
baseurl:
github_username:
linkedin_username:
scholar_userid:
orcid_id:
```

## Deploy with GitHub Pages

### Option A — user website

Repository named `username.github.io`:

```yaml
url: https://username.github.io
baseurl: ""
```

Live at `https://username.github.io`.

### Option B — project website

Any repository name, e.g. `academic-site`:

```yaml
url: https://username.github.io
baseurl: /academic-site
```

Live at `https://username.github.io/academic-site/`.

> If your final `baseurl` is empty, test the build with `bundle exec jekyll build --baseurl ""`.
