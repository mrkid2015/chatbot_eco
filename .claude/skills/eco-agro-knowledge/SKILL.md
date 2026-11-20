---
name: eco-agro-knowledge
description: Chuẩn hóa catalog, chính sách và tài liệu làm nguồn kiến thức cho chatbot Eco Agro.
---

# Chuẩn hóa nguồn kiến thức

1. Đọc `.claude/references/eco-agro-context.md` và các mẫu trong `docs/05-mau/`.
2. Chỉ nhận nguồn do người dùng cung cấp hoặc chỉ rõ; không tự ghép dữ liệu của doanh nghiệp trùng tên trên Internet.
3. Ghi mã sản phẩm, nguồn, ngày cập nhật, hiệu lực và trạng thái gốc; không thêm cổng người duyệt trong MVP Telegram theo yêu cầu chủ dự án. Phân biệt trường trống với giá trị 0.
4. Phát hiện mã trùng, giá thiếu đơn vị tiền, chính sách mâu thuẫn, tài liệu hết hiệu lực; báo lại trước khi nạp.
5. Nhật ký khách/PII/bí mật không thuộc kho kiến thức. Bản thử nội bộ được dùng dữ liệu chủ dự án chỉ định; trạng thái Nháp không tự chặn việc nhập. Không biến bản nháp thành dữ kiện đã xác minh.
6. Bảo toàn nguồn khi chia đoạn/lập chỉ mục để truy ngược câu trả lời. Giá và tồn kho cần truy vấn nguồn cập nhật thay vì mặc định tin đoạn văn cũ.
7. Sau khi nạp, kiểm tra truy xuất sản phẩm, câu hỏi không có đáp án, nguồn mâu thuẫn và chỉ dẫn độc hại trong tài liệu.
8. Đọc `docs/02-ky-thuat/data-model.md` và kế hoạch Telegram. Bảo toàn đáp án gốc, chia section đầy đủ; bot dùng short template theo ID, không icon. `data/cleaned/` là staging tái tạo được; cập nhật runtime qua migration/release khi đã build.
