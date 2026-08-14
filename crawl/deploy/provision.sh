#!/usr/bin/env bash
# Provision a crawl VM, copy this repo's crawler + detectors, and start a crawl.
# Fill in the variables; run from the artifact repository root on a machine with gcloud.
set -euo pipefail

PROJECT="${PROJECT:?set PROJECT}"
ZONE="${ZONE:?set ZONE, e.g. europe-west2-a}"
REGION="${REGION:?set REGION, e.g. europe-west2}"
VM="${VM:?set VM, e.g. av-crawl-gb}"
BUCKET="${BUCKET:?set BUCKET, e.g. gs://your-bucket-gb}"
COUNTRY_CODE="${COUNTRY_CODE:?set COUNTRY_CODE, e.g. gb}"
CSV_LOCAL="${CSV_LOCAL:-crawl/lists/${COUNTRY_CODE}-top100k.csv}"

if [ ! -f "$CSV_LOCAL" ]; then
  echo "ERROR: missing domain CSV $CSV_LOCAL"
  echo "See crawl/lists/README.md"
  exit 1
fi

gcloud config set project "$PROJECT"

if ! gcloud compute instances describe "$VM" --zone="$ZONE" >/dev/null 2>&1; then
  echo "==> creating $VM"
  gcloud storage buckets create "$BUCKET" --location="$REGION" 2>/dev/null || true
  gcloud compute instances create "$VM" \
    --zone="$ZONE" \
    --machine-type=e2-standard-16 \
    --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
    --boot-disk-size=250GB --boot-disk-type=pd-balanced \
    --scopes=cloud-platform
  sleep 30
else
  st=$(gcloud compute instances describe "$VM" --zone="$ZONE" --format='value(status)')
  if [ "$st" = TERMINATED ] || [ "$st" = STOPPED ]; then
    gcloud compute instances start "$VM" --zone="$ZONE"
    sleep 25
  fi
fi

gcloud compute ssh "crawl@$VM" --zone="$ZONE" --command="mkdir -p crawler deploy analysis pages logs"
gcloud compute scp --recurse crawl/crawler "crawl@$VM:crawler" --zone="$ZONE"
gcloud compute scp --recurse crawl/deploy "crawl@$VM:deploy" --zone="$ZONE"
gcloud compute scp "$CSV_LOCAL" "crawl@$VM:${COUNTRY_CODE}-top100k.csv" --zone="$ZONE"
gcloud compute scp --recurse analysis/prevalence "crawl@$VM:analysis/prevalence" --zone="$ZONE"
gcloud compute scp analysis/pyproject.toml "crawl@$VM:analysis/" --zone="$ZONE"
if [ -f analysis/uv.lock ]; then
  gcloud compute scp analysis/uv.lock "crawl@$VM:analysis/" --zone="$ZONE"
fi

gcloud compute ssh "crawl@$VM" --zone="$ZONE" --command="sed -i 's/\r$//' deploy/*.sh && chmod +x deploy/*.sh && bash deploy/setup.sh"
gcloud compute ssh "crawl@$VM" --zone="$ZONE" --command="COUNTRY_CODE=${COUNTRY_CODE} GCS_BUCKET=${BUCKET} bash deploy/start-crawl.sh"

echo "==> crawl started on $VM ($ZONE). SSH and tail ~/monitor.log"
