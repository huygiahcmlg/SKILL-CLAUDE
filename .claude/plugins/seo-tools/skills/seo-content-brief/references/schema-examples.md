# Schema Markup Examples — SEO Content Brief

Các đoạn JSON-LD có thể copy trực tiếp vào thẻ `<script>` trong `<head>` của trang.

---

## 1. FAQPage Schema

Dùng khi bài viết có phần FAQ (Câu hỏi thường gặp). Giúp Google hiển thị rich snippet accordion trên SERP.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Lavabo là gì? Khác gì chậu rửa mặt?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Lavabo (hay còn gọi là chậu rửa mặt, bồn rửa tay) là thiết bị vệ sinh dùng để rửa tay và mặt, thường được lắp đặt trong phòng tắm hoặc nhà vệ sinh. Tên gọi 'lavabo' có nguồn gốc từ tiếng Pháp. Về cơ bản, lavabo và chậu rửa mặt là một, chỉ khác tên gọi theo vùng miền."
      }
    },
    {
      "@type": "Question",
      "name": "Nên chọn lavabo treo tường hay âm bàn?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Lavabo treo tường phù hợp cho phòng tắm nhỏ vì tiết kiệm diện tích, dễ vệ sinh sàn. Lavabo âm bàn phù hợp khi bạn muốn lắp kết hợp với mặt đá/gỗ, tạo cảm giác sang trọng hơn nhưng cần không gian rộng hơn."
      }
    },
    {
      "@type": "Question",
      "name": "Thương hiệu lavabo nào tốt nhất?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Các thương hiệu lavabo được đánh giá tốt tại Việt Nam gồm: INAX (Nhật Bản) — men sứ cao cấp, bền; TOTO (Nhật Bản) — công nghệ hàng đầu; Caesar (Đài Loan) — giá hợp lý, mẫu đa dạng; Viglacera (Việt Nam) — giá tốt, phổ biến. Lựa chọn phụ thuộc vào ngân sách và nhu cầu."
      }
    },
    {
      "@type": "Question",
      "name": "Lavabo dùng được bao lâu?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Lavabo sứ chất lượng tốt có thể dùng 15-30 năm nếu được bảo quản đúng cách. Các thương hiệu lớn như INAX, TOTO thường bảo hành từ 3-10 năm tùy sản phẩm."
      }
    },
    {
      "@type": "Question",
      "name": "Giá lavabo dao động bao nhiêu?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Giá lavabo tại Việt Nam dao động từ 500.000đ đến trên 10 triệu đồng tùy loại và thương hiệu: Phổ thông (Viglacera, nội địa): 500.000 - 1.500.000đ; Tầm trung (Caesar, Hita): 1.500.000 - 3.500.000đ; Cao cấp (INAX, TOTO): 3.500.000 - 10.000.000đ+."
      }
    }
  ]
}
</script>
```

**Lưu ý:**
- Mỗi câu hỏi trong `mainEntity` phải khớp chính xác với H3 trong bài
- `text` trong `acceptedAnswer` nên ngắn gọn (50-300 từ), trả lời thẳng
- Tối đa 5-8 câu hỏi là tốt nhất (Google thường hiển thị 3-4)

---

## 2. HowTo Schema

Dùng cho bài hướng dẫn có các bước cụ thể (cách lắp, cách sửa, cách vệ sinh...). Có thể hiển thị rich snippet với các bước trực tiếp trên Google.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Cách lắp lavabo treo tường tại nhà",
  "description": "Hướng dẫn chi tiết cách lắp đặt lavabo treo tường đúng kỹ thuật, an toàn và bền chắc.",
  "totalTime": "PT2H",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "VND",
    "value": "200000"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Lavabo treo tường"
    },
    {
      "@type": "HowToSupply",
      "name": "Vòi lavabo"
    },
    {
      "@type": "HowToSupply",
      "name": "Xi phông thoát nước"
    },
    {
      "@type": "HowToSupply",
      "name": "Keo silicone chống thấm"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Khoan điện"
    },
    {
      "@type": "HowToTool",
      "name": "Mỏ lết, cờ lê"
    },
    {
      "@type": "HowToTool",
      "name": "Thước đo"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Xác định vị trí lắp đặt",
      "text": "Đo và đánh dấu vị trí lắp lavabo trên tường. Lavabo treo tường thường cách sàn 80-85cm. Dùng bút chì đánh dấu 2 điểm bắt vít theo khoảng cách lỗ của giá đỡ."
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Khoan lỗ và cắm tắc kê",
      "text": "Dùng khoan điện khoan 2 lỗ theo điểm đã đánh dấu với mũi khoan phù hợp (thường ∅8mm). Cắm tắc kê nhựa vào 2 lỗ vừa khoan."
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Gắn giá đỡ và lavabo",
      "text": "Vít chặt giá đỡ sắt vào tường qua 2 tắc kê. Đặt lavabo lên giá đỡ, kiểm tra độ thăng bằng bằng thước nivo. Siết chặt bu lông cố định lavabo."
    },
    {
      "@type": "HowToStep",
      "position": 4,
      "name": "Lắp vòi và đường ống nước",
      "text": "Lắp vòi lavabo vào lỗ giữa chậu. Kết nối đường ống cấp nước nóng/lạnh. Dùng băng keo Teflon quấn ren để chống rò rỉ."
    },
    {
      "@type": "HowToStep",
      "position": 5,
      "name": "Lắp xi phông thoát nước",
      "text": "Lắp xi phông (P-trap hoặc S-trap) vào lỗ thoát của chậu. Kết nối với đường thoát nước trong tường. Kiểm tra độ kín bằng cách chạy nước thử."
    },
    {
      "@type": "HowToStep",
      "position": 6,
      "name": "Trám keo silicone",
      "text": "Bơm keo silicone chống thấm dọc theo viền tiếp xúc giữa lavabo và tường để chống rò rỉ nước vào tường. Để khô 24 giờ trước khi sử dụng."
    }
  ]
}
</script>
```

**Lưu ý:**
- `totalTime` theo chuẩn ISO 8601: PT2H = 2 giờ, PT30M = 30 phút
- Mỗi `step` phải có `name` (tiêu đề bước) và `text` (mô tả chi tiết)
- Thêm `image` vào từng step nếu có ảnh minh họa

---

## 3. Article Schema

Dùng cho tất cả bài viết blog/tin tức để khai báo thông tin tác giả, ngày đăng, giúp Google đánh giá E-E-A-T.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Lavabo Là Gì? Top 6 Loại Phổ Biến + Cách Chọn Mua 2026",
  "description": "Tìm hiểu lavabo là gì, 6 loại phổ biến (treo tường, âm bàn, góc...), top thương hiệu INAX, TOTO, Caesar và cách chọn mua phù hợp.",
  "image": "https://example.com/images/lavabo-la-gi.jpg",
  "author": {
    "@type": "Person",
    "name": "Nguyễn Văn A",
    "url": "https://example.com/tac-gia/nguyen-van-a"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Tên Website",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2026-05-11",
  "dateModified": "2026-05-11",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/lavabo-la-gi-cach-chon-mua"
  }
}
</script>
```

---

## 4. BreadcrumbList Schema

Dùng để hiển thị đường dẫn breadcrumb trên SERP (Trang chủ > Danh mục > Bài viết).

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Trang chủ",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Thiết Bị Vệ Sinh",
      "item": "https://example.com/thiet-bi-ve-sinh"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Lavabo Là Gì? Top 6 Loại Phổ Biến + Cách Chọn Mua 2026",
      "item": "https://example.com/lavabo-la-gi-cach-chon-mua"
    }
  ]
}
</script>
```

---

## 5. Kết Hợp Nhiều Schema Trên 1 Trang

Có thể đặt nhiều `<script type="application/ld+json">` riêng biệt, hoặc dùng `@graph`:

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "Lavabo Là Gì? Top 6 Loại Phổ Biến + Cách Chọn Mua 2026",
      "datePublished": "2026-05-11",
      "author": { "@type": "Person", "name": "Tác giả" }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Lavabo là gì?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Lavabo là thiết bị vệ sinh dùng để rửa tay và mặt..."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Trang chủ", "item": "https://example.com" },
        { "@type": "ListItem", "position": 2, "name": "Lavabo là gì", "item": "https://example.com/lavabo-la-gi" }
      ]
    }
  ]
}
</script>
```

---

## Checklist Schema Trước Khi Publish

- [ ] Validate bằng [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Validate JSON syntax bằng [Schema.org Validator](https://validator.schema.org)
- [ ] FAQPage: câu hỏi trong schema khớp chính xác với H3 trong bài
- [ ] HowTo: đủ số bước, `totalTime` điền đúng
- [ ] Article: `dateModified` cập nhật mỗi khi chỉnh sửa bài
- [ ] Không dùng FAQPage cho nội dung có mục đích quảng cáo thuần túy (vi phạm Google guidelines)

---
*Reference bởi `seo-content-brief` skill | Schema.org v26.0*
