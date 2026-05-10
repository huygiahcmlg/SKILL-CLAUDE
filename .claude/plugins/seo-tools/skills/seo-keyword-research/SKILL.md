---
name: seo-keyword-research
description: Dùng skill này khi người dùng muốn "nghiên cứu từ khóa", "tìm keyword SEO", "keyword research cho [chủ đề]", "tìm từ khóa liên quan", "lên danh sách keyword", "phân tích từ khóa", "tìm long-tail keyword", "keyword ideas", "gợi ý từ khóa". Also use when user says "keyword research", "find keywords", "suggest keywords for [topic]".
argument-hint: <seed_keyword> [--gl <country_code>] [--hl <language_code>]
allowed-tools: [Bash, Read, Write]
user-invocable: true
metadata:
  version: 1.0.0
---

# SEO Keyword Research

Nghiên cứu từ khóa hàng loạt từ một seed keyword bằng cách khai thác Google Autocomplete qua SerpAPI. Phân loại theo intent và đề xuất content plan.

**Chi phí:** ~9 SerpAPI credits mỗi lần chạy (8 autocomplete + 1 SERP)

## Tài Liệu Tham Khảo
- `references/intent-signals.md` — Bảng phân loại intent + tín hiệu nhận diện
- `references/keyword-research-template.md` — Template output hoàn chỉnh

---

## BƯỚC 0: Kiểm Tra Điều Kiện

```bash
echo "${SERPAPI_KEY:0:5}..."
```

**Nếu key rỗng:** Hướng dẫn thêm `SERPAPI_KEY` vào `~/.claude/settings.json` và restart Claude Code.

---

## BƯỚC 1: Xác Định Seed Keyword

### Nếu được gọi với argument:
```
/seo-keyword-research lavabo
/seo-keyword-research "máy lọc nước" --gl vn --hl vi
/seo-keyword-research "coffee shop" --gl vn
```

### Nếu không có argument, hỏi:
- **Seed keyword / chủ đề** muốn nghiên cứu là gì?
- **Thị trường** (mặc định: Việt Nam)

**Params mặc định:**
```
gl = "vn"
hl = "vi"
```

Đặt biến:
- `SEED_KEYWORD` = keyword người dùng nhập
- `SLUG` = keyword dạng slug (thường → thay khoảng trắng bằng dấu gạch ngang, bỏ dấu tiếng Việt nếu cần)

---

## BƯỚC 2: Thu Thập Dữ Liệu Autocomplete (8 Credits)

Chạy script batch để lấy gợi ý từ 8 query variants:

```bash
export SERPAPI_KEY="..."  # Lấy từ env hoặc yêu cầu user cung cấp

bash ".claude/plugins/seo-tools/skills/seo-keyword-research/scripts/fetch-autocomplete-variants.sh" \
  "SEED_KEYWORD_HERE" \
  "vn" \
  "vi" \
  "D:/CLAUDE - LE/kw-research-raw.jsonl"
```

Script sẽ gọi autocomplete cho 8 query variants:
1. `[seed]`
2. `cách [seed]`
3. `[seed] là gì`
4. `mua [seed]`
5. `[seed] nào tốt`
6. `[seed] giá rẻ`
7. `[seed] tốt nhất`
8. `[seed] ở đâu`

---

## BƯỚC 3: Thu Thập Dữ Liệu SERP Cho Seed Keyword (1 Credit)

Gọi SERP thực để hiểu mức độ cạnh tranh:

```bash
bash ".claude/plugins/seo-tools/skills/seo-content-brief/scripts/fetch-serp.sh" \
  "SEED_KEYWORD_HERE" \
  "Vietnam" \
  "vi" \
  "vn" \
  "10" > "D:/CLAUDE - LE/kw-research-serp.json"
```

---

## BƯỚC 4: Parse Dữ Liệu Autocomplete

Đọc file JSONL (mỗi dòng = 1 JSON object) và extract tất cả suggestions:

```bash
PYTHONIOENCODING=utf-8 python3 -c "
import json

seen = set()
keywords = []

with open('D:/CLAUDE - LE/kw-research-raw.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            source_query = obj.get('source_query', '')
            response = obj.get('response', {})
            suggestions = response.get('suggestions', [])
            for s in suggestions:
                kw = s.get('value', '').strip()
                if kw and kw not in seen:
                    seen.add(kw)
                    keywords.append({'keyword': kw, 'source': source_query})
        except:
            pass

print(f'TOTAL_UNIQUE: {len(keywords)}')
for k in keywords:
    print(f\"KW|{k['keyword']}|{k['source']}\")
" 2>&1
```

---

## BƯỚC 5: Phân Loại Theo Intent

Dựa trên danh sách keywords đã parse, phân loại từng keyword theo tín hiệu trong `references/intent-signals.md`:

### Quy tắc phân loại:

**Informational** — nếu keyword chứa:
- là gì, là như thế nào, nghĩa là gì, tại sao, vì sao
- cách, hướng dẫn, làm thế nào, làm sao, bước
- có nên, có được không, nên không
- khác nhau, phân biệt, so với (khi chỉ tìm hiểu, chưa mua)

**Commercial Investigation** — nếu keyword chứa:
- tốt nhất, nào tốt, loại nào tốt, chọn loại nào
- review, đánh giá, nhận xét, có tốt không
- top, danh sách tốt nhất, so sánh A và B
- nên mua loại nào, lựa chọn

**Transactional** — nếu keyword chứa:
- mua, đặt hàng, giá, bao nhiêu tiền
- giá rẻ, khuyến mãi, sale, ở đâu mua
- cửa hàng, shop, chỗ nào bán
- chính hãng (kết hợp với intent mua)

**Navigational/Brand** — nếu keyword chứa tên thương hiệu cụ thể.

### Assign điểm ưu tiên:
- ⭐⭐⭐⭐⭐ = Informational long-tail (đuôi dài, dễ rank)
- ⭐⭐⭐⭐ = Informational head + Commercial Investigation
- ⭐⭐⭐ = Transactional (cạnh tranh với ecommerce)
- ⭐⭐ = Brand/Navigational
- ⭐ = Quá chung chung / head term khó rank

---

## BƯỚC 6: Phân Tích SERP Cho Seed Keyword

Đọc `D:/CLAUDE - LE/kw-research-serp.json` để xác định:

```bash
PYTHONIOENCODING=utf-8 python3 -c "
import json

with open('D:/CLAUDE - LE/kw-research-serp.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data.get('organic_results', [])
print(f'Số kết quả organic: {len(results)}')
for r in results[:10]:
    pos = r.get('position', '?')
    title = r.get('title', '')[:60]
    domain = r.get('link', '').split('/')[2] if r.get('link') else ''
    print(f'{pos}. {domain} — {title}')
" 2>/dev/null
```

Từ đó nhận xét:
- Loại trang thống trị (ecommerce, blog, wiki, brand)
- Mức độ cạnh tranh (domain authority cao hay thấp)
- Cơ hội content gap (có bài informational không)

---

## BƯỚC 7: Tạo Keyword Clusters

Nhóm các keywords liên quan theo chủ đề lớn. Thường có:

1. **Cluster Định Nghĩa:** "[seed] là gì", "nghĩa của [seed]", "[seed] có nghĩa là gì"
2. **Cluster Hướng Dẫn:** "cách [seed]", "hướng dẫn [seed]", "làm sao [seed]"
3. **Cluster So Sánh:** "[seed] nào tốt", "so sánh [seed]", "[seed] review"
4. **Cluster Mua Sắm:** "mua [seed]", "[seed] giá", "[seed] ở đâu"
5. **Cluster Đặc Tính:** "[seed] nhỏ", "[seed] cao cấp", "[seed] giá rẻ"
6. **Cluster Thương Hiệu:** "[brand] [seed]" (nếu có brand)

Mỗi cluster → gợi ý 1 pillar article hoặc supporting article.

---

## BƯỚC 8: Tạo Output Hoàn Chỉnh

Dựa trên template trong `references/keyword-research-template.md`, tạo báo cáo đầy đủ với:
- Tổng quan (tổng số keywords, phân bổ intent)
- Bảng keywords nhóm theo intent (Informational / Commercial / Transactional / Brand)
- Phân tích SERP (mức cạnh tranh, cơ hội)
- Content plan 3 giai đoạn (Quick wins / Mid-term / Long-term)
- Keyword clusters + pillar content đề xuất

---

## BƯỚC 9: Dọn Dẹp Temp Files

```bash
del "D:\CLAUDE - LE\kw-research-raw.jsonl" 2>nul
del "D:\CLAUDE - LE\kw-research-serp.json" 2>nul
del "D:\CLAUDE - LE\kw-research-parsed.txt" 2>nul
```

---

## BƯỚC 10: Tùy Chọn Lưu File

Hỏi người dùng:
```
Bạn có muốn lưu kết quả nghiên cứu này ra file không?
→ [Y] Lưu ra file Markdown (kw-research-{keyword}.md)
→ [N] Chỉ hiển thị trên màn hình
```

Nếu đồng ý, lưu vào thư mục làm việc: `kw-research-{keyword-slug}.md`

---

## Xử Lý Lỗi

| Tình huống | Hành động |
|-----------|-----------|
| SERPAPI_KEY không có | Hướng dẫn setup trong BƯỚC 0 |
| Script trả về 0 keywords | Thử seed keyword tiếng Anh hoặc rộng hơn |
| File JSONL rỗng | Kiểm tra API key và kết nối internet |
| Encoding error | Đảm bảo dùng `PYTHONIOENCODING=utf-8` |
| Hết credit (429) | Thông báo user nâng cấp plan tại serpapi.com/pricing |

---

## Ví Dụ Sử Dụng

```
/seo-keyword-research lavabo
/seo-keyword-research "học lập trình"
/seo-keyword-research "cà phê rang xay" --gl vn --hl vi
/seo-keyword-research "máy lọc nước gia đình"
```

## Skill Liên Quan
- `/seo-content-brief [keyword]` — Tạo content brief chi tiết cho keyword đã chọn
