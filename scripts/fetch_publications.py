"""Fetch the publications listed on an ORCID profile and rank the top 5 by
citation count (looked up via Semantic Scholar), writing the result to
_data/publications.yml.

Run by .github/workflows/update-publications.yml on a schedule and on
manual trigger. Both ORCID's public API and Semantic Scholar's Graph API
are official, documented, and don't require authentication for this kind
of light, occasional use. Semantic Scholar does rate-limit shared
unauthenticated traffic though, so lookups here retry with backoff and
pause briefly between calls. Any failure is soft: the existing data file
is left untouched and the reason is printed to the workflow log.
"""

import re
import sys
import time

import requests
import yaml

CONFIG_PATH = "_config.yml"
DATA_PATH = "_data/publications.yml"
TOP_N = 5

ORCID_API = "https://pub.orcid.org/v3.0"
S2_PAPER_API = "https://api.semanticscholar.org/graph/v1/paper"
S2_FIELDS = "title,year,citationCount,authors,externalIds"

ORCID_ID_RE = re.compile(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])")

# Preference order: try whichever external ID types a work has, in this order.
S2_ID_TYPES = (("DOI", "doi"), ("PMID", "pmid"), ("ARXIV", "arxiv"))


def get_orcid_id():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    raw = str((config.get("orcid") or {}).get("id", ""))
    match = ORCID_ID_RE.search(raw)
    if not match:
        print(
            "No valid ORCID iD found in _config.yml (orcid.id) — skipping fetch."
        )
        return None
    return match.group(1)


def fetch_orcid_works(orcid_id):
    resp = requests.get(
        f"{ORCID_API}/{orcid_id}/works",
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    groups = resp.json().get("group", [])

    works = []
    for group in groups:
        summary = group["work-summary"][0]
        title = ((summary.get("title") or {}).get("title") or {}).get("value")
        if not title:
            continue

        year = (
            (summary.get("publication-date") or {}).get("year") or {}
        ).get("value")

        external_ids = (summary.get("external-ids") or {}).get("external-id", [])
        ids_by_type = {
            e["external-id-type"].lower(): e["external-id-value"]
            for e in external_ids
            if e.get("external-id-type") and e.get("external-id-value")
        }

        works.append({"title": title, "year": year, "ids": ids_by_type})

    return works


def s2_lookup_paper(prefix, value, retries=3):
    url = f"{S2_PAPER_API}/{prefix}:{value}"
    for attempt in range(retries):
        resp = requests.get(url, params={"fields": S2_FIELDS}, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429:
            time.sleep(2**attempt * 2)
            continue
        return None
    return None


def citation_link(ids_by_type, s2_data):
    if "doi" in ids_by_type:
        return f"https://doi.org/{ids_by_type['doi']}"
    if s2_data and (s2_data.get("externalIds") or {}).get("DOI"):
        return f"https://doi.org/{s2_data['externalIds']['DOI']}"
    if "pmid" in ids_by_type:
        return f"https://pubmed.ncbi.nlm.nih.gov/{ids_by_type['pmid']}/"
    if "arxiv" in ids_by_type:
        return f"https://arxiv.org/abs/{ids_by_type['arxiv']}"
    return "#"


def enrich_with_citations(works):
    enriched = []
    for work in works:
        ids_by_type = work["ids"]
        s2_data = None
        for prefix, key in S2_ID_TYPES:
            if key in ids_by_type:
                s2_data = s2_lookup_paper(prefix, ids_by_type[key])
                time.sleep(1.1)  # stay well under the shared rate limit
                if s2_data:
                    break

        if not s2_data:
            # No DOI/PMID/arXiv ID, or Semantic Scholar has no record for
            # it — we can't get a citation count, so leave it out of the
            # ranked list rather than guessing.
            continue

        authors = ", ".join(
            a.get("name", "") for a in s2_data.get("authors", []) if a.get("name")
        )
        enriched.append(
            {
                "title": s2_data.get("title") or work["title"],
                "authors": authors,
                "year": s2_data.get("year") or work["year"],
                "citations": s2_data.get("citationCount") or 0,
                "link": citation_link(ids_by_type, s2_data),
            }
        )

    return enriched


def main():
    # The workflow passes today's date (computed in the shell, not in
    # Python) as the first argument, e.g. "2026-07-31".
    run_date = sys.argv[1] if len(sys.argv) > 1 else "unknown date"

    orcid_id = get_orcid_id()
    if not orcid_id:
        return

    try:
        works = fetch_orcid_works(orcid_id)
    except Exception as e:
        print(f"Could not fetch works from ORCID: {e}")
        return

    if not works:
        print(
            "No works found on this ORCID profile — leaving existing data "
            "file untouched."
        )
        return

    try:
        enriched = enrich_with_citations(works)
    except Exception as e:
        print(
            f"Could not fetch citation counts from Semantic Scholar (it "
            f"occasionally rate-limits unauthenticated requests — safe to "
            f"retry via 'Run workflow' in a few minutes): {e}"
        )
        return

    if not enriched:
        print(
            "None of your ORCID works have a DOI/PMID/arXiv ID that "
            "Semantic Scholar recognises, so no citation-ranked list could "
            "be built. Leaving the existing data file untouched — you can "
            "add publications to _data/publications.yml by hand instead."
        )
        return

    enriched.sort(key=lambda p: p["citations"], reverse=True)
    top_pubs = enriched[:TOP_N]

    data = {"last_updated": run_date, "items": top_pubs}

    with open(DATA_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"Updated {DATA_PATH} with {len(top_pubs)} publications.")


if __name__ == "__main__":
    main()
