"""
Compute per-provider site counts by combining crawler CSV output with
manually verified ODS data.  Run from the analysis/ directory:

    uv run python3 prevalence/provider_counts.py

For each dataset the script:
  1. Loads all crawler-detected sites from the CSV.
  2. Cross-references the manual check ODS to remove confirmed false
     positives and add any provider names the crawler missed.
  3. Counts unique domains per provider (one domain may increment
     multiple providers if it uses more than one).
"""

import csv
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

# ---------------------------------------------------------------------------
# ODS helpers
# ---------------------------------------------------------------------------

_ODS_TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
_ODS_TEXT  = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
_ODS_NS    = {"table": _ODS_TABLE, "text": _ODS_TEXT}


def _cell_text(cell) -> str:
    return " ".join(
        "".join(p.itertext())
        for p in cell.findall(".//text:p", _ODS_NS)
    ).strip()


def load_manual_check(path: Path) -> dict[str, str]:
    """Return {domain_lower: service_string} with duplicates resolved by
    keeping the non-false-positive entry."""
    with zipfile.ZipFile(path) as z:
        with z.open("content.xml") as f:
            root = ET.parse(f).getroot()

    manual: dict[str, str] = {}
    for row in root.findall(".//table:table-row", _ODS_NS)[1:]:
        cells = [_cell_text(c) for c in row.findall("table:table-cell", _ODS_NS)]
        if len(cells) < 3 or not cells[1]:
            continue
        domain = cells[1].strip().lower()
        svc = cells[2].strip()
        if domain not in manual or "false positive" in manual[domain].lower():
            manual[domain] = svc
    return manual


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def is_fp(svc: str) -> bool:
    sl = svc.lower()
    return (
        "false positive" in sl
        or "didn't have any" in sl
        or "doesn't seem" in sl
        or "account creation blocked, no age" in sl
        or "need to create account and pay" in sl
        or "blocked from account" in sl
        or "blocked completely" in sl
        or sl == "blocked"
        or sl in ("login", "")
    )


# Map of canonical provider name -> keywords to match in manual-check text
PROVIDER_KEYWORDS: dict[str, list[str]] = {
    "AgeVerif":    ["ageverif"],
    "Yoti":        ["yoti"],
    "VerifyMyAge": ["verifymy", "verifymyage"],
    "AgeGo":       ["agego"],
    "GoCam":       ["go.cam", "agerify"],
    "Incode":      ["incode"],
    "Gataca":      ["gataca", "amie"],
    "K-ID":        ["k-id"],
    "Ondato":      ["ondato"],
}

META_COLS    = {"", "name", "is_empty", "parse_error", "cloudflare", "rta", "meta_info"}
GENERIC_COLS = {"CatchAll", "CmpAgeVerif", "Generic", "Ep"}


def providers_from_manual(svc: str) -> set[str]:
    s = svc.lower()
    return {p for p, kws in PROVIDER_KEYWORDS.items() if any(k in s for k in kws)}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def combine(csv_path: Path, ods_path: Path) -> dict[str, set[str]]:
    """Return {domain: set_of_provider_names} for all confirmed AV sites."""
    manual = load_manual_check(ods_path)

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if not r["name"].startswith("_")]

    all_det_cols   = [k for k in rows[0] if k not in META_COLS]
    named_det_cols = [k for k in all_det_cols if k not in GENERIC_COLS]

    def has_any_av(row) -> bool:
        return any(row.get(c, "0") == "1" for c in all_det_cols)

    def csv_providers(row) -> set[str]:
        return {c for c in named_det_cols if row.get(c, "0") == "1"}

    domain_providers: dict[str, set[str]] = {}

    # Pass 1: crawler-detected sites
    for row in rows:
        if not has_any_av(row):
            continue
        domain = row["name"].lower().strip()
        if domain in manual and is_fp(manual[domain]):
            continue
        providers = csv_providers(row)
        if domain in manual and not is_fp(manual[domain]):
            providers |= providers_from_manual(manual[domain])
        domain_providers[domain] = providers

    # Pass 2: manual-confirmed sites the crawler missed entirely
    for domain, svc in manual.items():
        if is_fp(svc) or domain in domain_providers:
            continue
        providers = providers_from_manual(svc)
        if providers or "age gate" in svc.lower():
            domain_providers[domain] = providers

    return domain_providers


def summarise(domain_providers: dict[str, set[str]]) -> None:
    total = len(domain_providers)
    generic_only = sum(1 for p in domain_providers.values() if not p)
    counts: dict[str, int] = {}
    for providers in domain_providers.values():
        for p in providers:
            counts[p] = counts.get(p, 0) + 1

    print(f"  Confirmed AV sites:          {total}")
    print(f"  With named provider:         {total - generic_only}")
    print(f"  Generic/age-gate only:       {generic_only}")
    print()
    for p, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {p:20s}: {c:4d}  ({c / total * 100:.1f}%)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    datasets = [
        ("United Kingdom", DATA / "results10k.csv",     DATA / "manual check.ods"),
        ("Australia",      DATA / "results10k-aus.csv", DATA / "manual check aus.ods"),
    ]

    for label, csv_path, ods_path in datasets:
        print(f"=== {label} ===")
        domain_providers = combine(csv_path, ods_path)
        summarise(domain_providers)
        print()
