#!/bin/bash
# Fetch forum discussions related to a keyword from Vietnamese forums + Reddit via SerpAPI
# Uses site: operator to filter by domain
# Usage: fetch-forum-discussions.sh <seed> <gl> <hl> <output_file>
# Costs: 2 SerpAPI credits per run (1 for VN forums, 1 for Reddit)

SEED="${1:-}"
GL="${2:-vn}"
HL="${3:-vi}"
OUTPUT_FILE="${4:-./insight-forums.jsonl}"

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

# 2 strategic forum queries
QUERIES = [
    SEED + " (site:webtretho.com OR site:tinhte.vn OR site:voz.vn OR site:otofun.net)",
    SEED + " site:reddit.com",
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for query in QUERIES:
        params = urllib.parse.urlencode({
            "engine": "google",
            "q": query,
            "gl": GL,
            "hl": HL,
            "num": 10,
            "api_key": API_KEY
        })
        url = "https://serpapi.com/search.json?" + params
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            obj = {"source_query": query, "response": data}
        except Exception as e:
            obj = {"source_query": query, "response": {"error": str(e), "organic_results": []}}

        out.write(json.dumps(obj, ensure_ascii=False) + "\n")
        time.sleep(0.3)

print(OUTPUT_FILE)
PYEOF
