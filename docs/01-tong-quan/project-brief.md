# Định hướng Eco Agro đã làm rõ

Mục tiêu dài hạn là chatbot tư vấn Eco Agro. Phiên bản đầu ưu tiên nhân viên hỏi đáp sâu bệnh trên Telegram, nhanh, ổn định và nhẹ trên Windows; Messenger/bán hàng mở rộng sau.

Chọn sầu riêng, ba nhóm xì mủ/vàng lá/thối trái, 5 hồ sơ cụ thể trong `docs/03-san-pham/ke-hoach-chatbot-telegram.md`. Gemini hỗ trợ hiểu ngôn ngữ và hội thoại, code truy xuất đáp án cố định theo ID. Không icon, tin ngắn, chia đầy đủ các mục nguồn để dùng hoặc bật/tắt về sau. Không yêu cầu bước duyệt người dùng trước khi trả lời.

Đã nhận hai Excel, làm sạch ra bản riêng và SQLite staging. Không có mã nguồn bot hiện tại trong workspace; chủ dự án có thể tạo bot mới. Chưa kết nối credential, chạy bot hoặc đo tốc độ.

Đọc `requirements-discovery.md` để xem câu hỏi/câu trả lời; `../02-ky-thuat/data-cleaning-report.md` để xem chất lượng dữ liệu; kế hoạch Telegram là tài liệu triển khai hiện hành. Bộ mẫu AI gốc trong `skill-cau-hinh-folder-ai/` được giữ nguyên.
