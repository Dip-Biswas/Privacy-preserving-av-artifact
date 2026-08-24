# Age-verification crawl artifact

This repository lets you **replicate a prevalence crawl**: fetch homepages from a CrUX top-100K list, detect third-party age-verification vendors in the HTML, and combine the results into a CSV. It also documents **nine evaluation vectors** (protocol for reviewers) — without shipping exploit code, vendor names, or URLs.

| | |
| --- | --- |
| Crawl setup | [`docs/CRAWL.md`](docs/CRAWL.md) |
| Vendor detectors | [`docs/DETECTORS.md`](docs/DETECTORS.md) |
| Evaluation catalog | [`docs/ATTACKS.md`](docs/ATTACKS.md) |
| Evaluation guides (reviewers) | [`docs/guides/`](docs/guides/README.md) |
| Evaluation notice | [`docs/NOTICE-EVALUATION.md`](docs/NOTICE-EVALUATION.md) |
| Privacy measurement | [`docs/PRIVACY.md`](docs/PRIVACY.md) |

## What is included

1. **Prevalence crawl** — CrUX top 100K homepages from six jurisdictions, Selenium + xvfb, BeautifulSoup detectors.
2. **Adversarial evaluation** — nine vectors against face-based age-verification services, with reviewer protocol in [`docs/guides/`](docs/guides/README.md). No PoCs.
3. **Privacy / network checklist** — what to record and what questions to ask of HAR/WebSocket traces.

## Quick start 

You need Python 3.13+, [uv](https://docs.astral.sh/uv/), Google Chrome, and (on Linux) Xvfb.

```bash
# 1. Crawler
cd crawl/crawler
uv sync
mkdir -p ../../pages
printf 'deadbeefdeadbeefdeadbeefdeadbeef\n' > /tmp/seed.txt
uv run python main.py ../lists/example-domains.csv \
  -n 1 -w 0 \
  --seed-file /tmp/seed.txt \
  --container-output-dir ../../pages \
  --num-targets 3

# 2. Detectors
cd ../../analysis
uv sync
mkdir -p ../results-json
uv run python -m prevalence.main \
  --input-dir ../pages \
  --output-dir ../results-json \
  -n 1 -w 0
uv run python -m prevalence.combine \
  -i ../results-json \
  -o ../results-json/example_prevalence.csv
```

A full 100K crawl is not meant to run on a laptop. Use [`docs/CRAWL.md`](docs/CRAWL.md) for the GCP setup (20 crawl workers on an `e2-standard-16` VM in-region).

## Repository layout

```
crawl/crawler/     Selenium homepage crawler (Chrome + xvfb)
crawl/deploy/      VM setup, 20-way crawl, GCS mirror, 16-way analysis
crawl/lists/       Example domain CSV; how to obtain CrUX top-100K lists
analysis/          Vendor detectors + JSON→CSV combine
docs/              Setup, evaluation catalog, and reviewer protocol guides
```

## Jurisdictions crawled

| Code | Region | Legal context | Example GCP zone |
| --- | --- | --- | --- |
| `gb` | United Kingdom | Online Safety Act 2023 | `europe-west2-a` |
| `au` | Australia | Online Safety Act / industry codes | `australia-southeast1-a` |
| `tx` | Texas (US) | HB 1181 | `us-south1-a` |
| `fr` | France | SREN / Arcom | `europe-west9-a` |
| `id` | Indonesia | PP TUNAS | `asia-southeast2-a` |
| `ca` | Canada | No federal mandate (control) | `northamerica-northeast1-a` |

## Responsible use

Detectors and crawl code measure **which sites load which vendors**. They do not bypass age gates.

[`docs/ATTACKS.md`](docs/ATTACKS.md) and [`docs/guides/`](docs/guides/README.md) describe *what* was evaluated and under what conditions. Read [`docs/NOTICE-EVALUATION.md`](docs/NOTICE-EVALUATION.md) first. This repository does not publish attack scripts, payloads, toolchain install procedures, or vendor names/URLs.

## License

MIT. Crawl/detector modules include software from the *Papers, Please* artifact; see [`NOTICE.md`](NOTICE.md).
