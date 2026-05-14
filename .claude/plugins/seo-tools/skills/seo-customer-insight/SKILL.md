---
name: seo-customer-insight
description: Dùng skill này khi người dùng muốn "phân tích khách hàng", "customer insight", "search intent mapping", "phân tích intent chi tiết", "tìm pain point", "persona khách hàng từ keyword", "khách hàng đang tìm gì", "họ lo lắng điều gì", "intent layer", "micro intent". Also use when user says "customer insight for [keyword]", "search intent analysis", "map keyword to persona", "what do customers worry about".
argument-hint: <seed_keyword> [--gl <country_code>] [--hl <language_code>] [--forums]
allowed-tools: [Bash, Read, Write]
user-invocable: true
metadata:
  version: 1.0.0
---

# SEO Customer Insight & Search Intent Mapping

Phân tích sâu **chân dung khách hàng** và **search intent nhiều tầng** đằng sau một seed keyword. Trả lời câu hỏi: *Người tìm keyword này là ai? Họ đang ở giai đoạn nào của quyết định? Họ thật sự lo lắng / mong muốn điều gì?*

**Chi phí:** ~10–12 SerpAPI credits/lần
- 1 SERP (PAA + Related Searches của seed)
- 8 Autocomplete variants
- 1–2 SERP forum (webtretho/reddit/voz)

## Tài Liệu Tham Khảo
- `references/intent-layers.md` — Framework phân loại micro-intent 2 tầng
- `references/persona-painpoint-template.md` — Template output hoàn chỉnh

---

## BƯỚC 0: Kiểm Tra Điều Kiện

```bash
echo "${SERPAPI_KEY:0:5}..."
WORK_DIR=$(python3 -c "import tempfile; print(tempfile.gettempdir())")
```

**Nếu key rỗng:** Hướng dẫn thêm `SERPAPI_KEY` vào `~/.claude/settings.json` và restart Claude Code.

---

## BƯỚC 1: Xác Định Seed Keyword

### Nếu được gọi với argument:
```
/seo-customer-insight lavabo
/seo-customer-insight "máy lọc nước" --gl vn --hl vi
/seo-customer-insight "tủ lạnh side by side" --forums
```

### Nếu không có argument, hỏi:
- **Seed keyword / chủ đề** muốn phân tích là gì?
- **Thị trường** (mặc định: Việt Nam — `gl=vn, hl=vi`)
- **Có quét thêm forum (webtretho/reddit/voz) không?** (mặc định: có)

Đặt biến:
- `SEED_KEYWORD` = keyword người dùng nhập
- `SLUG` = keyword dạng slug (thường, bỏ dấu, thay khoảng trắng → dấu gạch)

---

## BƯỚC 2: Fetch SERP Seed Keyword (1 Credit)

Lấy PAA + Related Searches — đây là nguồn pain point trực tiếp từ user.

```bash
PYTHONIOENCODING=utf-8 python3 ".claude/plugins/seo-tools/skills/seo-content-brief/scripts/fetch-serp.py" \
  "<SEED_KEYWORD>" "Vietnam" "vi" "vn" "10" \
  > "${WORK_DIR}/insight-serp.json"
```

---

## BƯỚC 3: Fetch Autocomplete Variants (8 Credits)

Tái sử dụng script của `seo-keyword-research` để có 30–50 biến thể keyword.

```bash
bash ".claude/plugins/seo-tools/skills/seo-keyword-research/scripts/fetch-autocomplete-variants.sh" \
  "<SEED_KEYWORD>" "vn" "vi" \
  "D:/CLAUDE - LE/insight-kw-variants.jsonl"
```

---

## BƯỚC 4: Fetch Forum Discussions (1–2 Credits, optional)

Nếu user bật `--forums` (mặc định: bật), chạy script lấy thảo luận thật từ forum VN + reddit:

```bash
bash ".claude/plugins/seo-tools/skills/seo-customer-insight/scripts/fetch-forum-discussions.sh" \
  "<SEED_KEYWORD>" "vn" "vi" \
  "D:/CLAUDE - LE/insight-forums.jsonl"
```

Script query 2 lần với operator:
- `<seed> site:webtretho.com OR site:tinhte.vn OR site:voz.vn`
- `<seed> site:reddit.com`

---

## BƯỚC 5: Parse Toàn Bộ Dữ Liệu

```bash
PYTHONIOENCODING=utf-8 python3 - << 'PYEOF'
import json

# ===== 1. PAA + Related từ SERP chính =====
with open('${WORK_DIR}/insight-serp.json', 'r', encoding='utf-8') as f:
    serp = json.load(f)

paa = [q.get('question', '') for q in serp.get('related_questions', []) if q.get('question')]
related = [r.get('query', '') for r in serp.get('related_searches', []) if r.get('query')]

print('=== PAA (People Also Ask) ===')
for q in paa:
    print('-', q)
print()
print('=== RELATED SEARCHES ===')
for r in related:
    print('-', r)
print()

# ===== 2. Autocomplete keywords =====
print('=== AUTOCOMPLETE VARIANTS ===')
seen = set()
with open('${WORK_DIR}/insight-kw-variants.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
            for s in obj.get('response', {}).get('suggestions', []):
                kw = s.get('value', '').strip()
                if kw and kw not in seen:
                    seen.add(kw)
                    print('-', kw)
        except: pass

# ===== 3. Forum discussions =====
print()
print('=== FORUM DISCUSSIONS ===')
try:
    with open('${WORK_DIR}/insight-forums.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                obj = json.loads(line)
                source = obj.get('source_query', '')
                results = obj.get('response', {}).get('organic_results', [])
                print(f'--- Source: {source} ---')
                for r in results[:8]:
                    title = r.get('title', '')[:100]
                    snippet = r.get('snippet', '')[:200]
                    link = r.get('link', '')
                    print(f'TITLE: {title}')
                    print(f'SNIPPET: {snippet}')
                    print(f'URL: {link}')
                    print()
            except: pass
except FileNotFoundError:
    print('(no forum data — --forums was disabled or fetch failed)')
PYEOF
```

---

## BƯỚC 6: Phân Loại Micro-Intent (Theo `intent-layers.md`)

Với mỗi keyword/PAA/forum question, gán **2 nhãn**:

**Tầng 1 — Macro Intent** (theo phân loại cũ):
- Informational / Commercial Investigation / Transactional / Navigational

**Tầng 2 — Micro Intent** (mới — mô tả tâm lý cụ thể):

| Micro Intent | Tín hiệu | Ví dụ |
|--------------|---------|-------|
| `Định nghĩa` | là gì, nghĩa là, ý nghĩa | "lavabo là gì" |
| `Hướng dẫn` | cách, hướng dẫn, làm sao, các bước | "cách lắp lavabo" |
| `Lo ngại / Rủi ro` | có bị, có hại không, an toàn không, có sao không | "lavabo bị tắc phải làm sao" |
| `So sánh` | hay, vs, khác nhau, nên chọn loại nào | "lavabo dương vành hay âm bàn" |
| `Đánh giá / Review` | review, đánh giá, có tốt không, có nên mua | "lavabo TOTO có tốt không" |
| `Tư vấn / Đề xuất` | nên, gợi ý, loại nào phù hợp, cho phòng nhỏ | "lavabo nào cho phòng tắm nhỏ" |
| `Giá / Ngân sách` | giá, bao nhiêu tiền, giá rẻ, tầm | "lavabo dưới 2 triệu" |
| `Mua / Địa điểm` | mua ở đâu, cửa hàng, shop, chính hãng | "mua lavabo TOTO ở đâu" |
| `Bảo trì / Sửa chữa` | sửa, vệ sinh, làm sạch, thay thế | "cách thông lavabo bị tắc" |
| `Tự DIY` | tự làm, tự lắp, tự sửa | "tự lắp lavabo tại nhà" |

Output: bảng `keyword | macro_intent | micro_intent | confidence`.

---

## BƯỚC 7: Suy Luận Persona

Dựa trên TỔ HỢP của:
- Loại micro-intent xuất hiện nhiều
- Ngôn ngữ trong forum (xưng hô, tone)
- Topic của PAA
- Loại site rank top 10

→ Suy ra **2–4 persona** với:
- **Tên gọi** (ví dụ: "Chủ nhà DIY", "Mẹ trẻ tìm sự an toàn", "Designer chuyên nghiệp")
- **Demographic ước lượng** (tuổi, role, mức thu nhập nếu suy được)
- **Mức độ kỹ thuật** (newbie / trung cấp / chuyên gia)
- **Stage trong customer journey** (Awareness / Consideration / Decision / Retention)
- **Top 3 micro-intent đặc trưng** của persona này
- **Câu nói tiêu biểu** (paraphrase 1 câu từ PAA hoặc forum)

⚠️ **Quy tắc bịa số**: KHÔNG được đoán demographic chính xác (ví dụ: "25 tuổi"). Dùng range hoặc qualifier ("trẻ tuổi, có vẻ mới mua nhà").

---

## BƯỚC 8: Trích Xuất Pain Points

Từ forum snippets + PAA "có sao không / có bị / phải làm sao / lo ngại":

Liệt kê dưới dạng bảng:

| Pain Point | Bằng chứng (PAA/forum quote) | Tần suất | Persona ảnh hưởng |
|------------|------------------------------|----------|-------------------|
| Sợ mua phải hàng nhái | "lavabo TOTO chính hãng phân biệt thế nào" — PAA | Cao | Chủ nhà DIY |
| Lo lắng lắp đặt sai | "tự lắp lavabo có khó không" — forum webtretho | Trung | DIYer mới |
| Ngân sách hạn chế | "lavabo dưới 1 triệu" — autocomplete | Cao | Sinh viên / nhà thuê |

**Phân loại pain point thành 4 nhóm**:
1. 💰 **Financial** — giá, ngân sách, hao mòn, tiền điện/nước
2. 🛠️ **Functional** — không hoạt động, lỗi kỹ thuật, không phù hợp
3. 😰 **Emotional** — sợ bị lừa, sợ chọn sai, sợ phán xét
4. ⏱️ **Time** — không có thời gian, muốn nhanh, muốn dễ

---

## BƯỚC 9: Tạo Output Hoàn Chỉnh

Theo template `references/persona-painpoint-template.md`, bao gồm các section:

1. **Tổng quan insight** (3–5 dòng tóm lược)
2. **Bảng phân loại Micro-Intent** (toàn bộ keyword + tag intent)
3. **Phân bổ Intent theo Customer Journey Stage** (% phân bổ Awareness/Consideration/Decision)
4. **Chân dung 2–4 Persona** (mỗi persona = 1 khung)
5. **Pain Point Matrix** (4 nhóm financial/functional/emotional/time)
6. **Content Angle theo Persona** (mỗi persona → 2–3 content idea đáp ứng pain point)
7. **Voice & Tone Recommendations** (gợi ý cách viết phù hợp với ngôn ngữ user)
8. **Câu hỏi user thật sự muốn hỏi mà chưa được trả lời** (gap from PAA + forum)

---

## BƯỚC 10: Dọn Dẹp Temp Files

```bash
rm -f "${WORK_DIR}/insight-serp.json"
rm -f "${WORK_DIR}/insight-kw-variants.jsonl"
rm -f "${WORK_DIR}/insight-forums.jsonl"
```

---

## BƯỚC 11: Tùy Chọn Lưu File

Hỏi user:
```
Bạn có muốn lưu báo cáo này ra file không?
→ [Y] Lưu Markdown: customer-insight-<slug>.md
→ [N] Chỉ hiển thị
```

---

## Xử Lý Lỗi

| Tình huống | Hành động |
|-----------|-----------|
| SERPAPI_KEY rỗng | Dừng, hướng dẫn setup |
| Forum query trả về 0 kết quả | Báo niche, skip pain point từ forum, vẫn làm phần intent + persona |
| PAA rỗng | Báo seed quá hẹp, chỉ làm việc với autocomplete |
| 429 (hết credit) | Báo nâng cấp plan |
| Encoding error | Đảm bảo `PYTHONIOENCODING=utf-8` |

---

## Ví Dụ Sử Dụng

```
/seo-customer-insight lavabo
/seo-customer-insight "máy lọc nước RO"
/seo-customer-insight "học SEO" --gl vn
/seo-customer-insight "tủ lạnh inverter" --forums
```

## Skill / Agent Liên Quan
- `/seo-keyword-research [keyword]` — Bước trước khi làm customer insight
- `/seo-content-brief [keyword]` — Bước sau, dùng persona + pain point để viết brief
- Agent `keyword-competitor-research` — Gọi skill này như 1 phase phân tích
