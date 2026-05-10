# SEO Tools Plugin

Bộ công cụ SEO tích hợp **SerpAPI** - tối ưu cho thị trường Việt Nam.

## Skills Bao Gồm

### 📋 `seo-content-brief`
Tạo content brief SEO chuyên sâu bằng cách phân tích dữ liệu thực từ Google SERP.

**Cách dùng:**
```
/seo-content-brief <keyword>
/seo-content-brief "bán hàng online"
/seo-content-brief "học SEO" --gl vn --hl vi
```

**Output:** Brief đầy đủ gồm:
- Phân tích Search Intent
- Top 10 đối thủ SERP
- People Also Ask (PAA)
- Từ khóa chính + phụ + LSI
- Cấu trúc H1/H2/H3 đề xuất
- Hướng dẫn viết (word count, tone, góc độ độc đáo)
- Meta title, meta description
- Internal linking gợi ý
- Checklist trước publish

---

## Cài Đặt

### 1. Đăng ký SerpAPI
- Truy cập: https://serpapi.com
- Free tier: **100 searches/tháng** miễn phí
- Lấy API key tại: https://serpapi.com/manage-api-key

### 2. Cấu hình API Key
Thêm vào `~/.claude/settings.json`:

```json
{
  "env": {
    "SERPAPI_KEY": "your_serpapi_key_here"
  }
}
```

Hoặc dùng lệnh:
```bash
claude config env set SERPAPI_KEY=your_key_here
```

### 3. Khởi động lại Claude Code
Để biến môi trường được load.

---

## Cấu Trúc Plugin

```
seo-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── seo-content-brief/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── fetch-serp.sh           # Lấy SERP organic + PAA + related
│       │   └── fetch-keyword-ideas.sh  # Lấy autocomplete suggestions
│       └── references/
│           ├── serpapi-docs.md
│           ├── content-brief-template.md
│           └── seo-frameworks.md
└── README.md
```

---

## Yêu Cầu Hệ Thống

- **Bash** (Git Bash trên Windows hoặc WSL)
- **curl** (đã có sẵn trong Git Bash/WSL)
- **Python 3** (cho parsing JSON nếu cần)

---

## Chi Phí Sử Dụng

| Plan | Giá | Searches/tháng |
|------|-----|---------------|
| Free | $0 | 100 |
| Developer | $50 | 5,000 |
| Production | $130 | 30,000 |

> Mỗi lần chạy `/seo-content-brief` = **2 search credits** (1 cho SERP, 1 cho autocomplete)

---

## Roadmap (Tương Lai)

- [ ] Skill `seo-keyword-research` - nghiên cứu cụm từ khóa hàng loạt
- [ ] Skill `serp-monitor` - theo dõi vị trí từ khóa định kỳ
- [ ] Skill `competitor-analysis` - phân tích chuyên sâu đối thủ top 3
- [ ] Tích hợp xuất Google Docs / Notion

---

## Tác Giả

Created with Claude Code | Email: huygiahcmlg@gmail.com
