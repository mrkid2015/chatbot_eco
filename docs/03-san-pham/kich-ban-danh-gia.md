# Bộ kiểm tra MVP Telegram cần xây khi build

Hiện chỉ có kiểm tra dữ liệu; các ca hội thoại dưới đây chưa chạy vì chưa có bot. Không yêu cầu bước duyệt. Mục tiêu là đúng truy vấn/mẫu theo ID và xử lý không đủ dữ kiện.

| Nhóm | Ca bắt buộc |
|---|---|
| 5 ID | Mỗi ID có ca đủ dấu hiệu, thiếu dấu hiệu, phủ định, mâu thuẫn; đủ bằng chứng mới trả ID tương ứng |
| Ngoài pilot | Dấu nấm hồng/sâu đục thân, u rễ/mối, trái sau thu hoạch: không ép chọn bệnh trong pilot |
| Đồng nhiễm | Lỗ mọt cùng vết ướt lan: không khẳng định chỉ Fusarium hoặc chỉ Phytophthora |
| Unknown | Chưa đào rễ/không rõ/không quan sát được không bị đổi thành Không |
| Ngôn ngữ | Có dấu/không dấu, viết tắt, nhiều ý một câu, tự sửa thông tin |
| Điều phối | Chào/cảm ơn không reset; `/reset` xóa fact phiên; đổi triệu chứng không giữ fact sai ngữ cảnh |
| Gemini | JSON sai schema, fact không căn cứ, ID ngoài whitelist, timeout, quota: không đoán hoặc ghi trạng thái hỏng |
| Truy vấn | Parameterized SQL, ID hợp lệ trong đúng release, không lấy bệnh của cây khác |
| Nội dung | Short template cố định; không icon; giữ phủ định/cảnh báo/đơn vị khi split; đầy đủ section có thể bật/tắt |
| Telegram | Callback hợp lệ/cũ, update lặp, chat trái phép/nhóm bị từ chối, retry lỗi và giới hạn tốc độ |
| Phiên | 5 người đồng thời không lẫn trạng thái; tin đến nhanh trong một chat được tuần tự hóa |
| Cập nhật | Import dry-run/diff, rollback release, không mất session/runtime khi tái tạo staging |
| Bảo mật | Không log token/PII; prompt injection không mở quyền; không dùng NHAT_KY_CHAT làm kiến thức |
| Thông tin | Chỉ trả FAQ có nguồn; chưa có hotline/giá không tự bịa |
| Tốc độ | Đo local, AI và mạng riêng; p95, số API call, token, RAM/CPU/đĩa theo mục tiêu trong kế hoạch |

Lưu mã ca, dữ liệu/release, đầu vào, kỳ vọng, ID/fact/thông điệp thực tế, thời gian và kết quả. Mock API để kiểm thử core offline; Telegram/Gemini thật chỉ kiểm tra khi có cấu hình và quyền chạy thử. Không lấy độ chính xác phân loại trong bộ test làm cam kết chẩn đoán thực địa.
