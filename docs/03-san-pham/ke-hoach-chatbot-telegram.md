# Kế hoạch chatbot Telegram Eco Agro

Trạng thái: đã hỏi nhu cầu và làm sạch dữ liệu; chưa xây hoặc kết nối bot. Phạm vi căn cứ `docs/01-tong-quan/requirements-discovery.md`.

## 1. Kết quả cần đạt

Nhân viên thử trên Telegram, nói tiếng Việt tự nhiên về sầu riêng bị xì mủ, vàng lá hoặc thối trái. Bot chào hỏi, hỏi từng câu để phân biệt và trả lời ngắn theo ID, không icon. Phần dài tách thành tin nhắn có thứ tự; lưu đầy đủ mọi mục nguồn để bật/tắt hoặc xem tiếp sau này.

| ID | Hồ sơ trong bản thử |
|---|---|
| `SB-XIMU-PHYTO` | Xì mủ Phytophthora |
| `SB-XIMU-FUSA` | Xì mủ Fusarium kết hợp mọt |
| `SB-THOI-RE` | Thối rễ–vàng lá |
| `SB-THOI-TRAI` | Thối trái do nấm |
| `SB-SAU-DUC-TRAI` | Sâu đục trái |

Hồ sơ khác và sản phẩm vẫn được lưu để mở rộng, nhưng không tự gia nhập kết quả chẩn đoán của bộ thử. Messenger, chốt đơn, giá MISA và phân tích ảnh nằm ở giai đoạn sau. Ảnh gửi vào bản đầu được phản hồi là chưa hỗ trợ, đề nghị mô tả bằng chữ.

## 2. Phương án nhẹ trên Windows

Python 3.11+ (máy hiện có 3.12), SQLite đi kèm Python, Telegram qua long polling và Gemini qua API. Đề xuất dùng `python-telegram-bot` cho adapter Telegram và một HTTP client async tương thích cho Gemini. Chỉ chốt phiên bản package và model sau khi kiểm tra API khả dụng lúc build. Không chạy mô hình AI trên máy, không cần GPU.

Không cần Node.js, Docker, Redis, server PostgreSQL hay vector database cho 5 hồ sơ. Một tiến trình bot, file SQLite và file `.env`; thư viện nằm trong `.venv`. Long polling không cần domain, webhook hoặc mở port inbound. Máy phải bật, có mạng và không ngủ thì mới trả lời được.

GitHub dùng lưu code, theo dõi thay đổi và chạy kiểm tra tự động. GitHub Pages không chạy tiến trình Python bot; GitHub Actions dùng test/build, không chọn để giữ bot chạy 24/7. Khi ổn định, chuyển cùng code sang VPS nhỏ hoặc dịch vụ chạy worker có tiến trình liên tục; đo thực tế rồi mới chọn tài nguyên. Chưa tạo repo hoặc đăng dữ liệu nào lên GitHub.

## 3. Luồng hội thoại và vai trò Gemini

1. Xác thực người thử bằng allowlist Telegram user ID; chỉ nhận chat riêng giai đoạn đầu.
2. Xử lý `/start`, `/help`, `/reset`, chào/cảm ơn và nút bấm bằng local code khi đủ rõ, không gọi AI không cần thiết.
3. Với tin tự do, Gemini trả JSON giới hạn: `intent`, `crop`, `symptom_group`, `facts`, `clarification_needed`. Không trả một đoạn khuyến cáo kỹ thuật tự viết.
4. Code validate schema, kiểu dữ liệu, giá trị cho phép và phạm vi. Chỉ nhận fact có căn cứ trong lời người dùng; giá trị chưa quan sát là `unknown`.
5. Engine xác định câu hỏi tiếp theo theo fact/candidate, hỏi một ý mỗi lần, có Có/Không/Không rõ hoặc nút phù hợp ngữ nghĩa. Không hỏi lại câu đã trả lời trừ khi khách sửa thông tin.
6. Chỉ chọn ID khi đáp ứng tiêu chí bằng chứng đã mã hóa, không mâu thuẫn với cây/bộ phận/phạm vi và không còn trường hợp ngoài bộ thử chưa loại được. Không dùng “còn 1 ID” làm tiêu chí duy nhất.
7. Truy vấn SQLite bằng parameter theo ID, đọc `short_answer` và các section. Mẫu trả lời kỹ thuật được lưu cố định, Gemini không diễn đạt lại.
8. Nếu thiếu thông tin, ngoài phạm vi, có thể đồng nhiễm hoặc hết câu hỏi mà chưa phân biệt được, trả mẫu chưa đủ dữ kiện và đề nghị kỹ sư; không khẳng định đã chuyển người nếu chưa có tích hợp.

Chào hỏi/thông tin có thể do Gemini xử lý trong phạm vi dữ liệu FAQ; lời chào không làm mất phiên chẩn đoán. Yêu cầu đổi cây/đổi triệu chứng hoặc reset phải tạo trạng thái đúng. Gemini lỗi/timeout thì bot vẫn trả lời lệnh, nút bấm và luồng hỏi local; không fallback sang đoán bệnh.

## 4. Luồng kỹ thuật cho ba nhóm triệu chứng

Đây là thiết kế cần mã hóa và kiểm thử, không phải xác nhận chuyên môn mới. Lấy dấu hiệu từ nguồn, giữ khả năng chưa đủ dữ kiện.

- **Xì mủ:** xác nhận sầu riêng và vị trí; hỏi lỗ mọt nhỏ/mùn, lỗ đục to, vết ướt thâm lan rộng, dấu khô cành. Nhận diện dấu hiệu sâu đục thân/nấm hồng ngoài bộ thử để dừng kết luận. Nếu dấu mọt và vết loang ướt cùng xuất hiện, phản hồi khả năng phối hợp/chưa phân biệt thay vì chọn độc một ID. Không sao chép lỗi nhánh `Q-XIMU-02`.
- **Vàng lá:** xác nhận triệu chứng và quan sát rễ. “Chưa đào/chưa biết” là unknown; không tự suy ra rễ khỏe. Rễ thối đen/tuột vỏ/mùi hôi là bằng chứng cho hồ sơ thối rễ; các dấu u rễ, mối, vàng lá đơn thuần hoặc thiếu quan sát phải đi nhánh chưa đủ/phạm vi khác. Không chọn thối rễ chỉ vì nó là ID vàng lá duy nhất trong pilot.
- **Thối trái:** hỏi trái còn trên cây hay sau thu hoạch; sau thu hoạch thuộc hồ sơ khác nên ngoài pilot. Hỏi lỗ đục/phân sâu và dạng vết thối. Phân biệt sâu đục trái với thối do nấm theo dấu nguồn; nếu hai dấu hiệu cùng có hoặc quan sát không rõ thì không ép chọn. Không suy ra thối do nấm chỉ từ câu trả lời “không thấy sâu”.

Mỗi ID cần bảng `required_support`, `contradictions`, `unknown_fallback` và test ca dương/âm/mơ hồ, được phiên bản hóa cùng dữ liệu. Những điều kiện suy diễn mới phải được ghi rõ là logic thiết kế, không tự gán cho chuyên gia trong file nguồn.

## 5. Nội dung trả lời và cập nhật

- Tin đầu: mẫu ngắn cố định theo ID, nhận định tham khảo và dấu hiệu khớp. Không coi là chẩn đoán chắc chắn ngoài thực địa.
- Các mục: dấu hiệu, tác nhân, điều kiện/giai đoạn, canh tác, hoạt chất, PHI, sản phẩm hỗ trợ, khi cần kỹ sư, nguồn. Mọi mục đều được giữ trong database, không loại mất phần chưa bật.
- Renderer dùng bản không icon, đổi ký hiệu trạng thái thành chữ. Không làm rơi phần “chưa đăng ký”, “chưa có dữ liệu”, đơn vị hoặc điều kiện khi chia tin.
- Đề xuất mặc định gửi phần ngắn và phần canh tác/lưu ý; mục chi tiết qua nút xem tiếp. Có chế độ gửi tất cả theo thứ tự nếu muốn, cấu hình bằng section policy. Mỗi tin mục tiêu khoảng 600–900 ký tự, hard limit thấp hơn giới hạn Telegram hiện hành, không cắt từ hoặc escape HTML lỗi.
- Toàn bộ hoạt chất/MRL/PHI giữ nguyên căn cứ nguồn; không biến số MRL thành khuyến cáo liều dùng. Các mục có trạng thái thiếu/mâu thuẫn cần thể hiện đúng. Nguồn thay đổi thì import release mới và kiểm tra tự động, không cần bước người duyệt.

## 6. Thứ tự triển khai và đầu ra kiểm tra được

| Bước | Công việc | Điều kiện hoàn thành |
|---|---|---|
| 0 — đã làm | Khảo sát project, hỏi nhu cầu, làm sạch hai Excel, xuất SQLite staging | Nguồn không đổi, không mất dòng/ô, đủ 5 ID |
| 1 | Tạo package Python, config `.env.example`, migration SQLite runtime và importer | Một lệnh tạo DB; import lặp không trùng; staging không ghi đè phiên runtime |
| 2 | Viết engine local cho 3 nhóm, fact yes/no/unknown, tiêu chí nhận ID và fallback | Ca chuẩn trả đúng ID; ca mơ hồ/ngoài phạm vi không kết luận ép buộc; xử lý lỗi JSON nguồn rõ ràng |
| 3 | Tạo short templates theo ID, section delivery, FAQ chào hỏi và renderer chia tin | Không icon, không mất nội dung/đơn vị/lưu ý; thứ tự phần đúng |
| 4 | Thêm adapter Gemini, schema JSON, timeout và giới hạn gọi | Output sai schema/ID không hợp lệ không đổi trạng thái; câu hỏi local vẫn hoạt động khi API lỗi |
| 5 | Kết nối Telegram polling, allowlist, private chat, session, reset và outbox | Không lẫn hai người; update lặp không chạy lại nghiệp vụ; chỉ một poller cho một token |
| 6 | Test Windows, 5 người giả lập và thử Telegram thật khi có credential | Đo độ trễ, RAM, số gọi/token AI; không lỗi chẩn đoán kỳ vọng trong bộ ca; có bằng chứng lỗi/retry |
| 7 | Viết hướng dẫn start/stop, cập nhật/rollback dữ liệu và gỡ môi trường | Chạy trong `.venv`, Ctrl+C dừng; không thêm service tự khởi động; sao lưu/xóa có mục tiêu |

Không cần bot mới để làm bước 1–4. Khi đến bước 5, nếu bot cũ đang polling/webhook ở nơi khác, chọn bot thử mới hoặc điều phối dừng bản cũ để tránh xung đột. Không tự thay webhook hoặc dừng bot cũ khi chưa biết chủ sở hữu tiến trình.

## 7. Nghiệm thu tốc độ và tài nguyên

Các con số sau là **mục tiêu đề xuất để đo**, chưa phải kết quả đạt được:

- 5 phiên đồng thời, 30 lượt/phiên gồm chào, nút, hỏi tự do, thay đổi thông tin và ngoài phạm vi.
- p95 xử lý local dưới 0,5 giây, tính trong app, tách khỏi thời gian mạng Telegram.
- p95 lượt có Gemini dưới 5 giây trong điều kiện mạng và quota bình thường; hard timeout dự kiến 8 giây rồi phản hồi fallback. Tối đa một yêu cầu AI đang xử lý mỗi phiên; hạn chế retry ảnh hưởng tốc độ.
- Không gọi Gemini với `/start`, `/help`, `/reset` và nút trả lời hợp lệ. Báo số lần gọi, token/cost nếu provider trả số liệu.
- Đo RAM/CPU/đĩa khi idle và tải; không hứa mức RAM trước khi có runtime. Mục tiêu app nhỏ, không tải model/embeddings cục bộ.
- Kiểm tra không gửi sai ID ở toàn bộ ca xác định; ca mơ hồ/ngoài pilot phải trả chưa đủ, tách phiên chính xác. Kết quả benchmark không thay cho độ đúng kỹ thuật.

## 8. Những phần chưa thực hiện

Chưa có code bot, token/API cấu hình, model đã chọn, engine runtime, migration, benchmark hoặc tin nhắn gửi thật. Chưa tạo Git repo/đăng GitHub. Tất cả lệnh bot sau này chỉ được ghi là chạy được sau khi triển khai và kiểm tra.
