#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:/usr/bin:/bin"

PAGES="${PAGES:-$HOME/pages}"
JSON_OUT="${JSON_OUT:-$HOME/results-json}"
COUNTRY_CODE="${COUNTRY_CODE:-au}"
CSV_OUT="${CSV_OUT:-$HOME/${COUNTRY_CODE}_prevalence.csv}"
NUM_WORKERS="${NUM_WORKERS:-16}"
TIMEOUT_SEC="${TIMEOUT_SEC:-180}"

cd "$HOME/analysis"
uv sync >/dev/null

echo "==> resume missing JSON ($NUM_WORKERS workers, timeout=${TIMEOUT_SEC}s)"
uv run python - <<'PY'
import json
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

pages = os.path.expanduser("~/pages")
out = os.path.expanduser("~/results-json")
timeout_sec = int(os.environ.get("TIMEOUT_SEC", "180"))
workers = int(os.environ.get("NUM_WORKERS", "16"))
analysis = os.path.expanduser("~/analysis")

missing = []
for name in os.listdir(pages):
    if not name.endswith(".html"):
        continue
    base = name[:-5]
    if not os.path.exists(os.path.join(out, base + ".json")):
        missing.append(name)

print(f"missing={len(missing)}", flush=True)
if not missing:
    raise SystemExit(0)

def process(name: str) -> str:
    base = name[:-5]
    json_path = os.path.join(out, base + ".json")
    env = os.environ.copy()
    env["PATH"] = os.path.expanduser("~/.local/bin:") + env.get("PATH", "")
    code = (
        "import json; from prevalence.check_site import check_site; "
        f"row=check_site(('{pages}', '{name}')); "
        f"json.dump(row, open('{json_path}','w'))"
    )
    try:
        subprocess.run(
            ["uv", "run", "python", "-c", code],
            cwd=analysis,
            env=env,
            timeout=timeout_sec,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return "ok"
    except Exception:
        row = {"name": base, "parse_error": 1}
        with open(json_path, "w") as f:
            json.dump(row, f)
        return "fallback"

done = 0
with ProcessPoolExecutor(max_workers=workers) as pool:
    futures = [pool.submit(process, name) for name in missing]
    for fut in as_completed(futures):
        done += 1
        if done % 200 == 0 or done == len(missing):
            print(f"processed {done}/{len(missing)}", flush=True)

print("resume complete", flush=True)
PY

final_json="$(find "$JSON_OUT" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "==> json files now: $final_json"

echo "==> combine to CSV"
uv run python -m prevalence.combine -i "$JSON_OUT" -o "$CSV_OUT"
echo "==> wrote $CSV_OUT"
