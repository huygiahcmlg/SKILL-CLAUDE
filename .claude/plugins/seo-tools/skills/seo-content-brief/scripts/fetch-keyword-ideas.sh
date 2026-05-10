#!/bin/bash
# Fetch Google Autocomplete suggestions via SerpAPI
# Usage: ./fetch-keyword-ideas.sh "keyword" [gl] [hl]
# Requires: SERPAPI_KEY env var

KEYWORD="${1:-}"
GL="${2:-vn}"
HL="${3:-vi}"

if [ -z "$SERPAPI_KEY" ]; then
  echo '{"error": "SERPAPI_KEY chưa được cấu hình"}' >&2
  exit 1
fi

if [ -z "$KEYWORD" ]; then
  echo '{"error": "Thiếu keyword"}' >&2
  exit 1
fi

curl -s "https://serpapi.com/search.json" \
  --get \
  --data-urlencode "engine=google_autocomplete" \
  --data-urlencode "q=${KEYWORD}" \
  --data-urlencode "gl=${GL}" \
  --data-urlencode "hl=${HL}" \
  --data-urlencode "api_key=${SERPAPI_KEY}"
