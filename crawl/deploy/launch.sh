#!/usr/bin/env bash
# Launches N parallel crawl workers over the domain CSV.
# All workers share ONE seed so the shuffled list is partitioned without overlap.
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/crawler"

COUNTRY_CODE="${COUNTRY_CODE:-id}"
CSV="${CSV:-$HOME/${COUNTRY_CODE}-top100k.csv}"
NUM_WORKERS="${NUM_WORKERS:-20}"
NUM_TARGETS="${NUM_TARGETS:-100000}"
OUTPUT_DIR="${OUTPUT_DIR:-$HOME/pages}"
LOG_DIR="${LOG_DIR:-$HOME/logs}"
SEED_FILE="${SEED_FILE:-$HOME/seed.txt}"

mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

if [ ! -f "$SEED_FILE" ]; then
  head -c 16 /dev/urandom | xxd -p | tr -d '\n' > "$SEED_FILE"
  echo "generated seed: $(cat "$SEED_FILE")"
fi

echo "==> warmup (downloads chromedriver, verifies Chrome works)"
uv run python -c "from crawl import visit_website; visit_website('https://example.com', '$OUTPUT_DIR', output_path='$OUTPUT_DIR/_warmup.html')" \
  > "$LOG_DIR/warmup.log" 2>&1 || true
if [ -s "$OUTPUT_DIR/_warmup.html" ]; then
  echo "    warmup OK ($(wc -c < "$OUTPUT_DIR/_warmup.html") bytes)"
else
  echo "    WARNING: warmup produced no output; check $LOG_DIR/warmup.log"
fi

echo "==> launching $NUM_WORKERS workers (targets=$NUM_TARGETS, csv=$CSV)"
: > "$HOME/worker_pids.txt"
for i in $(seq 0 $((NUM_WORKERS - 1))); do
  nohup uv run python main.py "$CSV" \
    -n "$NUM_WORKERS" -w "$i" \
    --seed-file "$SEED_FILE" \
    --container-output-dir "$OUTPUT_DIR" \
    --num-targets "$NUM_TARGETS" \
    > "$LOG_DIR/worker-$i.log" 2>&1 &
  echo $! >> "$HOME/worker_pids.txt"
  sleep 0.5
done

echo "==> launched. PIDs in ~/worker_pids.txt"
echo "    tail a worker:   tail -f $LOG_DIR/worker-0.log"
echo "    count results:   ls $OUTPUT_DIR | wc -l"
