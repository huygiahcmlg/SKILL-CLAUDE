#!/bin/bash
# Fetch Google Autocomplete for seed keyword + 7 strategic variants
# Uses Python urllib to handle Vietnamese UTF-8 encoding correctly on Windows
# Usage: fetch-autocomplete-variants.sh <seed> <gl> <hl> <output_file>
# Costs: 8 SerpAPI credits per run

SEED="${1:-}"
GL="${2:-vn}"
HL="${3:-vi}"
OUTPUT_FILE="${4:-./kw-research-raw.jsonl}"

if [ -z "$SERPAPI_KEY" ]; then
  echo '{"error": "SERPAPI_KEY chưa được cấu hình. Thêm vào ~/.claude/settings.json"}' >&2
  exit 1
fi

if [ -z "$SEED" ]; then
  echo '{"error": "Thiếu seed keyword"}' >&2
  exit 1
fi

PYTHONIOENCODING=utf-8 python3 - << PYEOF
import urllib.request, urllib.parse, json, time, sys

API_KEY = "${SERPAPI_KEY}"
GL = "${GL}"
HL = "${HL}"
SEED = "${SEED}"
OUTPUT_FILE = r"${OUTPUT_FILE}"

# 8 strategic query variants
QUERIES = [
    SEED,
    "cách " + SEED,
    SEED + " là gì",
    "mua " + SEED,
    SEED + " nào tốt",
    SEED + " giá rẻ",
    SEED + " tốt nhất",
    SEED + " ở đâu",
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for query in QUERIES:
        params = urllib.parse.urlencode({
            "engine": "google_autocomplete",
            "q": query,
            "gl": GL,
            "hl": HL,
            "api_key": API_KEY
        })
        url = "https://serpapi.com/search.json?" + params
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            obj = {"source_query": query, "response": data}
        except Exception as e:
            obj = {"source_query": query, "response": {"error": str(e), "suggestions": []}}

        out.write(json.dumps(obj, ensure_ascii=False) + "\n")
        time.sleep(0.3)

print(OUTPUT_FILE)
PYEOF
