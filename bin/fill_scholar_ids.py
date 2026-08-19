#!/usr/bin/env python3
"""Fill `google_scholar_id` in `_bibliography/papers.bib` from `_data/citations.yml`.

Citation cluster IDs come from `bin/update_scholar_citations.py` (key after the colon
in `DbuBsVUAAAAJ:CLUSTERID`). Titles are matched with Jaccard similarity.

Dry-run by default. Apply with `--write`.

Usage (from repo root):

    python3 bin/fill_scholar_ids.py
    python3 bin/fill_scholar_ids.py --write
    python3 bin/fill_scholar_ids.py --min-score 0.7 --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
CITATIONS = ROOT / "_data" / "citations.yml"


def norm(text: str) -> str:
    text = text.lower().replace("–", "-").replace("—", "-").replace("’", "'")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def jaccard(a: str, b: str) -> float:
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    score = len(ta & tb) / len(ta | tb)
    if a in b or b in a:
        score = max(score, 0.9)
    return score


def extract_title(entry: str) -> str:
    match = re.search(r"(?i)\btitle\s*=\s*\{\{(.+?)\}\}", entry, re.S)
    if not match:
        match = re.search(r"(?i)\btitle\s*=\s*\{(.+?)\}", entry, re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def extract_key(entry: str) -> str:
    match = re.match(r"@\w+\{([^,]+),", entry)
    return match.group(1).strip() if match else ""


def iter_entries(text: str) -> list[tuple[int, int, str]]:
    entries = []
    i = 0
    while True:
        match = re.search(r"@\w+\{", text[i:])
        if not match:
            break
        start = i + match.start()
        brace = i + match.end() - 1
        depth = 0
        end = None
        for j in range(brace, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        if end is None:
            break
        entries.append((start, end, text[start:end]))
        i = end
    return entries


def load_citations() -> list[tuple[str, str, str]]:
    data = yaml.safe_load(CITATIONS.read_text(encoding="utf-8"))
    papers = (data or {}).get("papers") or {}
    out = []
    for key, meta in papers.items():
        cluster = key.split(":", 1)[1] if ":" in key else key
        title = (meta or {}).get("title") or ""
        out.append((cluster, title, norm(title)))
    return out


def insert_id(entry: str, cluster: str) -> str:
    body = entry.rstrip()
    if body.endswith("}"):
        inner = body[:-1].rstrip()
    else:
        return entry
    if not inner.endswith(","):
        inner += ","
    return inner + f"\n  google_scholar_id = {{{cluster}}},\n}}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write matches into papers.bib")
    parser.add_argument("--min-score", type=float, default=0.55)
    parser.add_argument("--replace", action="store_true", help="Overwrite existing google_scholar_id")
    args = parser.parse_args()

    if not BIB.exists() or not CITATIONS.exists():
        sys.exit("Run from the site repo root (need _bibliography/papers.bib and _data/citations.yml).")

    cites = load_citations()
    text = BIB.read_text(encoding="utf-8")
    entries = iter_entries(text)
    replacements: list[tuple[int, int, str]] = []
    print(f"{'status':<8} {'score':>5}  key  ->  cluster  title")
    for start, end, entry in entries:
        key = extract_key(entry)
        title = extract_title(entry)
        has_id = "google_scholar_id" in entry
        if has_id and not args.replace:
            print(f"{'keep':<8} {'—':>5}  {key}")
            continue
        nt = norm(title)
        best_score = 0.0
        best: tuple[str, str] | None = None
        for cluster, ctitle, nc in cites:
            score = jaccard(nt, nc)
            if score > best_score:
                best_score = score
                best = (cluster, ctitle)
        if not best or best_score < args.min_score:
            hint = f"{best[0]} / {best[1][:60]}" if best else ""
            print(f"{'skip':<8} {best_score:5.2f}  {key}  {title[:60]}  {hint}")
            continue
        cluster, ctitle = best
        print(f"{'match':<8} {best_score:5.2f}  {key}  ->  {cluster}  {ctitle[:60]}")
        replacements.append((start, end, insert_id(entry, cluster)))

    if not args.write:
        print(f"\nDry run: {len(replacements)} insert(s). Re-run with --write to apply.")
        return

    if not replacements:
        print("Nothing to write.")
        return

    out = []
    cursor = 0
    for start, end, new_entry in replacements:
        out.append(text[cursor:start])
        out.append(new_entry)
        cursor = end
    out.append(text[cursor:])
    BIB.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {len(replacements)} google_scholar_id field(s) to {BIB}")


if __name__ == "__main__":
    main()
