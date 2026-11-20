# Database: dữ liệu đã xuất và thiết kế nâng cấp

## Kho chuẩn hóa hiện có

SQLite là một file, dùng `sqlite3` có sẵn trong Python. `data/cleaned/eco_agro.sqlite` là dữ liệu staging có thể tái tạo từ Excel.

| Bảng | Vai trò |
|---|---|
| `sources` | Tên và SHA-256 của hai file nguồn |
| `diseases` | ID, cây, tên, chất lượng nguồn, trạng thái nguồn, đáp án nguyên bản, tọa độ nguồn |
| `answer_sections` | Mục nội dung riêng, thứ tự, bản gốc và bản hiển thị không icon |
| `symptom_groups`, `group_candidates` | Nhóm triệu chứng và liên kết nhiều–nhiều đến hồ sơ |
| `questions` | Câu phân biệt và JSON nguồn; hiện gắn `source_unresolved`, chưa dùng như logic runtime |
| `pilot_members` | 5 ID chủ dự án đã chọn |
| `products` | 26 sản phẩm, quy cách, mã đăng ký kiểu TEXT, trường nguồn |
| `combos`, `combo_components` | Combo và thành phần; giữ liên kết chưa khớp là NULL |
| `faqs` | Câu hỏi sản phẩm, chưa tự tạo đáp án |

`fields_json` chỉ giữ phần thuộc tính nguồn chưa tách, không thay cho cột ID/khóa ngoại dùng truy vấn chính. SQLite đã bật kiểm tra khóa ngoại khi ghi; migration/runtime phải bật lại trên mỗi connection. Không có bảng nhật ký khách trong database staging.

## Schema runtime cần triển khai

Giữ staging và runtime tách file. Runtime dự kiến ở `data/runtime/bot.sqlite`, không bị script làm sạch ghi đè.

- `schema_migrations(version, applied_at)`: theo dõi migration, sao lưu trước thay đổi.
- `knowledge_releases(id, source_hash, created_at)`: phiên bản nhập liệu, một đợt cập nhật là một transaction.
- `disease_versions(disease_id, release_id, ...)` và `answer_section_versions(...)`: giữ lịch sử, `short_answer` cố định theo ID, đầy đủ nội dung gốc và display.
- `section_delivery_policy(section_key, enabled, delivery_mode, order_index)`: bật/tắt và cách gửi, có thể dùng hoạt chất/PHI/nguồn khi cần mà không mất nội dung. Không dùng làm bước chờ duyệt.
- `diagnostic_questions`, `response_options`, `rules`, `rule_conditions`, `rule_effects`: cấu trúc hóa fact, yes/no/unknown, nhánh và tác động; không chạy trực tiếp câu văn hoặc JSON mâu thuẫn từ Excel.
- `sessions(id, user_id, chat_id, mode, release_id, ttl_at, ...)`, `session_facts`, `asked_questions`: từng người/chat có trạng thái riêng, có `mode` (`BOT_ACTIVE`, `WAITING_ENGINEER`, `HUMAN_HANDOFF`), TTL và reset.
- `conversation_turns(id, session_id, user_id, role, text, intent, latency_ms, fallback_reason, created_at)`: lịch sử hội thoại ngắn hạn theo từng phiên (cô lập theo `user_id`, có TTL) để giao tiếp/chào hỏi tự nhiên và làm nguồn đầu vào đã che PII cho tối ưu giao tiếp offline; tách biệt hoàn toàn với bảng kiến thức sâu bệnh.
- `user_preferences(user_id, preferred_salutation, style_note, updated_at)` và `feedback_events(id, turn_id, user_id, rating, reason, created_at)`: lưu nhẹ thói quen xưng hô theo từng người và phản hồi hữu ích/chưa đúng ý.
- `communication_examples(id, style_release_id, scenario, user_utterance, good_reply, score, active)` và `utterance_aliases(id, style_release_id, phrase, normalized_target, target_type, active)`: kho ví dụ chào hỏi/làm rõ/chuyển ý và từ đồng nghĩa/viết tắt nhà vườn hay dùng, được phiên bản hóa và kiểm tra guardrail tự động (không chứa hoạt chất/liều/PHI/MRL, không icon, chống prompt injection), rollback được theo `style_release_id`.
- `handoff_tickets(ticket_id, session_id, user_id, status, reason, summary_json, engineer_group_chat_id, topic_id, assigned_engineer_id, idempotency_key, created_at, closed_at)` và `handoff_messages(id, ticket_id, sender_role, text, telegram_message_id, created_at)`: quản lý hồ sơ chuyển kỹ sư thật, chống tạo trùng ticket khi bấm nhiều lần và lưu vết chuyển tiếp 2 chiều (Phase 1.5).
- `processed_updates`, `outbox`: tránh xử lý update Telegram lặp và gửi tiếp phần còn thiếu sau lỗi; không hứa exactly-once ở phía Telegram khi timeout chưa biết đã gửi hay chưa.
- `information_faqs`: chào hỏi/phạm vi bot và thông tin doanh nghiệp có nguồn; tách khỏi bệnh và lịch sử trò chuyện.

Tất cả ID hồ sơ giữ nguyên để liên kết từ file và code cũ. Bật/tắt một hồ sơ là cấu hình phạm vi, không xóa dữ liệu cũ. Thêm cây/bệnh mới không cần đổi logic Telegram. Cần validate liên kết, luồng và nội dung trước khi chuyển phiên bản dữ liệu, tự động bằng script/test, không thêm luồng người duyệt.

## Quy tắc cập nhật lâu dài

Excel là nguồn nhập ban đầu; sau build, dữ liệu chỉnh sửa theo định dạng import/version được chỉ rõ. Không duy trì hai nơi có quyền ghi độc lập. Import có dry-run, diff theo ID, giữ nguyên phiên bản trước; thay dữ liệu trong transaction, phiên đang chạy gắn với release để tránh đổi đáp án giữa lượt. Rollback bằng đổi release đang dùng. Bộ thử chỉ tải 5 ID vào phạm vi trả lời, giữ ứng viên ngoài phạm vi làm dấu chặn kết luận ép buộc.
