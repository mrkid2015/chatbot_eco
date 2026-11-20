# Quy tắc MVP sâu bệnh Telegram

- Phạm vi và 5 ID lấy từ `CLAUDE.md`, discovery và kế hoạch Telegram. Không coi bộ mẫu web/bán hàng là yêu cầu hiện hành.
- Không thêm bước người duyệt trước khi trả lời. Trạng thái nguồn để đối chiếu, không tự đổi thành chứng nhận chuyên môn.
- Gemini trích ý định/fact; code validate JSON, chọn câu hỏi và đọc đáp án theo ID. Không để LLM tự viết lại phần kỹ thuật.
- Mẫu ngắn cố định theo ID; giữ đầy đủ đáp án gốc, section, nguồn và cảnh báo để mở rộng. Không icon; chuyển ký hiệu có/không/cần xác minh sang chữ có cùng ý nghĩa.
- Unknown không phải Không. Không kết luận vì còn một ứng viên sau khi giới hạn pilot; xử lý nguyên nhân ngoài phạm vi, mâu thuẫn và đồng nhiễm rõ ràng.
- Không chạy trực tiếp rules nguồn mâu thuẫn, nhất là `Q-XIMU-02`. Viết logic tường minh, có ca kiểm thử dương/âm/mơ hồ.
- Chào hỏi không xóa trạng thái chẩn đoán; reset mới xóa phiên. Xử lý tuần tự trong từng chat, cô lập nhiều người, chống xử lý update lặp.
- API lỗi vẫn có lệnh/nút local và fallback trung thực. Không bịa ID, thông tin doanh nghiệp, hoạt chất, liều, PHI/MRL.
- Staging có thể tái tạo; runtime phải tách file và cập nhật theo release/migration. Không dùng nhật ký chat làm kiến thức.
- Đề xuất môi trường nhẹ Windows/Python/SQLite; không tự cài Docker, Node hoặc DB server. Không tạo service nền hay đổi bot cũ ngoài yêu cầu.
- Không báo đã chạy bot, đo tốc độ hoặc kiểm tra API thật khi mới có dữ liệu và kế hoạch.
