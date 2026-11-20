---
name: eco-agro-diagnostics
description: Thiết kế và triển khai hỏi đáp sâu bệnh sầu riêng cho MVP Telegram Eco Agro với Gemini và đáp án cố định theo ID.
---

# Hỏi đáp sâu bệnh Eco Agro

1. Đọc `CLAUDE.md`, `.claude/references/project-context.json`, `.claude/rules/diagnostic-chatbot.md` và kế hoạch Telegram.
2. Giữ phạm vi 5 ID đã chọn, không thêm bước người duyệt. Xem SQLite staging và báo cáo nguồn trước khi viết truy vấn/logic.
3. Tách Gemini hiểu lời người dùng khỏi engine bằng chứng/câu hỏi và renderer lấy mẫu. Xác thực JSON, unknown và ID, không chạy thẳng rules nguồn mâu thuẫn.
4. Viết short template cố định và section không icon, giữ toàn bộ dữ liệu gốc/cảnh báo, chia tin không mất đơn vị/ý nghĩa.
5. Kiểm tra ca xác định, mơ hồ, đồng nhiễm, ngoài pilot và lời chào xen ngang; không dùng một ứng viên còn lại làm bằng chứng đủ.
6. Khi triển khai adapter, ưu tiên polling Windows, môi trường riêng, timeout, cô lập phiên và allowlist. Chỉ cần credential ở bước kết nối thật, không yêu cầu gửi khóa qua chat.
7. Báo kết quả kiểm tra dữ liệu/core/runtime/API thật riêng, không báo bot hoạt động khi chưa chạy. Cập nhật tài liệu và đồng bộ cấu hình AI sau khi sửa bản gốc.
