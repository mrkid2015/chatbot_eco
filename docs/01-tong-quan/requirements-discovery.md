# Câu hỏi và nhu cầu đã trao đổi

Nội dung ghi nhận từ trao đổi ngày 20/11/2026. Đây là cơ sở thay cho giả định web chat/bán hàng ở bộ mẫu ban đầu.

| Câu hỏi | Câu trả lời của chủ dự án |
|---|---|
| Ai dùng đầu tiên, kênh nào? | Nhân viên dùng Telegram trước; Messenger cho khách có thể làm sau |
| Ưu tiên gì? | Ổn định, nhanh, hỏi đáp sâu bệnh đúng kỹ thuật; chỉ cần 3–5 hồ sơ |
| Có hội thoại thông thường không? | Có chào hỏi, hỏi đáp thông tin và API AI tham gia trả lời |
| Cây trồng nào? | Sầu riêng |
| Nhóm triệu chứng nào? | Xì mủ, vàng lá và thối trái |
| 5 hồ sơ cụ thể? | Đã chọn Phytophthora xì mủ, Fusarium–mọt xì mủ, thối rễ–vàng lá, thối trái do nấm, sâu đục trái |
| AI tự viết đáp án kỹ thuật không? | Không. Mẫu ngắn cố định theo ID, không icon; dài thì chia nhiều tin |
| Có giữ toàn bộ thông tin không? | Có. Chia đầy đủ các mục trong file, có thể bật/tắt dùng sau, hỗ trợ cập nhật lâu dài |
| Có cần bước duyệt trước khi trả lời không? | Không. Không thêm quyền duyệt hay chờ người duyệt cho bộ thử |
| Có thể thiết kế lại database không? | Có, cần chuẩn hóa để tối ưu và mở rộng |
| API AI nào? | Gemini |
| Có bot cũ không? | Có bot Telegram, chưa cung cấp code; có thể tạo bot mới nếu cần |
| Chạy đâu? | Thử Windows trước, nhờ đề xuất phương án nhẹ và dễ gỡ |
| Có thể dùng GitHub không? | Muốn biết cách dùng GitHub; chưa yêu cầu tạo repo hoặc đăng tải |
| Có học từ lịch sử trò chuyện không? | Có — học từ lịch sử trước đó để tự tối ưu giao tiếp/chào hỏi và cách hiểu câu hỏi, nhưng tuyệt đối không tự học hay tự sửa phần kiến thức kỹ thuật sâu bệnh |
| Khi bot không trả lời được thì sao? | Chuyển cuộc trò chuyện cho kỹ sư thật (kèm tóm tắt ca, chỉ báo thành công khi gửi thật tới nhóm/kênh kỹ sư) |

## Những câu chỉ cần chốt khi kết nối/chạy thật

1. Dùng bot Telegram hiện có hay bot thử mới? Token nhập vào `.env` cục bộ, không dán vào chat hoặc GitHub.
2. Gemini project/API key đã có chưa? Chọn model đang khả dụng trong tài khoản tại thời điểm triển khai; chưa ghi cứng tên model.
3. Telegram user ID nào được thử nội bộ? Mặc định đề xuất chat riêng, danh sách cho phép và không mở cho công chúng.
4. Ngân sách API/tháng và số người dùng đồng thời? Tạm đề xuất kiểm tra 5 người; đây chưa phải con số chủ dự án cam kết.
5. Có tài liệu thông tin Eco Agro nào ngoài 2 Excel? Nếu chưa có, bot chỉ trả lời phạm vi hệ thống, không bịa số hotline/giờ làm việc.
6. Kênh nhận bàn giao kỹ sư trên Telegram: `ENGINEER_GROUP_CHAT_ID` (khuyến nghị dùng Group bật chế độ Forum/Topics), danh sách kỹ sư trực và khung giờ trực (`SUPPORT_HOURS`).

Các điểm này không cản việc làm sạch, thiết kế database hoặc lập kế hoạch. Chỉ cần credential và cấu hình nhóm kỹ sư khi kiểm tra API/Telegram thật.
