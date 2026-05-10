# SerpAPI - Tài Liệu Tham Khảo

## Xác Thực
- API Key truyền qua tham số: `api_key=YOUR_KEY`
- Không cần Basic Auth (khác DataForSEO)

## Cấu Hình Biến Môi Trường
Thêm vào `~/.claude/settings.json`:
```json
{
  "env": {
    "SERPAPI_KEY": "your_serpapi_key_here"
  }
}
```

## Endpoint Chính: Google Search

### URL
```
GET https://serpapi.com/search.json
```

### Tham Số Quan Trọng
| Tham số | Mô tả | Ví dụ |
|---------|-------|-------|
| `q` | Từ khóa tìm kiếm | `q=bán hàng online` |
| `engine` | Engine tìm kiếm | `engine=google` (mặc định) |
| `location` | Vị trí địa lý | `location=Vietnam` |
| `gl` | Mã quốc gia (Google Country) | `gl=vn` |
| `hl` | Ngôn ngữ giao diện | `hl=vi` |
| `num` | Số kết quả trả về | `num=10` (max 100) |
| `start` | Offset (phân trang) | `start=10` |
| `api_key` | API key | `api_key=xxx` |

### Cài Đặt Mặc Định Cho Việt Nam
```
location=Vietnam
gl=vn
hl=vi
num=10
```

## Cấu Trúc Response

### Kết Quả Organic
```json
{
  "organic_results": [
    {
      "position": 1,
      "title": "Tiêu đề trang",
      "link": "https://example.com/page",
      "displayed_link": "example.com › page",
      "snippet": "Mô tả ngắn của trang...",
      "about_this_result": {...},
      "cached_page_link": "...",
      "date": "2024-01-01"
    }
  ]
}
```

### People Also Ask (Câu Hỏi Liên Quan)
```json
{
  "related_questions": [
    {
      "question": "Câu hỏi người dùng hay hỏi?",
      "snippet": "Câu trả lời ngắn...",
      "title": "Nguồn trả lời",
      "link": "https://..."
    }
  ]
}
```

### Related Searches (Tìm Kiếm Liên Quan)
```json
{
  "related_searches": [
    {
      "query": "từ khóa liên quan",
      "link": "https://www.google.com/search?q=..."
    }
  ]
}
```

### Knowledge Graph
```json
{
  "knowledge_graph": {
    "title": "Chủ đề",
    "type": "Loại thực thể",
    "description": "Mô tả...",
    "source": {...}
  }
}
```

## Endpoint Google Autocomplete (Gợi Ý Từ Khóa)

### URL & Tham Số
```
GET https://serpapi.com/search.json?engine=google_autocomplete&q=keyword&gl=vn&hl=vi&api_key=KEY
```

### Response
```json
{
  "suggestions": [
    {
      "value": "gợi ý từ khóa 1",
      "type": "query"
    }
  ]
}
```

## Giới Hạn & Pricing
- Free plan: 100 searches/tháng
- Paid plans: từ $50/tháng (5,000 searches)
- Mỗi lần gọi script = 1 search credit
- Xem tại: https://serpapi.com/pricing

## Xử Lý Lỗi Thường Gặp
| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `Invalid API key` | Key sai hoặc hết hạn | Kiểm tra lại SERPAPI_KEY |
| `Your account has run out of searches` | Hết credit | Nâng cấp plan |
| `Location not found` | Sai tên địa điểm | Dùng `Vietnam` (chính xác) |
| Kết quả rỗng | Keyword không có kết quả | Thử keyword khác |

## Parsing JSON với Python
```bash
# Lấy danh sách title từ organic results
cat response.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('organic_results', []):
    print(f\"{r['position']}. {r['title']} - {r['link']}\")
"

# Lấy danh sách câu hỏi PAA
cat response.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for q in data.get('related_questions', []):
    print(f\"- {q['question']}\")
"
```
