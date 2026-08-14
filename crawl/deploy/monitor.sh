#!/usr/bin/env bash
# Monitors crawl workers. Periodically mirrors results to GCS for durability.
# When all workers exit, does a final sync + uploads logs, then stops the VM.
set -uo pipefail

OUTPUT_DIR="${OUTPUT_DIR:-$HOME/pages}"
LOG_DIR="${LOG_DIR:-$HOME/logs}"
GCS_BUCKET="${GCS_BUCKET:?set GCS_BUCKET, e.g. gs://YOUR_BUCKET}"
PIDS_FILE="${PIDS_FILE:-$HOME/worker_pids.txt}"
STOP_WHEN_DONE="${STOP_WHEN_DONE:-1}"
SYNC_EVERY="${SYNC_EVERY:-15}"   # mirror to GCS every N loops (loop=60s)

mirror() {
  gcloud storage rsync -r "$OUTPUT_DIR" "$GCS_BUCKET/pages/" \
    >/dev/null 2>>"$HOME/mirror_err.log" || echo "WARN: rsync failed (see ~/mirror_err.log)"
}

echo "==> monitoring workers from $PIDS_FILE (mirror every $((SYNC_EVERY)) min)"
i=0
while true; do
  alive=0
  while read -r pid; do
    [ -z "$pid" ] && continue
    if kill -0 "$pid" 2>/dev/null; then alive=$((alive + 1)); fi
  done < "$PIDS_FILE"

  count=$(find "$OUTPUT_DIR" -maxdepth 1 -name '*.html' | wc -l)
  echo "$(date -u +%H:%M:%S) workers_alive=$alive pages=$count"

  if [ "$alive" -eq 0 ]; then
    if [ "$count" -lt "${MIN_PAGES_BEFORE_STOP:-50000}" ]; then
      echo "WARN: all workers exited early ($count pages < ${MIN_PAGES_BEFORE_STOP:-50000}); not stopping VM"
      exit 1
    fi
    break
  fi

  i=$((i + 1))
  if [ $((i % SYNC_EVERY)) -eq 0 ]; then
    echo "$(date -u +%H:%M:%S) mirroring to GCS..."
    mirror
  fi
  sleep 60
done

echo "==> crawl finished; final sync + logs"
mirror
STAMP="$(date -u +%Y%m%d-%H%M%S)"
gcloud storage cp -r "$LOG_DIR" "$GCS_BUCKET/logs-$STAMP/" || echo "WARN: log upload failed"
find "$OUTPUT_DIR" -maxdepth 1 -name '*.html' | wc -l > /tmp/final_count.txt
gcloud storage cp /tmp/final_count.txt "$GCS_BUCKET/final_page_count-$STAMP.txt" || true

echo "==> done. results in $GCS_BUCKET/pages/"
if [ "$STOP_WHEN_DONE" = "1" ]; then
  echo "==> stopping this VM"
  NAME="$(curl -s -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/name)"
  ZONE="$(curl -s -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/zone | awk -F/ '{print $NF}')"
  gcloud compute instances stop "$NAME" --zone "$ZONE" --quiet
fi
