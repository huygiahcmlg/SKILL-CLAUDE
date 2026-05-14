# Search Intent Layers — Framework Phân Loại 2 Tầng

## Triết Lý

Phân loại intent truyền thống (Informational / Commercial / Transactional / Navigational) **chưa đủ** để định hướng content. Cần thêm tầng micro-intent để hiểu **chính xác user đang nghĩ gì**.

---

## Tầng 1: Macro Intent (4 nhóm cũ)

| Macro Intent | Mục tiêu user | Loại content phù hợp |
|--------------|---------------|----------------------|
| Informational | Tìm hiểu, học | Guide, How-to, Definition, FAQ |
| Commercial Investigation | So sánh trước khi mua | Listicle, Comparison, Review |
| Transactional | Mua / hành động | Landing page, Product page |
| Navigational | Tìm site/brand cụ thể | Brand page |

---

## Tầng 2: Micro Intent (10 nhóm tâm lý cụ thể)

### 1. `Định nghĩa` — User chưa biết khái niệm
**Tín hiệu:** là gì, nghĩa là, ý nghĩa, định nghĩa, là sao
**Câu hỏi user thật sự muốn hỏi:** "Cái này nó là cái gì?"
**Content cần có:** Giải thích đơn giản + ảnh minh hoạ + ví dụ
**Stage:** Awareness

### 2. `Hướng dẫn` — User muốn tự làm
**Tín hiệu:** cách, hướng dẫn, làm sao, các bước, tutorial
**Câu hỏi:** "Làm cái này như thế nào?"
**Content cần có:** Step-by-step + ảnh từng bước + lưu ý
**Stage:** Awareness / Consideration

### 3. `Lo ngại / Rủi ro` — User có nỗi sợ cụ thể
**Tín hiệu:** có bị, có hại không, an toàn không, có sao không, có nguy hiểm
**Câu hỏi:** "Tôi có nên lo lắng về điều này không?"
**Content cần có:** Reassurance + dữ liệu thực tế + dấu hiệu nhận biết
**Stage:** Consideration

### 4. `So sánh` — User đang phân vân giữa 2+ lựa chọn
**Tín hiệu:** hay, vs, khác nhau, nên chọn loại nào, A or B
**Câu hỏi:** "Cái nào tốt hơn cho tôi?"
**Content cần có:** Bảng so sánh + ưu nhược + use case
**Stage:** Consideration

### 5. `Đánh giá / Review` — User muốn ý kiến của người khác
**Tín hiệu:** review, đánh giá, có tốt không, có nên mua
**Câu hỏi:** "Người khác đã dùng thì sao?"
**Content cần có:** Review chân thực + ưu/nhược + ảnh thực tế
**Stage:** Consideration / Decision

### 6. `Tư vấn / Đề xuất` — User có context cụ thể cần lời khuyên
**Tín hiệu:** nên, gợi ý, loại nào phù hợp, cho [context]
**Câu hỏi:** "Với case của tôi (X) thì nên dùng cái nào?"
**Content cần có:** Decision tree theo use case
**Stage:** Consideration / Decision

### 7. `Giá / Ngân sách` — User đã chốt nhu cầu, đang lọc theo tiền
**Tín hiệu:** giá, bao nhiêu tiền, giá rẻ, tầm giá, dưới X
**Câu hỏi:** "Cái này tốn bao nhiêu? Có phù hợp túi tôi không?"
**Content cần có:** Bảng giá theo phân khúc + ROI / cost-benefit
**Stage:** Decision

### 8. `Mua / Địa điểm` — User sẵn sàng mua
**Tín hiệu:** mua ở đâu, cửa hàng, shop, chính hãng, đặt mua
**Câu hỏi:** "Mua ở đâu uy tín?"
**Content cần có:** Danh sách shop + tip phân biệt chính hãng
**Stage:** Decision

### 9. `Bảo trì / Sửa chữa` — User đã sở hữu, đang gặp vấn đề
**Tín hiệu:** sửa, vệ sinh, làm sạch, thay thế, hỏng, bị lỗi
**Câu hỏi:** "Cái của tôi đang gặp vấn đề, làm sao khắc phục?"
**Content cần có:** Troubleshooting + DIY hoặc liên hệ ai
**Stage:** Retention

### 10. `Tự DIY` — User muốn tiết kiệm, tự làm
**Tín hiệu:** tự làm, tự lắp, tự sửa, DIY, ở nhà
**Câu hỏi:** "Tôi có tự làm được không?"
**Content cần có:** Đánh giá độ khó + dụng cụ cần + cảnh báo khi nào nên thuê thợ
**Stage:** Consideration / Retention

---

## Bảng Map Micro-Intent → Customer Journey Stage

```
AWARENESS (Mới nhận biết vấn đề)
  → Định nghĩa, Hướng dẫn cơ bản

CONSIDERATION (Đang nghiên cứu giải pháp)
  → Lo ngại, So sánh, Tư vấn, Review, Tự DIY

DECISION (Sẵn sàng mua / hành động)
  → Giá, Mua / Địa điểm, Đánh giá (deep review)

RETENTION (Đã sở hữu, cần hỗ trợ)
  → Bảo trì / Sửa chữa, Hướng dẫn nâng cao
```

---

## Quy Tắc Gán Nhãn

1. **Một keyword có thể có nhiều micro-intent** — chọn nhãn chính (mạnh nhất), nhãn phụ ghi trong ngoặc.
   - Ví dụ: "lavabo TOTO có tốt không giá bao nhiêu" → `Đánh giá` (chính) + `Giá` (phụ)

2. **Khi không có tín hiệu rõ** → mặc định gán theo macro-intent:
   - Informational → `Định nghĩa` hoặc `Hướng dẫn`
   - Commercial → `So sánh` hoặc `Đánh giá`
   - Transactional → `Mua / Địa điểm` hoặc `Giá`

3. **Confidence score:**
   - **Cao** = có ít nhất 2 tín hiệu rõ
   - **Trung bình** = có 1 tín hiệu
   - **Thấp** = không có tín hiệu, gán theo phỏng đoán
