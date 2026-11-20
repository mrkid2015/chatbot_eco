---
name: eco-agro-sales
description: Thiết kế hoặc sửa luồng tư vấn bán hàng, prompt và truy xuất sản phẩm cho chatbot Eco Agro.
---

# Tư vấn bán hàng Eco Agro

Skill này dành cho giai đoạn mở rộng bán hàng. MVP hiện hành dùng `eco-agro-diagnostics`, không triển khai lead/MISA/Messenger hoặc yêu cầu bước duyệt theo quy trình bán hàng để chặn bộ thử Telegram.

1. Đọc `docs/03-san-pham/yeu-cau-mvp.md`, `docs/03-san-pham/chatbot-system-prompt.md` và `.claude/rules/sales-advice.md`.
2. Xác định ý định: hỏi sản phẩm, so sánh, giá, chính sách, để lại nhu cầu hoặc gặp người thật.
3. Xác định dữ liệu nguồn, trạng thái duyệt và độ mới. Thiếu nguồn thì thiết kế phản hồi thiếu thông tin; không tạo sản phẩm hay giá giả dưới tên Eco Agro.
4. Hỏi ngắn gọn từng bước, gợi ý có căn cứ và giải thích vì sao phù hợp. Cho khách chọn chuyển nhân viên.
5. Chỉ ghi nhận lead sau khi khách đồng ý; tách yêu cầu đặt hàng khỏi xác nhận giao dịch.
6. Kiểm tra bằng `docs/03-san-pham/kich-ban-danh-gia.md`; báo rõ kết quả thực chạy và trường hợp còn thiếu hạ tầng.
