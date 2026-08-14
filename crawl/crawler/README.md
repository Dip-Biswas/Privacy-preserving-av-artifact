# Page crawler

Selenium + xvfb homepage fetcher used in the six-jurisdiction prevalence crawl.

**Full setup (local + GCP, CrUX lists, analysis):** see [`docs/CRAWL.md`](../../docs/CRAWL.md).

## Minimal local usage

```bash
uv sync
uv run python main.py path/to/domains.csv \
  -n 1 -w 0 \
  --seed-file seed.txt \
  --container-output-dir ./pages \
  --num-targets 100
```

CSV format: `origin,rank` with `https://` URLs. All workers must share the same `--seed-file` so the shuffled list partitions without overlap.
