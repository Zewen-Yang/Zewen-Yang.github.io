#!/usr/bin/env python

import logging
import os
import sys
import yaml
from datetime import datetime
from scholarly import scholarly, ProxyGenerator


def configure_proxy() -> None:
    """Route scholarly through a proxy when one is configured.

    Google Scholar returns 403 to GitHub Actions runner IPs, and scholarly's 403
    handler retries forever (sleeping 60-120s between attempts) without counting
    against ``set_retries``. A direct connection from CI therefore never finishes
    on its own; it only dies when the workflow's ``timeout`` kills it.

    * ``SCRAPERAPI_KEY`` — use ScraperAPI (https://www.scraperapi.com/), which
      scholarly supports natively. Set it as a repository secret for the
      ``update-citations`` workflow. This is the reliable option.
    * ``SCHOLARLY_FREE_PROXIES=1`` — rotate through free public proxies. Zero cost
      but slow and frequently broken; only a best-effort fallback.

    With neither set (e.g. running locally from a residential IP) scholarly talks
    to Scholar directly, which is what worked before.
    """
    scraperapi_key = os.environ.get("SCRAPERAPI_KEY", "").strip()
    use_free_proxies = os.environ.get("SCHOLARLY_FREE_PROXIES", "").strip().lower() in ("1", "true", "yes")

    if scraperapi_key:
        pg = ProxyGenerator()
        try:
            proxy_ok = pg.ScraperAPI(scraperapi_key)
        except Exception as e:
            # scholarly parses the /account response as JSON; an invalid key yields a
            # non-JSON body and the error escapes as a bare JSONDecodeError.
            proxy_ok = False
            print(f"ScraperAPI setup raised {type(e).__name__}: {e}")
        if not proxy_ok:
            print("SCRAPERAPI_KEY is set but ScraperAPI rejected it (invalid key or quota exhausted).")
            sys.exit(1)
        # Pass the same generator as the secondary proxy too; otherwise scholarly
        # fetches the author page through free proxies first and only falls back
        # to ScraperAPI after those time out.
        scholarly.use_proxy(pg, pg)
        print("Using ScraperAPI proxy for Google Scholar requests.")
    elif use_free_proxies:
        pg = ProxyGenerator()
        try:
            pg.FreeProxies()
        except Exception as e:
            print(f"Could not find a working free proxy: {e}")
            sys.exit(1)
        scholarly.use_proxy(pg, pg)
        print("Using free rotating proxies for Google Scholar requests.")
    else:
        print("No proxy configured; connecting to Google Scholar directly.")


def load_scholar_user_id() -> str:
    """Load the Google Scholar user ID from the configuration file."""
    config_file = "_data/socials.yml"
    if not os.path.exists(config_file):
        print(
            f"Configuration file {config_file} not found. Please ensure the file exists and contains your Google Scholar user ID."
        )
        sys.exit(1)
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        scholar_user_id = config.get("scholar_userid")
        if not scholar_user_id:
            print(
                "No 'scholar_userid' found in the configuration file. Please add 'scholar_userid' to _data/socials.yml."
            )
            sys.exit(1)
        return scholar_user_id
    except yaml.YAMLError as e:
        print(
            f"Error parsing YAML file {config_file}: {e}. Please check the file for correct YAML syntax."
        )
        sys.exit(1)


SCHOLAR_USER_ID: str = load_scholar_user_id()
OUTPUT_FILE: str = "_data/citations.yml"


def get_scholar_citations() -> None:
    """Fetch and update Google Scholar citation data."""
    print(f"Fetching citations for Google Scholar ID: {SCHOLAR_USER_ID}")
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if the output file was already updated today
    existing_data = None
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                existing_data = yaml.safe_load(f)
            if (
                existing_data
                and "metadata" in existing_data
                and "last_updated" in existing_data["metadata"]
            ):
                print(f"Last updated on: {existing_data['metadata']['last_updated']}")
                if existing_data["metadata"]["last_updated"] == today:
                    print("Citations data is already up-to-date. Skipping fetch.")
                    return
        except Exception as e:
            print(
                f"Warning: Could not read existing citation data from {OUTPUT_FILE}: {e}. The file may be missing or corrupted."
            )

    citation_data = {"metadata": {"last_updated": today}, "papers": {}}

    configure_proxy()
    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    try:
        author = scholarly.search_author_id(SCHOLAR_USER_ID)
        author_data = scholarly.fill(author)
    except Exception as e:
        print(
            f"Error fetching author data from Google Scholar for user ID '{SCHOLAR_USER_ID}': {e}. Please check your internet connection and Scholar user ID."
        )
        sys.exit(1)

    if not author_data:
        print(
            f"Could not fetch author data for user ID '{SCHOLAR_USER_ID}'. Please verify the Scholar user ID and try again."
        )
        sys.exit(1)

    if "publications" not in author_data:
        print(f"No publications found in author data for user ID '{SCHOLAR_USER_ID}'.")
        sys.exit(1)

    for pub in author_data["publications"]:
        try:
            pub_id = pub.get("pub_id") or pub.get("author_pub_id")
            if not pub_id:
                print(
                    f"Warning: No ID found for publication: {pub.get('bib', {}).get('title', 'Unknown')}. This publication will be skipped."
                )
                continue

            title = pub.get("bib", {}).get("title", "Unknown Title")
            year = pub.get("bib", {}).get("pub_year", "Unknown Year")
            citations = pub.get("num_citations", 0)

            print(f"Found: {title} ({year}) - Citations: {citations}")

            citation_data["papers"][pub_id] = {
                "title": title,
                "year": year,
                "citations": citations,
            }
        except Exception as e:
            print(
                f"Error processing publication '{pub.get('bib', {}).get('title', 'Unknown')}': {e}. This publication will be skipped."
            )

    # Compare new data with existing data
    if existing_data and existing_data.get("papers") == citation_data["papers"]:
        print("No changes in citation data. Skipping file update.")
        return

    try:
        with open(OUTPUT_FILE, "w") as f:
            yaml.dump(citation_data, f, width=1000, sort_keys=True)
        print(f"Citation data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_FILE}: {e}. Please check file permissions and disk space."
        )
        sys.exit(1)


if __name__ == "__main__":
    # Surface scholarly's own log lines (403 / captcha / proxy retries) so a CI run
    # that gets killed by `timeout` still leaves evidence of *why* it was stuck.
    # Line-buffer stdout: without this, output sitting in the buffer is lost when
    # `timeout` sends SIGTERM.
    sys.stdout.reconfigure(line_buffering=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s scholarly: %(message)s", stream=sys.stdout)
    scholarly.set_logger(True)
    try:
        get_scholar_citations()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
