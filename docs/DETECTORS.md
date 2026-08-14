# Provider detectors

Each check is a BeautifulSoup / string match on **already downloaded** homepage HTML. Detectors do not open age-gate UIs.

Code: [`analysis/prevalence/avp/`](../analysis/prevalence/avp/). Runner: [`analysis/prevalence/main.py`](../analysis/prevalence/main.py).

## Pipeline

```
pages/*.html
    → python -m prevalence.main --input-dir pages --output-dir results-json -n N -w i
    → one JSON per HTML file
    → python -m prevalence.combine -i results-json -o {code}_prevalence.csv
```

`main.py` shards files across workers the same way the crawler does (`worker`, `num-workers`). Empty files set `is_empty`. Challenge/interstitial error pages set `cloudflare` and skip vendors. RTA is a separate meta-tag check ([`analysis/prevalence/rta/`](../analysis/prevalence/rta/)).

A vendor column is `1` if **any** of that class’s checks returned true (`Detector.detect`). The names of the true checks are stored in `meta_info`.

## Check styles (strict → broad)

| Style | Example | Risk |
| --- | --- | --- |
| Script/iframe URL | `<script src="https://vendor.example/sdk.js">` | Low false positive |
| DOM fingerprint | vendor-specific `id` or CSS class | Low–medium |
| Config flag | JS config boolean enabling the vendor | Low |
| Domain substring | `".vendor.example" in webpage` | **High** — matches CSP allowlists and privacy-policy links |

When you audit a surprising hit, open `meta_info` first. A `subdomains`-only hit with no `scripts` / `iframes` is often not a live SDK.

## Local run

```bash
cd analysis
uv sync
uv run python -m prevalence.main \
  --input-dir /path/to/pages \
  --output-dir /path/to/json \
  -n 4 -w 0
# repeat -w 1,2,3 or use crawl/deploy/analyze.sh on a VM
uv run python -m prevalence.combine -i /path/to/json -o prevalence.csv
```

Tests (from `analysis/`):

```bash
uv run pytest prevalence/check_site/check_site_test.py
```

## Adding a detector

1. Copy a small detector in `analysis/prevalence/avp/`.
2. Return a `dict[str, bool]` of named checks.
3. Register the class in `DETECTORS` inside `avp/__init__.py`.
4. Prefer script `src` / iframe `src` over a raw domain-substring check.

## Named vs generic

Headline prevalence numbers use **named** vendor detectors only. Columns `CatchAll`, `CmpAgeVerif`, `Generic`, and `Ep` are heuristic age-gate detectors and are reported separately.
