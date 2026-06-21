# 04 — Own the Repo & Pull al-folio Updates

This page documents the one-time git setup that makes this site **your own repository**
while keeping the ability to **pull upstream al-folio updates**. It is a record of exactly
what was done, plus the day-to-day commands you use afterwards.

## The mental model: two remotes

When you start from al-folio, your only git remote (`origin`) points at the original
project. To own the site without losing upstream updates, split the two roles:

| Remote | Points at | Used for |
| ------ | --------- | -------- |
| `origin` | `git@github.com:Zewen-Yang/Zewen-Yang.github.io.git` | **Your** repo. Daily `push`/`pull`. |
| `upstream` | `https://github.com/alshedivat/al-folio.git` | The original al-folio. **Pull updates only.** |

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

```bash
git fetch upstream
git merge upstream/main      # or: git rebase upstream/main
# resolve any conflicts, then:
git add -A
git commit                   # only needed if merge stopped for conflicts
git push
```

Conflicts usually appear in files you personalized (`_config.yml`, `_data/cv.yml`,
content under `_pages`/`_news`/`_posts`). Keep your values, take upstream's structural
changes. Because v1 runtime lives in gems (see [README](README.md)), most upstream code
changes arrive via `bundle update`, not via merge — so content conflicts stay small.

## GitHub Pages

After the first push, enable Pages in **Settings → Pages** (Source: GitHub Actions, which
the bundled `.github/workflows/` deploy uses, or the `main` branch). The site goes live at
`https://zewen-yang.github.io` shortly after the build finishes.
