# Crawl setup

Full recipe: crawl the CrUX top 100,000 origins from inside each jurisdiction, save homepage HTML, then run vendor detectors.

The crawler is adapted from the open *Papers, Please* artifact. We ran it on geographically matched GCP VMs so sites that geo-fence age gates still see a local visitor.

## 0. What you will produce

For each country code (`gb`, `au`, `tx`, `fr`, `id`, `ca`):

| Output | Typical size | Meaning |
| --- | --- | --- |
| `pages/{host}.html` | tens of GB | Rendered homepage HTML |
| `results-json/{host}.json` | hundreds of MB | Per-site detector flags |
| `{code}_prevalence.csv` | ~50–80 MB | One row per site, one column per provider |

A named AVP hit is `1` in any vendor-specific detector column, excluding the four generic heuristics (`CatchAll`, `CmpAgeVerif`, `Generic`, `Ep`). That is the headline prevalence population.

## 1. Hardware we used

| Setting | Value |
| --- | --- |
| VM | GCP `e2-standard-16` (16 vCPU, 64 GB RAM) |
| Disk | 250 GB balanced persistent disk |
| OS | Ubuntu 24.04 LTS |
| Crawl workers | 20 |
| Analysis workers | 16 |
| Page load timeout | 25 s + 2 s settle (`crawl/crawler/crawl.py`) |
| Browser | Google Chrome, incognito, xvfb 800×600 |
| Interaction | **None** — homepage GET only |

One 100K crawl is on the order of many hours of wall time plus substantial egress. Budget a GCS bucket for durability; the monitor script rsyncs HTML every ~15 minutes and can auto-stop the VM when workers exit.

## 2. Domain list (CrUX top 100K)

The crawler expects a CSV with header `origin,rank` and full `https://` URLs:

```csv
origin,rank
https://www.example.com,1000
https://docs.google.com,1000
```

CrUX rank bands are coarse (1K / 10K / 50K / 100K). Many sites share rank `1000`.

**How to build a country list**

1. Download a Chrome UX Report country export for the crawl month (we used **14 May 2026** lists). Public CrUX / BigQuery documentation: [Chrome UX Report](https://developer.chrome.com/docs/crux) and the [`chrome-ux-report`](https://console.cloud.google.com/bigquery?p=chrome-ux-report) dataset.
2. Keep the top 100,000 origins for that country (or `us` for Texas, then crawl from a Texas VM).
3. Save as `{code}-top100k.csv` and place it on the VM as `$HOME/{code}-top100k.csv`.

A three-row smoke-test file is in [`crawl/lists/example-domains.csv`](../crawl/lists/example-domains.csv). Do not commit full 100K lists unless you have confirmed redistribution is allowed for your CrUX snapshot.

## 3. Local crawl (small lists only)

Linux (or WSL) with Chrome + Xvfb:

```bash
sudo apt-get update
sudo apt-get install -y xvfb google-chrome-stable   # or install Chrome from Google's .deb

cd crawl/crawler
uv sync

mkdir -p ../../pages ../../logs
head -c 16 /dev/urandom | xxd -p | tr -d '\n' > ../../seed.txt

uv run python main.py ../../lists/example-domains.csv \
  -n 1 -w 0 \
  --seed-file ../../seed.txt \
  --container-output-dir ../../pages \
  --num-targets 3
```

`main.py` flags:

| Flag | Meaning |
| --- | --- |
| `-n / --num-workers` | Total worker count (must match how you shard) |
| `-w / --worker` | This worker’s index, `0 … n-1` |
| `--seed-file` | Shared hex seed so every worker shuffles the CSV the **same** way, then takes every *n*-th row |
| `--num-targets` | How many rows to consider from the shuffled list (100000 for a full run) |
| `--container-output-dir` | Directory for `{host}.html` |
| `--proxy` | Optional SOCKS5 port |

Already-downloaded hosts are skipped. Empty or timed-out visits print `bailing on …` and move on.

**Windows note.** `pyvirtualdisplay` / Xvfb is a Linux path. For a Windows smoke test, run the crawler in WSL or on the Ubuntu VM. Analysis (detectors) can run on Windows if you already have HTML files.

## 4. Full GCP crawl

### 4.1 Create project, VM, and bucket

Replace placeholders. Zones should match the jurisdiction so CDN/geo-fences see a local IP.

```bash
export PROJECT=your-gcp-project
export ZONE=europe-west2-a          # example: London for GB
export REGION=europe-west2
export VM=av-crawl-gb
export BUCKET=gs://your-bucket-gb
export COUNTRY_CODE=gb

gcloud config set project "$PROJECT"

gcloud storage buckets create "$BUCKET" --location="$REGION"

gcloud compute instances create "$VM" \
  --zone="$ZONE" \
  --machine-type=e2-standard-16 \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=250GB --boot-disk-type=pd-balanced \
  --scopes=cloud-platform
```

A copy-paste helper is [`crawl/deploy/provision.sh`](../crawl/deploy/provision.sh).

### 4.2 Copy code and the domain CSV onto the VM

From your laptop, in this repository:

```bash
gcloud compute ssh "crawl@$VM" --zone="$ZONE" --command="mkdir -p crawler deploy analysis pages logs"

gcloud compute scp --recurse crawl/crawler "crawl@$VM:crawler" --zone="$ZONE"
gcloud compute scp --recurse crawl/deploy "crawl@$VM:deploy" --zone="$ZONE"
gcloud compute scp crawl/lists/${COUNTRY_CODE}-top100k.csv "crawl@$VM:${COUNTRY_CODE}-top100k.csv" --zone="$ZONE"

gcloud compute scp --recurse analysis/prevalence "crawl@$VM:analysis/prevalence" --zone="$ZONE"
gcloud compute scp analysis/pyproject.toml "crawl@$VM:analysis/" --zone="$ZONE"
gcloud compute scp analysis/uv.lock "crawl@$VM:analysis/" --zone="$ZONE"
```

On the VM, convert CRLF if you copied from Windows:

```bash
sed -i 's/\r$//' ~/deploy/*.sh ~/crawler/*.py
chmod +x ~/deploy/*.sh
```

### 4.3 Install Chrome, uv, Python deps

```bash
bash ~/deploy/setup.sh
```

This installs Chrome, Xvfb, tmux, `uv`, and runs `uv sync` in `~/crawler`.

### 4.4 Start the crawl

```bash
export COUNTRY_CODE=gb
export GCS_BUCKET=gs://your-bucket-gb
bash ~/deploy/start-crawl.sh
```

What that does:

1. `launch.sh` — warmup Chrome, then 20 `main.py` workers sharing one seed, `--num-targets 100000`.
2. `monitor.sh` — every 60s prints `workers_alive` and page count; every 15 loops rsyncs `~/pages` to `$GCS_BUCKET/pages/`. When all workers exit and page count ≥ `MIN_PAGES_BEFORE_STOP` (default 50,000), uploads logs and **stops the VM**.

Watch progress:

```bash
tail -f ~/monitor.log
tail -f ~/logs/worker-0.log
ls ~/pages | wc -l
```

Resume after a crash: HTML already on disk is skipped. Re-run `start-crawl.sh` (it kills leftover `main.py` processes first). If the VM auto-stopped, start it and run `start-crawl.sh` again; GCS already has a partial mirror.

### 4.5 Run detectors on the VM

After the crawl (or on a copy of `pages/`):

```bash
export COUNTRY_CODE=gb
export GCS_BUCKET=gs://your-bucket-gb
export PAGES=$HOME/pages
export CSV_OUT=$HOME/gb_prevalence.csv
bash ~/deploy/analyze.sh
```

This starts 16 workers of `python -m prevalence.main`, waits until they exit, combines JSON → CSV, prints a provider histogram, and uploads to GCS.

If analysis dies mid-way, `resume-analysis.sh` continues (JSON files already written are left in place; `main.py` overwrites per file).

## 5. Interpreting `{code}_prevalence.csv`

Important columns:

| Column | Meaning |
| --- | --- |
| `name` | Hostname as crawled |
| `is_empty` | Zero-byte download |
| `parse_error` | BeautifulSoup failed |
| `cloudflare` | Cloudflare challenge/error page |
| `rta` | RTA-5042 meta tag (self-labelled adult) |
| `meta_info` | JSON of which detector checks fired, e.g. `{"Vendor": ["subdomains"]}` |
| Provider columns | `1` if that vendor’s detector fired |

Headline **named AVP** count:

```python
import pandas as pd
df = pd.read_csv("gb_prevalence.csv")
meta = {"Unnamed: 0", "name", "is_empty", "parse_error", "cloudflare", "rta", "meta_info"}
generic = {"CatchAll", "CmpAgeVerif", "Generic", "Ep"}
providers = [c for c in df.columns if c not in meta and c not in generic]
named = df[providers].fillna(0).astype(int).max(axis=1) == 1
print(int(named.sum()), "named AVP sites")
```

`meta_info` tells you *why* a vendor was flagged. A hit on `subdomains` alone (vendor domain string anywhere in HTML) can be a CSP allowlist, not a live SDK.

## 6. Limits

These follow from homepage-only crawling:

- Age gates behind login, payment, or interior pages are invisible.
- Server-side / “headless” age checks leave no client-side script.
- Some vendors also sell KYC; a detector hit is not always an *age* gate.
- Broad domain-string checks (`subdomains`) overcount CSP and documentation links.
- Bot-blocking (Cloudflare) depresses prevalence slightly.

Treat every prevalence number as a **lower bound**.

## 7. Docker (optional)

`crawl/crawler/Dockerfile` builds Ubuntu + Chrome. The production crawl used bare VMs (`setup.sh`), not Docker, because 20 parallel Chrome instances are simpler on a dedicated 16-vCPU machine with a large disk.
