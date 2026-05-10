#!/bin/bash
# Fetch Google SERP data via SerpAPI
# Usage: ./fetch-serp.sh "keyword" [location] [hl] [gl] [num]
# Requires: SERPAPI_KEY env var

KEYWORD="${1:-}"
LOCATION="${2:-Vietnam}"
HL="${3:-vi}"
GL="${4:-vn}"
NUM="${5:-10}"

if [ -z "$SERPAPI_KEY" ]; then
  echo '{"error": "SERPAPI_KEY chưa được cấu hình. Chạy: claude config env set SERPAPI_KEY=your_key"}' >&2
  exit 1
fi

if [ -z "$KEYWORD" ]; then
  echo '{"error": "Thiếu keyword. Cú pháp: ./fetch-serp.sh \"keyword\""}' >&2
  exit 1
fi

curl -s "https://serpapi.com/search.json" \
  --get \
  --data-urlencode "q=${KEYWORD}" \
  --data-urlencode "location=${LOCATION}" \
  --data-urlencode "hl=${HL}" \
  --data-urlencode "gl=${GL}" \
  --data-urlencode "num=${NUM}" \
  --data-urlencode "api_key=${SERPAPI_KEY}"
