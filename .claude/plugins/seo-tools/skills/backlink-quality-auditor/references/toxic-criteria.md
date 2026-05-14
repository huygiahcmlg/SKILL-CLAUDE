# Toxic Backlink — Tiêu Chí Phát Hiện

## Triết Lý

Không phải mọi backlink xấu đều cần disavow. Chỉ disavow khi **chắc chắn**. Disavow nhầm = mất ranking.

Skill này flag dựa trên **dấu hiệu khách quan** (TLD, pattern, anchor). User cần **review** kết quả trước khi upload disavow.

---

## 4 Nhóm Tín Hiệu Toxic

### 🚩 Nhóm 1: TLD / Domain Pattern Spam

**Trigger flag:**
- `tld_spam` — TLD trong danh sách free/spam:
  - Free TLDs: `.tk .ml .ga .cf .gq`
  - Cheap spam: `.xyz .top .click .loan .work .date .racing .accountant .faith .review .bid .stream .download .science .party .trade`
- `autogen_pattern` — Domain có pattern auto-generate:
  - Chuỗi ký tự ngẫu nhiên dài (≥12 chars)
  - Domain bắt đầu bằng word + 4+ số
  - Ví dụ: `xkqwlmsa3982.com`, `news4521.net`
- `casino_adult_kw` — Keyword spam trong domain:
  - `casino, poker, betting, gambling, slot, viagra, cialis, porn, xxx, adult, escort, loan, payday, forex`
  - VN: `ca-do, ca-cuoc, sex, khieu-dam`

**Score:** 3–5 điểm.

---

### 🚩 Nhóm 2: Foreign Language Mismatch

**Trigger flag:**
- `foreign_tld` — TLD nước ngoài rủi ro cao khi link đến site VN:
  - `.ru .cn .pl .ro .su .kz .by .ir .ua .rs`
- `foreign_script` — Tên domain chứa ký tự Cyrillic, Trung, Nhật (IDN suspicious)

**Score:** 2 điểm.

> ⚠️ **Lưu ý**: Foreign TLD không phải lúc nào cũng toxic. Nếu user kinh doanh quốc tế hoặc có chi nhánh ở các nước này, **không nên disavow** chỉ dựa trên TLD.

---

### 🚩 Nhóm 3: Anchor Text Quality

**Phân loại anchor:**
- `branded` — Chứa tên brand (an toàn, lý tưởng 30–60%)
- `keyword` — Keyword chính xác/biến thể (lý tưởng 10–25%)
- `generic` — "click here", "tại đây", "website" (lý tưởng 10–20%)
- `naked_url` — URL trần (tự nhiên)
- `foreign` — Anchor tiếng nước ngoài không liên quan
- `spam` — Anchor commercial spam (casino, viagra, loan...)

**Trigger flag:**
- `over_optimized` — Khi % keyword anchor > 30% tổng anchor → over-optimization
- `commercial_spam_anchor` — Anchor chứa từ commercial spam
- `foreign_anchor` — Anchor toàn chữ nước ngoài (Cyrillic, Trung, v.v.)

---

### 🚩 Nhóm 4: Link Pattern Đáng Ngờ

**Trigger flag:**
- `directory_pattern` — Domain chứa `directory/listing/submit/catalog/bookmark`
  - Đa số directory submission cũ là low-quality
- `pbn_indicator` — Pattern numbered subdomain dạng PBN:
  - `blog123.example.com`, `wp42.something.net`, `news888.xyz`
- `free_subdomain` — Free platform (blogspot, wordpress.com, weebly, wix)
  - Flag yếu — chỉ +1 điểm. Free platform có thể chính chủ.

**Score:** 1–3 điểm tùy flag.

---

## Bảng Tổng Hợp Điểm

| Flag | Điểm | Mức độ |
|------|------|--------|
| `casino_adult_kw` | 5 | Rất cao |
| `tld_spam` | 4 | Cao |
| `pbn_indicator` | 3 | Cao |
| `autogen_pattern` | 3 | Cao |
| `foreign_tld` | 2 | Trung |
| `foreign_script` | 2 | Trung |
| `directory_pattern` | 2 | Trung |
| `free_subdomain` | 1 | Thấp |

---

## Phân Loại Cuối Cùng

| Tổng điểm | Status | Hành động đề xuất |
|-----------|--------|--------------------|
| 0 | `clean` | Giữ lại |
| 1–3 | `suspicious` | Review thủ công — KHÔNG tự động disavow |
| ≥ 4 | `toxic` | Đề xuất disavow (vào `disavow.txt`) |

---

## Quy Trình Review (Trước Khi Upload Disavow)

1. **Mở `toxic-domains.csv`** trong Excel/Sheets
2. Với mỗi domain `toxic`:
   - Truy cập domain → check thực tế
   - Nếu là site hợp pháp (cho dù domain xấu) → **xóa khỏi disavow.txt**
   - Nếu thực sự spam/PBN → giữ trong disavow
3. Với domain `suspicious`:
   - Mặc định KHÔNG đưa vào disavow
   - User có thể thêm vào nếu confirm spam

⚠️ **Quy tắc vàng**: *"Khi nghi ngờ, đừng disavow."* Backlink trung tính tốt hơn disavow nhầm.

---

## Disavow File Format (Google chuẩn)

```
# Comment giải thích
domain:spam-domain.com
domain:another-spam.net

# Specific URL (ít dùng — domain-level đủ)
http://specific-spam.com/bad-link
```

- Mỗi dòng 1 entry
- `domain:` prefix → disavow toàn bộ domain (bao gồm subdomain)
- Không có prefix → chỉ disavow URL cụ thể (chỉ dùng khi domain còn link tốt khác)
- Comment bắt đầu bằng `#`
- File: UTF-8, ≤ 100,000 dòng, ≤ 2MB
