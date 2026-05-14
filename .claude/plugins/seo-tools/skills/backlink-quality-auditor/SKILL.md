---
name: backlink-quality-auditor
description: Dùng skill này khi người dùng muốn "audit backlink", "kiểm tra backlink", "phân tích backlink hiện có", "tìm toxic backlink", "anchor text distribution", "tạo disavow file", "disavow Google", "backlink xấu", "link spam", "vệ sinh backlink profile". Also use when user says "audit my backlinks", "check toxic links", "generate disavow file", "anchor distribution analysis".
argument-hint: <path_to_top_linking_sites_csv> [--anchor-csv <path>] [--out <output_dir>]
allowed-tools: [Bash, Read, Write]
user-invocable: true
metadata:
  version: 1.0.0
---

# Backlink Quality Auditor

Phân tích **backlink profile hiện có** từ Google Search Console CSV export. Phát hiện toxic links, phân tích anchor text distribution, và tạo **disavow file** sẵn upload lên Google Search Console.

**Chi phí:** 0 credit (thuần offline Python — không gọi SerpAPI).

**Input bắt buộc:**
- File CSV `top-linking-sites.csv` từ GSC (Tools > Links > Top linking sites > Export)

**Input tùy chọn:**
- File CSV `top-linking-text.csv` từ GSC (Top linking text > Export) — để phân tích anchor distribution

## Tài Liệu Tham Khảo
- `references/toxic-criteria.md` — 4 nhóm tiêu chí + scoring + ví dụ
- `references/audit-template.md` — Template output báo cáo

---

## BƯỚC 0: Xác Định File Input

### Nếu được gọi với argument:
```
/backlink-quality-auditor "D:/exports/top-linking-sites.csv"
/backlink-quality-auditor "D:/exports/sites.csv" --anchor-csv "D:/exports/anchors.csv"
/backlink-quality-auditor "D:/exports/sites.csv" --out "D:/audit-output/"
```

### Nếu không có argument, hỏi:
1. **Đường dẫn tới `top-linking-sites.csv`** từ GSC (bắt buộc)
2. **Đường dẫn tới `top-linking-text.csv`** (tùy chọn)
3. **Thư mục output** (mặc định: thư mục hiện tại)
4. **Domain của bạn** (để loại internal links — tùy chọn)

### Hướng dẫn user export từ GSC:
> Search Console → property của bạn → Tools (sidebar) → Links → Top linking sites → More → Export → Download CSV
>
> Lặp lại với "Top linking text" để có anchor data.

---

## BƯỚC 1: Chạy Audit Script

```bash
PYTHONIOENCODING=utf-8 python3 \
  ".claude/plugins/seo-tools/skills/backlink-quality-auditor/scripts/audit-backlinks.py" \
  --sites "<PATH_TO_LINKING_SITES_CSV>" \
  [--anchors "<PATH_TO_ANCHOR_TEXT_CSV>"] \
  [--my-domain "<USER_DOMAIN>"] \
  --out "<OUTPUT_DIR>"
```

Script sẽ tạo các file trong `<OUTPUT_DIR>`:
- `audit-report.json` — Dữ liệu structured cho LLM tổng hợp
- `disavow.txt` — File sẵn upload lên Google Disavow Tool
- `toxic-domains.csv` — Bảng chi tiết domain bị flag (cho user review)

---

## BƯỚC 2: Đọc Kết Quả Audit

```bash
PYTHONIOENCODING=utf-8 python3 -c "
import json
with open('<OUTPUT_DIR>/audit-report.json', 'r', encoding='utf-8') as f:
    r = json.load(f)
print('=== TỔNG QUAN ===')
print(f\"Total linking domains: {r['summary']['total_domains']}\")
print(f\"Clean: {r['summary']['clean']} ({r['summary']['clean_pct']}%)\")
print(f\"Suspicious: {r['summary']['suspicious']} ({r['summary']['suspicious_pct']}%)\")
print(f\"Toxic: {r['summary']['toxic']} ({r['summary']['toxic_pct']}%)\")
print()
print('=== TOP 20 TOXIC ===')
for d in r['toxic_domains'][:20]:
    print(f\"{d['domain']} | score={d['toxic_score']} | flags={','.join(d['flags'])}\")
print()
print('=== ANCHOR DISTRIBUTION ===')
for a in r.get('anchor_analysis', {}).get('top_anchors', [])[:15]:
    print(f\"{a['anchor']} | count={a['count']} | category={a['category']} | over_opt={a['over_optimized']}\")
" 2>&1
```

---

## BƯỚC 3: Phân Tích & Diễn Giải

Dựa trên `audit-report.json`, viết phân tích theo template `references/audit-template.md`:

### 3.1 — Health Score Tổng Quan

| Toxic % | Đánh giá | Hành động |
|---------|---------|-----------|
| < 5% | 🟢 Lành mạnh | Theo dõi định kỳ |
| 5–15% | 🟡 Cần dọn dẹp | Disavow nhóm toxic cao |
| 15–30% | 🟠 Cảnh báo | Disavow + audit nguồn link mới |
| > 30% | 🔴 Nghiêm trọng | Disavow ngay + xem có Manual Action không |

### 3.2 — Phân Loại Toxic Theo 4 Nhóm

Đếm flag từ `flags[]` của mỗi domain, group theo:
- 🚩 **TLD/Domain pattern spam** (tld_spam, autogen_pattern, casino_adult_kw)
- 🚩 **Foreign language mismatch** (foreign_tld, foreign_kw_in_domain)
- 🚩 **Anchor quality** (over_optimized, commercial_spam_anchor, foreign_anchor)
- 🚩 **Link pattern đáng ngờ** (free_subdomain, directory_pattern, pbn_indicator)

### 3.3 — Anchor Text Distribution

Nếu có anchor CSV, phân tích theo category:
- **Branded** — chứa tên brand (an toàn, nên chiếm 30–60%)
- **Exact-match** — keyword chính xác (cảnh báo nếu > 30%)
- **Partial-match** — biến thể keyword (10–25% là tốt)
- **Generic** — "click here", "tại đây", "website" (10–20% là tự nhiên)
- **Naked URL** — URL trần
- **Spam/Foreign** — commercial spam hoặc tiếng nước ngoài (cần disavow)

⚠️ **Cảnh báo over-optimization** nếu exact-match anchor > 30% tổng anchor.

---

## BƯỚC 4: Tạo Báo Cáo Cuối + Disavow File

Output cho user:
1. **Báo cáo audit** (theo template, hiển thị trên màn hình)
2. **Thông báo file disavow đã tạo:** `<OUTPUT_DIR>/disavow.txt`
3. **Hướng dẫn upload:**

```
Cách upload disavow.txt:
1. Truy cập: https://search.google.com/search-console/disavow-links-tool
2. Chọn property
3. Click "Disavow links" → Upload file disavow.txt
4. Đợi 4–8 tuần để Google xử lý
⚠️ LƯU Ý: Chỉ disavow khi CHẮC CHẮN. Disavow nhầm có thể mất ranking.
```

---

## BƯỚC 5: Hỏi Lưu File Báo Cáo

Hỏi user có muốn lưu báo cáo Markdown thành `backlink-audit-<YYYY-MM-DD>.md` trong `<OUTPUT_DIR>` không.

---

## Xử Lý Lỗi

| Tình huống | Hành động |
|-----------|-----------|
| File CSV không tồn tại | Báo path không đúng + hướng dẫn export GSC |
| CSV không có header expected | Hiển thị header thực + hỏi user mapping column |
| Encoding error | Script tự thử utf-8 → utf-8-sig → cp1252 |
| 0 domain trong CSV | Báo CSV rỗng, kiểm tra lại export |
| Tất cả domain "clean" | Báo profile sạch, không cần disavow |

---

## Ví Dụ Sử Dụng

```
/backlink-quality-auditor "D:/seo/gsc-export/top-linking-sites.csv"

/backlink-quality-auditor "D:/seo/sites.csv" \
  --anchor-csv "D:/seo/anchors.csv" \
  --my-domain "lavabosaigon.vn" \
  --out "D:/seo/audit-2026-05/"
```

## Skill / Agent Liên Quan
- Agent `offpage-backlink` — Gọi skill này như 1 phase "audit" trong workflow link building tổng thể
- `/seo-content-brief` — Sau khi disavow xong, build content mới với anchor strategy lành mạnh
