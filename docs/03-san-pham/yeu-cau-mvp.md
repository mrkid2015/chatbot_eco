# Yêu cầu MVP Telegram nội bộ

Theo nhu cầu đã ghi trong `docs/01-tong-quan/requirements-discovery.md`; chi tiết triển khai ở `ke-hoach-chatbot-telegram.md`.

- Nhân viên chat riêng với Telegram bot; giới hạn người thử, chạy trên Windows trước.
- Hỗ trợ sầu riêng, 5 ID: `SB-XIMU-PHYTO`, `SB-XIMU-FUSA`, `SB-THOI-RE`, `SB-THOI-TRAI`, `SB-SAU-DUC-TRAI`.
- Chào hỏi, trợ giúp, hỏi thông tin phạm vi bot, reset và tiếp tục hội thoại tự nhiên.
- Gemini hiểu tin tự do thành JSON, engine chọn câu hỏi/kiểm tra bằng chứng. Nội dung trả lời kỹ thuật lấy mẫu cố định theo ID, không tự viết lại.
- Mẫu ngắn, không icon; chia dài theo từng mục/tin. Giữ đầy đủ tất cả thông tin nguồn và cấu hình mục có thể dùng/không dùng về sau.
- Không yêu cầu quyền duyệt trước trả lời. Không mở toàn bộ 143 hồ sơ vào pilot chỉ vì đã nhập database.
- Chưa đủ dữ kiện/ngoài phạm vi/đồng nhiễm có phản hồi riêng, không chọn ép một ID.
- Không bịa giá, tồn kho, liều, PHI, MRL hay thông tin doanh nghiệp. Nguồn sản phẩm ghi giá từ MISA nhưng chưa tích hợp MISA trong MVP.
- Tách phiên, không xử lý update lặp, timeout AI có fallback và không làm mất ngữ cảnh.

Messenger, bán hàng, lead/đặt hàng, ảnh và vận hành 24/7 là giai đoạn sau. Chưa có ứng dụng chạy được; kiểm tra dữ liệu không được báo thành kiểm thử bot.
