# SEO Tools Plugin

Bộ công cụ SEO tích hợp **SerpAPI** - tối ưu cho thị trường Việt Nam.

## Skills Bao Gồm

### 🔍 `seo-keyword-research` *(New)*
Nghiên cứu từ khóa hàng loạt từ một seed keyword — phân loại intent, gợi ý content plan.

**Cách dùng:**
```
/seo-keyword-research <seed_keyword>
/seo-keyword-research "lavabo"
/seo-keyword-research "máy lọc nước" --gl vn --hl vi
```

**Output:**
- 30-50 từ khóa unique từ Google Autocomplete
- Phân loại theo intent: Informational / Commercial / Transactional / Brand
- Keyword clusters theo chủ đề
- Phân tích SERP seed keyword (mức độ cạnh tranh)
- Content plan 3 giai đoạn (Quick wins / Mid-term / Long-term)

**Chi phí:** ~9 SerpAPI credits/lần (8 autocomplete + 1 SERP)

---

### 🧠 `seo-customer-insight` *(New)*
Phân tích **chân dung khách hàng** và **search intent nhiều tầng** đằng sau seed keyword. Trả lời: Ai là người tìm? Họ ở stage nào? Lo lắng / muốn gì?

**Cách dùng:**
```
/seo-customer-insight <seed_keyword>
/seo-customer-insight "lavabo"
/seo-customer-insight "máy lọc nước" --forums
```

**Output:**
- Phân loại micro-intent 10 nhóm (Định nghĩa / Hướng dẫn / Lo ngại / So sánh / Review / Tư vấn / Giá / Mua / Bảo trì / Tự DIY)
- Map keyword → Customer Journey Stage (Awareness / Consideration / Decision / Retention)
- 2–4 Persona với mức kỹ thuật + câu nói tiêu biểu
- Pain Point Matrix 4 nhóm (💰 Financial / 🛠️ Functional / 😰 Emotional / ⏱️ Time)
- Content angle theo persona + Voice & Tone recommendation
- Content gap: câu hỏi user hỏi mà SERP chưa trả lời tốt

**Chi phí:** ~10–12 SerpAPI credits/lần (1 SERP + 8 autocomplete + 2 forum queries)

---

### 🛡️ `backlink-quality-auditor` *(New v1.4.0)*
Audit backlink profile hiện có từ Google Search Console CSV export. Phát hiện toxic links, phân tích anchor text, tạo disavow file sẵn upload. **0 SerpAPI credit** — thuần offline Python.

**Cách dùng:**
```
/backlink-quality-auditor "D:/exports/top-linking-sites.csv"
/backlink-quality-auditor "D:/exports/sites.csv" --anchor-csv "D:/exports/anchors.csv" --out "D:/audit-2026-05/"
```

**Input bắt buộc:** `top-linking-sites.csv` từ GSC (Tools > Links > Top linking sites > Export)
**Input tùy chọn:** `top-linking-text.csv` cho phân tích anchor distribution

**Output:**
- `disavow.txt` — File chuẩn Google Disavow Tool, sẵn upload
- `toxic-domains.csv` — Bảng chi tiết domain bị flag (review trong Excel)
- `audit-report.json` — Dữ liệu structured
- Báo cáo Markdown: health score + phân loại theo 4 nhóm + anchor distribution + action plan

**Toxic detection 4 nhóm:**
- 🚩 TLD/Domain pattern spam (`.tk`, `.xyz`, casino keywords, autogen patterns)
- 🚩 Foreign language mismatch (Russian/Chinese TLD link đến site VN)
- 🚩 Anchor quality (over-optimization > 30%, commercial spam)
- 🚩 Link pattern đáng ngờ (PBN, directory, free subdomain)

**Chi phí:** 0 credit

---

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

**Chi phí:** ~2 SerpAPI credits/lần

---

## Sub-Agents Bao Gồm

Sub-agents là các agent chuyên dụng được gọi bằng **Agent tool** (không phải slash command). Claude chính sẽ tự động ủy quyền cho sub-agent khi gặp task phù hợp, hoặc bạn có thể yêu cầu trực tiếp.

### 🕵️ `keyword-competitor-research` *(Refactored v1.3.0 — Thin Orchestrator)*
Sub-agent **điều phối** competitor analysis. Tự làm phân tích top 10 SERP + content gap, **delegate** keyword research sang skill `seo-keyword-research` và customer insight sang skill `seo-customer-insight`. Không duplicate logic của skill.

**Khi nào được gọi:**
- User yêu cầu "phân tích đối thủ", "competitor analysis"
- "Tìm content gap", "đối thủ rank gì", "ai đang rank top cho keyword này"
- Cần deep dive cả keyword lẫn ai đang rank

**Phạm vi linh hoạt (user chọn):**
- `quick` — chỉ competitor + SERP features (~1 credit)
- `keyword` — competitor + keyword variations (~10 credits)
- `customer` — competitor + customer insight (~13 credits)
- `full` — tất cả (~23 credits)

**Output:**
- Bản đồ đối thủ top 10 (loại domain, content type, topics chính)
- Phân tích SERP features (featured snippet, PAA, local pack)
- (Delegate) Keyword variations + intent → từ skill `seo-keyword-research`
- (Delegate) Persona + pain point → từ skill `seo-customer-insight`
- **Content Gap Matrix** tổng hợp 3 nguồn (việc cốt lõi của agent)
- Chiến lược content 3 giai đoạn gắn với persona

**Chi phí:** ~1–23 SerpAPI credits tùy scope

---

### 🔗 `offpage-backlink` *(Refactored v1.4.0 — Discover + Audit)*
Sub-agent off-page SEO toàn diện: tìm cơ hội link mới + audit backlink hiện có. Phần audit **delegate** sang skill `backlink-quality-auditor`.

**Khi nào được gọi:**
- "Tìm backlink", "link building", "offpage SEO"
- "Guest post", "tìm resource page", "unlinked mentions"
- "Audit backlink profile", "tìm toxic link", "tạo disavow file"

**Phạm vi linh hoạt:**
- `discover` — chỉ tìm cơ hội link mới (~11 credits)
- `audit` — chỉ audit backlink hiện có qua GSC CSV (0 credit)
- `full` — cả audit + discover

**Output:**
- (Delegate) Backlink health score + disavow.txt → từ skill `backlink-quality-auditor`
- Guest post opportunities + priority scoring
- Resource page targets
- Unlinked brand mentions
- Broken link opportunities
- Skyscraper targets
- Email templates (VN + EN)
- Kế hoạch hành động theo tuần

**Chi phí:** 0–25 SerpAPI credits tùy scope

---

## Bắt Đầu Nhanh (Getting Started)

> Thực hiện 1 lần duy nhất. Sau đó gọi skill bằng `/seo-keyword-research lavabo` là xong.

### Bước 1: Kiểm tra Prerequisites

Mở terminal (Git Bash trên Windows, Terminal trên Mac/Linux) và chạy:

```bash
python3 --version   # Cần Python 3.7+
git --version       # Cần Git (để chạy Git Bash trên Windows)
```

Nếu thiếu: tải Python 3 tại https://python.org/downloads — chọn "Add to PATH" khi cài.

---

### Bước 2: Lấy SerpAPI Key

1. Đăng ký tại **https://serpapi.com** (free tier: 100 searches/tháng)
2. Sau khi đăng nhập, vào **https://serpapi.com/manage-api-key**
3. Copy API key (dạng: `abc123...`)

---

### Bước 3: Thêm Key vào Claude Code Settings

Mở hoặc tạo file `~/.claude/settings.json` (trên Windows: `C:\Users\<tên>\\.claude\settings.json`):

```json
{
  "env": {
    "SERPAPI_KEY": "paste-your-key-here"
  }
}
```

> **Lưu ý:** Nếu file đã có nội dung khác, chỉ thêm phần `"env": { ... }` vào object JSON có sẵn — đừng tạo file mới đè lên.

---

### Bước 4: Khởi Động Lại Claude Code

Đóng Claude Code hoàn toàn và mở lại. Sau đó kiểm tra key đã được load:

```bash
echo "${SERPAPI_KEY:0:8}..."
```

Nếu thấy 8 ký tự đầu key thay vì `...` là thành công.

---

### Bước 5: Chạy Thử

```
/seo-keyword-research lavabo
```

Claude sẽ fetch ~30–50 từ khóa liên quan, phân loại intent, và trả về báo cáo trong ~30 giây. Mỗi lần chạy tốn **9 credits** từ 100 credits/tháng miễn phí.

---

### Quản Lý Credits

| Plan | Giá | Searches/tháng | Phù hợp cho |
|------|-----|----------------|-------------|
| Free | $0 | 100 | Test / 1–2 dự án nhỏ |
| Developer | $50 | 5,000 | Agency nhỏ |
| Production | $130 | 30,000 | Agency lớn |

Chi phí mỗi skill:
- `/seo-keyword-research` = ~9 credits
- `/seo-customer-insight` = ~10–12 credits
- `/seo-content-brief` = ~2 credits
- `/backlink-quality-auditor` = **0 credits** (offline)
- Agent `keyword-competitor-research full` = ~23 credits

---

## Cài Đặt (Chi Tiết)

### Cấu hình API Key (cách khác)

```bash
claude config env set SERPAPI_KEY=your_key_here
```

---

## Cấu Trúc Plugin

```
seo-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── seo-keyword-research/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── fetch-autocomplete-variants.sh  # Batch 8 variant queries
│   │   └── references/
│   │       ├── intent-signals.md               # Intent classification guide
│   │       └── keyword-research-template.md    # Output template
│   ├── seo-customer-insight/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── fetch-forum-discussions.sh     # Forum scraping (webtretho/reddit)
│   │   └── references/
│   │       ├── intent-layers.md                # Micro-intent 2-tier framework
│   │       └── persona-painpoint-template.md   # Output template
│   ├── backlink-quality-auditor/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── audit-backlinks.py             # Offline CSV audit + disavow gen
│   │   └── references/
│   │       ├── toxic-criteria.md               # 4 nhóm toxic detection rules
│   │       └── audit-template.md               # Output report template
│   └── seo-content-brief/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── fetch-serp.py           # Lấy SERP organic + PAA + related (UTF-8 safe)
│       │   ├── fetch-serp.sh           # Legacy — dùng fetch-serp.py thay thế
│       │   └── fetch-keyword-ideas.sh  # Lấy autocomplete suggestions
│       └── references/
│           ├── serpapi-docs.md
│           ├── content-brief-template.md
│           └── seo-frameworks.md
├── agents/
│   ├── keyword-competitor-research.md  # Sub-agent: KW + competitor analysis
│   └── offpage-backlink.md             # Sub-agent: backlink opportunities
└── README.md
```

---

## Yêu Cầu Hệ Thống

- **Python 3.7+** — bắt buộc (dùng cho tất cả API calls và JSON parsing)
- **Bash** — Git Bash trên Windows, Terminal trên Mac/Linux
- **curl** — đã có sẵn trong Git Bash/WSL (chỉ dùng bởi legacy scripts)

---


## Roadmap (Tương Lai)

- [x] Skill `seo-keyword-research` - nghiên cứu cụm từ khóa hàng loạt *(v1.0.0)*
- [x] Skill `seo-content-brief` - tạo content brief chuyên sâu *(v1.0.0)*
- [x] Agent `keyword-competitor-research` - phân tích đối thủ + content gap *(v1.2.0)*
- [x] Agent `offpage-backlink` - tìm cơ hội backlink *(v1.2.0)*
- [x] Skill `seo-customer-insight` - persona + micro-intent + pain point mapping *(v1.3.0)*
- [x] Skill `backlink-quality-auditor` - audit GSC backlinks + tạo disavow file *(v1.4.0)*
- [ ] Skill `serp-monitor` - theo dõi vị trí từ khóa định kỳ
- [ ] Tích hợp xuất Google Docs / Notion

---

## Tác Giả

Created with Claude Code | Email: huygiahcmlg@gmail.com
