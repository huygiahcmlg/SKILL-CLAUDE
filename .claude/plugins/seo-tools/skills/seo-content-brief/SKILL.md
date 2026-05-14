---
name: seo-content-brief
description: Dùng skill này khi người dùng muốn "tạo content brief SEO", "viết content brief cho keyword", "phân tích SERP", "nghiên cứu từ khóa để viết bài", "tạo outline SEO", "lên kế hoạch nội dung cho [keyword]", hoặc nhắc đến SerpAPI, từ khóa SEO, đối thủ SERP. Also use when user mentions "SEO brief", "content outline", "keyword research" combined with intent to create content.
argument-hint: <keyword> [--location <location>] [--gl <country_code>] [--hl <language_code>]
allowed-tools: [Bash, Read, Write]
user-invocable: true
metadata:
  version: 1.0.0
---

# SEO Content Brief Generator

Tạo content brief chuyên sâu bằng cách phân tích dữ liệu thực từ Google SERP thông qua SerpAPI.

## Tài Liệu Tham Khảo
- `references/serpapi-docs.md` — Cấu hình API và cấu trúc response
- `references/content-brief-template.md` — Template xuất brief
- `references/seo-frameworks.md` — Framework phân tích intent, cấu trúc bài viết
- `references/schema-examples.md` — JSON-LD schema mẫu (FAQPage, HowTo, Article, BreadcrumbList)
- `examples/output-lavabo.md` — Ví dụ output hoàn chỉnh cho keyword "lavabo"

---

## BƯỚC 0: Kiểm Tra Điều Kiện

Trước khi bắt đầu, kiểm tra `SERPAPI_KEY` có trong biến môi trường không:

```bash
echo "${SERPAPI_KEY:0:5}..."
WORK_DIR=$(python3 -c "import tempfile; print(tempfile.gettempdir())")
```

**Nếu key rỗng hoặc không có:** Hướng dẫn người dùng:
1. Đăng ký tại https://serpapi.com (có free tier 100 searches/tháng)
2. Lấy API key tại https://serpapi.com/manage-api-key
3. Thêm vào Claude Code settings: Chạy lệnh `claude config` hoặc thêm trực tiếp vào `~/.claude/settings.json`:
   ```json
   {
     "env": {
       "SERPAPI_KEY": "your_key_here"
     }
   }
   ```
4. Khởi động lại Claude Code và thử lại

**Nếu có key:** Tiếp tục workflow.

---

## BƯỚC 1: Xác Định Keyword Và Tham Số

### Nếu được gọi với argument:
```
/seo-content-brief bán hàng online
/seo-content-brief "học lập trình" --gl vn --hl vi
/seo-content-brief "best coffee shop" --location "Ho Chi Minh City" --gl vn --hl vi
```

### Nếu không có argument:
Hỏi người dùng:
- **Keyword chính** muốn viết bài là gì?
- **Thị trường** (mặc định: Việt Nam / `gl=vn, hl=vi`)
- **Vị trí cụ thể** nếu cần (ví dụ: Hà Nội, TP.HCM)

**Mặc định cho thị trường Việt Nam:**
```
location = "Vietnam"
gl = "vn"
hl = "vi"
num = "10"
```

---

## BƯỚC 2: Thu Thập Dữ Liệu SERP

### 2A: Fetch Kết Quả Organic + PAA + Related Searches

Chạy script `fetch-serp.py`:

```bash
PYTHONIOENCODING=utf-8 python3 ".claude/plugins/seo-tools/skills/seo-content-brief/scripts/fetch-serp.py" \
  "KEYWORD_HERE" "Vietnam" "vi" "vn" "10"
```

Lưu response vào biến để phân tích. Nếu response chứa `"error"`, báo lỗi rõ ràng.

### 2B: Fetch Gợi Ý Từ Khóa (Autocomplete)

Chạy script `fetch-keyword-ideas.sh` để lấy từ khóa liên quan:

```bash
bash ".claude/plugins/seo-tools/skills/seo-content-brief/scripts/fetch-keyword-ideas.sh" \
  "KEYWORD_HERE" \
  "vn" \
  "vi"
```

---

## BƯỚC 3: Phân Tích Dữ Liệu

Sau khi có response JSON, phân tích các phần sau:

### 3A: Phân Tích Organic Results (Top 10)
Từ `organic_results`, trích xuất:
- `position`, `title`, `link`, `snippet`
- Xác định loại domain (brand lớn, blog, forum, ecommerce)
- Xác định loại nội dung mỗi trang (hướng dẫn, listicle, so sánh, landing page)
- Ghi nhận pattern trong title tags (cấu trúc, năm, con số)

### 3B: Phân Tích Search Intent
Dựa trên top 10 results và keyword, phân loại intent:
- **Thông tin (Informational):** Bài hướng dẫn, giải thích thống trị
- **Thương mại (Commercial):** Review, so sánh, top N thống trị  
- **Giao dịch (Transactional):** Trang sản phẩm, landing page thống trị
- **Điều hướng (Navigational):** Brand-specific pages thống trị

Tham khảo `references/seo-frameworks.md` để phân loại chính xác.

### 3C: Khai Thác People Also Ask
Từ `related_questions`:
- Liệt kê tất cả câu hỏi
- Đây là nguồn H2/H3 tiềm năng và FAQ content

### 3D: Khai Thác Related Searches
Từ `related_searches` + autocomplete `suggestions`:
- Tổng hợp danh sách keyword phụ
- Phân nhóm theo chủ đề
- Chọn 5-8 keyword phụ phù hợp nhất

### 3E: Ước Tính Word Count
Dựa trên loại nội dung thống trị trong SERP, tham khảo bảng trong `references/seo-frameworks.md`.

---

## BƯỚC 4: Tạo Content Brief

Dựa trên phân tích, tạo content brief hoàn chỉnh theo template trong `references/content-brief-template.md`.

**Điền đầy đủ tất cả sections:**

### Section 1: Tổng Quan Keyword
- Xác định intent rõ ràng
- Đề xuất loại nội dung phù hợp với SERP
- Gợi ý URL slug tối ưu (dùng dấu gạch ngang, không dấu tiếng Việt)

### Section 2: Phân Tích SERP Top 10
- Bảng đầy đủ với title, domain, loại trang
- Nhận xét tổng hợp về pattern SERP

### Section 3: Câu Hỏi PAA
- Liệt kê tất cả câu hỏi tìm được
- Chú thích câu nào nên thành H2, câu nào thành FAQ

### Section 4: Từ Khóa Chiến Lược
- Keyword chính
- 5-8 keyword phụ từ related searches + autocomplete
- 5-10 từ khóa LSI (gợi ý dựa trên snippets và chủ đề)

### Section 5: Cấu Trúc Nội Dung
- H1 cụ thể (bao gồm keyword, năm nếu phù hợp)
- H2 dựa trên PAA + pattern từ competitors
- H3 chi tiết hơn nếu cần
- Giải thích lý do chọn cấu trúc này

### Section 6: Hướng Dẫn Viết
- Word count cụ thể (min-max)
- Tone giọng văn phù hợp với audience
- Góc độ độc đáo để khác biệt với đối thủ
- Các yếu tố bắt buộc

### Section 7: On-Page SEO
- Meta title (≤60 ký tự, chứa keyword chính)
- Meta description (≤160 ký tự, có CTA)
- URL slug (lowercase, không dấu, dùng gạch ngang)
- Alt text gợi ý cho ảnh chính

### Section 8: Internal Linking
- Gợi ý topic liên quan có thể link đến (nếu người dùng đề cập site của họ)

### Section 9: Checklist
- Checklist đầy đủ để verify trước khi publish

---

## BƯỚC 5: Tùy Chọn Lưu File

Hỏi người dùng có muốn lưu brief ra file không:

```
Bạn có muốn tôi lưu content brief này ra file không?
→ [Y] Lưu ra file Markdown (seo-brief-{keyword}.md)
→ [N] Chỉ hiển thị trên màn hình
```

Nếu đồng ý, lưu vào thư mục làm việc hiện tại với tên: `seo-brief-{keyword-slug}.md`

---

## Xử Lý Lỗi

| Tình huống | Hành động |
|-----------|-----------|
| SERPAPI_KEY không có | Hướng dẫn setup chi tiết (xem Bước 0) |
| API trả về lỗi xác thực | "API key không hợp lệ - kiểm tra lại key tại serpapi.com" |
| Hết search credit | "Tài khoản hết credit - nâng cấp plan tại serpapi.com/pricing" |
| Keyword trả về 0 kết quả | Gợi ý thử keyword rộng hơn hoặc tiếng Anh |
| Response JSON bị lỗi | Thử lại 1 lần, nếu vẫn lỗi báo người dùng kiểm tra kết nối |

---

## Ví Dụ Sử Dụng

```
/seo-content-brief học lập trình python
/seo-content-brief "phần mềm quản lý bán hàng"
/seo-content-brief "cà phê rang xay" --location "Ha Noi" --gl vn --hl vi
```

## Skill Liên Quan
- `ai-seo` — Tối ưu nội dung cho AI search (ChatGPT, Gemini, Perplexity)
- `programmatic-seo` — Tạo hàng loạt trang SEO theo template
- `copywriting` — Viết nội dung sau khi có brief
- `schema-markup` — Thêm structured data vào bài viết
