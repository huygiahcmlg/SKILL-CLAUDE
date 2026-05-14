#!/usr/bin/env python3
"""
Fetch Google SERP via SerpAPI — UTF-8 safe replacement for fetch-serp.sh.
Usage: python3 fetch-serp.py <keyword> [location] [hl] [gl] [num]
Output: JSON to stdout (pipe or redirect safely)
Requires: SERPAPI_KEY env var
"""
import sys, os, json, urllib.request, urllib.parse

KEYWORD  = sys.argv[1] if len(sys.argv) > 1 else ""
LOCATION = sys.argv[2] if len(sys.argv) > 2 else "Vietnam"
HL       = sys.argv[3] if len(sys.argv) > 3 else "vi"
GL       = sys.argv[4] if len(sys.argv) > 4 else "vn"
NUM      = int(sys.argv[5]) if len(sys.argv) > 5 else 10
API_KEY  = os.environ.get("SERPAPI_KEY", "")

if not API_KEY:
    sys.stderr.write('{"error":"SERPAPI_KEY chua duoc cau hinh. Them vao ~/.claude/settings.json"}\n')
    sys.exit(1)
if not KEYWORD:
    sys.stderr.write('{"error":"Thieu keyword. Cu phap: python3 fetch-serp.py \\"keyword\\""}\n')
    sys.exit(1)

params = urllib.parse.urlencode({
    "engine": "google", "q": KEYWORD, "location": LOCATION,
    "hl": HL, "gl": GL, "num": NUM, "api_key": API_KEY,
})
url = "https://serpapi.com/search.json?" + params
try:
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read().decode("utf-8"))
except Exception as e:
    sys.stderr.write(json.dumps({"error": str(e)}) + "\n")
    sys.exit(1)

# Write UTF-8 bytes directly — avoids Windows console encoding issues on redirect
sys.stdout.buffer.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
