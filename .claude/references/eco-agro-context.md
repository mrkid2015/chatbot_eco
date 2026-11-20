# Bối cảnh Eco Agro hiện hành

Chủ dự án cung cấp hai file: `ECO_Du_lieu_san_pham.xlsx` (26 dòng sản phẩm, 2 combo, 2 câu hỏi chưa đáp) và `DB-Chatbot-Chan-Doan-Sau-Benh.xlsx` (143 hồ sơ sâu bệnh, 7 nhóm, 16 câu phân biệt, 96 tin nhật ký). Đã làm sạch ra bản riêng, không sửa nguồn. Giá theo hướng dẫn file lấy từ MISA, chưa có tích hợp.

Nhu cầu đã chốt: Telegram nội bộ, sầu riêng, xì mủ/vàng lá/thối trái, 5 ID đã chỉ định, Gemini API, mẫu ngắn cố định theo ID, không icon, giữ đầy đủ các mục để cập nhật và bật/tắt về sau. Không có bước người duyệt trước trả lời. Chưa có code bot cũ trong workspace; người dùng có thể tạo bot mới.

Đề xuất chạy thử Python + SQLite trên Windows, không cài Docker/Node/DB server. GitHub lưu code và CI; chưa yêu cầu tạo repo hoặc upload dữ liệu. Không dùng chat log làm kiến thức. Các số MRL/PHI/đăng ký là thông tin trong nguồn, chưa được đối chiếu bên ngoài.

Thông tin công ty/giá/tồn kho/liên hệ không có nguồn thì chưa được trả lời như dữ kiện. Xem discovery, báo cáo dữ liệu và kế hoạch Telegram trong `docs/`.
