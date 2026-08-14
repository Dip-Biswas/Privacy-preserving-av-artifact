#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
COUNTRY_CODE="${COUNTRY_CODE:-id}"
PAGES="${PAGES:-$HOME/pages}"
JSON_OUT="${JSON_OUT:-$HOME/results-json}"
CSV_OUT="${CSV_OUT:-$HOME/${COUNTRY_CODE}_prevalence.csv}"
NUM_WORKERS="${NUM_WORKERS:-16}"
GCS_BUCKET="${GCS_BUCKET:?set GCS_BUCKET}"

mkdir -p "$JSON_OUT" "$HOME/logs"

echo "==> setup analysis env"
cd "$HOME/analysis"
uv sync

echo "==> run detectors ($NUM_WORKERS workers)"
: > "$HOME/analysis_pids.txt"
for i in $(seq 0 $((NUM_WORKERS - 1))); do
  nohup uv run python -m prevalence.main \
    --input-dir "$PAGES" \
    --output-dir "$JSON_OUT" \
    -n "$NUM_WORKERS" -w "$i" \
    > "$HOME/logs/analysis-$i.log" 2>&1 &
  echo $! >> "$HOME/analysis_pids.txt"
  sleep 0.3
done

echo "==> waiting for analysis workers"
while true; do
  alive=0
  while read -r pid; do
    [ -z "$pid" ] && continue
    kill -0 "$pid" 2>/dev/null && alive=$((alive + 1))
  done < "$HOME/analysis_pids.txt"
  count=$(find "$JSON_OUT" -maxdepth 1 -name '*.json' | wc -l)
  echo "$(date -u +%H:%M:%S) analysis_workers=$alive json_files=$count"
  [ "$alive" -eq 0 ] && break
  sleep 60
done

echo "==> combine to CSV"
uv run python -m prevalence.combine -i "$JSON_OUT" -o "$CSV_OUT"

echo "==> summary"
uv run python3 - <<'PY'
import os
import pandas as pd
from pathlib import Path

csv_path = Path(os.environ.get("CSV_OUT", str(Path.home() / "id_prevalence.csv")))
df = pd.read_csv(csv_path)
meta = {"name", "is_empty", "parse_error", "cloudflare", "rta", "meta_info"}
generic = {"CatchAll", "CmpAgeVerif", "Generic", "Ep"}
providers = [c for c in df.columns if c not in meta and c not in generic]

def col_sum(col):
    return int((df[col].fillna(0).astype(int) == 1).sum())

any_av = df[providers + list(generic)].fillna(0).astype(int).max(axis=1)
named = df[providers].fillna(0).astype(int).max(axis=1)

print(f"Total sites analyzed:     {len(df)}")
print(f"Empty pages:              {col_sum('is_empty')}")
print(f"Parse errors:             {col_sum('parse_error')}")
print(f"Cloudflare blocked:       {col_sum('cloudflare')}")
print(f"RTA label present:        {col_sum('rta')}")
print(f"Any AV signal (incl gen): {(any_av == 1).sum()}")
print(f"Named provider detected:  {(named == 1).sum()}")
print()
print("Top providers (raw detector hits):")
counts = sorted(((p, col_sum(p)) for p in providers), key=lambda x: -x[1])
for p, c in counts[:25]:
    if c:
        print(f"  {p:20s} {c:6d}  ({c/len(df)*100:.2f}%)")
PY

echo "==> upload results"
STAMP="$(date -u +%Y%m%d-%H%M%S)"
gcloud storage cp "$CSV_OUT" "$GCS_BUCKET/analysis/${COUNTRY_CODE}_prevalence-$STAMP.csv"
gcloud storage rsync -r "$JSON_OUT" "$GCS_BUCKET/analysis/json-$STAMP/"

echo "==> analysis complete"
