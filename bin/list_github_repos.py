#!/usr/bin/env python3
"""List non-fork GitHub repos for filling `_data/repositories.yml`.

Reads `github_username` from `_data/socials.yml` unless `--user` is given.

Usage (from repo root):

    python3 bin/list_github_repos.py
    python3 bin/list_github_repos.py --user Zewen-Yang --include-forks
    python3 bin/list_github_repos.py --yaml
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOCIALS = ROOT / "_data" / "socials.yml"
API = "https://api.github.com/users/{user}/repos?per_page=100&type=owner&sort=updated"


def github_username() -> str:
    text = SOCIALS.read_text(encoding="utf-8")
    match = re.search(r"^github_username:\s*(\S+)", text, re.M)
    if not match:
        sys.exit(f"No github_username in {SOCIALS}")
    return match.group(1).split("#", 1)[0].strip()


def fetch_repos(user: str) -> list[dict]:
    url = API.format(user=user)
    req = urllib.request.Request(url, headers={"User-Agent": "al-folio-site-scripts"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.URLError as exc:
        sys.exit(f"GitHub API request failed: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", help="GitHub username (default: _data/socials.yml)")
    parser.add_argument("--include-forks", action="store_true")
    parser.add_argument(
        "--yaml",
        action="store_true",
        help="Print a github_repos: snippet you can paste into _data/repositories.yml",
    )
    args = parser.parse_args()

    user = args.user or github_username()
    repos = fetch_repos(user)
    chosen = []
    for repo in repos:
        if repo.get("fork") and not args.include_forks:
            continue
        chosen.append(repo)
        stars = repo.get("stargazers_count", 0)
        pushed = (repo.get("pushed_at") or "")[:10]
        name = repo.get("full_name")
        desc = repo.get("description") or ""
        fork = " (fork)" if repo.get("fork") else ""
        print(f"{stars:>4}  {pushed}  {name}{fork}  {desc}")

    if args.yaml:
        print("\n# paste under github_repos: in _data/repositories.yml")
        print("github_repos:")
        for repo in chosen:
            print(f"  - {repo['full_name']}")


if __name__ == "__main__":
    main()
