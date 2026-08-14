# Prevalence analysis

BeautifulSoup detectors for third-party age-verification providers.

- Full crawl + detect pipeline: [`docs/CRAWL.md`](../docs/CRAWL.md)
- Detector design: [`docs/DETECTORS.md`](../docs/DETECTORS.md)

```bash
uv sync
uv run python -m prevalence.main --input-dir ../pages --output-dir ../results-json -n 1 -w 0
uv run python -m prevalence.combine -i ../results-json -o ../prevalence.csv
```
