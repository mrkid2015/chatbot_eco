# Chạy thử Windows, GitHub và gỡ tài nguyên

## Những gì hiện đã cài

Tạo `.venv` tại `D:\Vibecode\Chatbot\.venv`, cài `openpyxl==3.1.5` và phụ thuộc `et-xmlfile` để đọc/ghi Excel. Dùng Python 3.12 vốn có trên máy; không cài Python mới, Docker, Node.js, database server hay service nền.

Đã đo tại thời điểm chuẩn bị: `.venv` khoảng 13,39 MiB dữ liệu file; `data/cleaned/` 1,53 MiB; audit 0,53 MiB. Đây là dung lượng file, không phải RAM runtime; dung lượng trên đĩa thực tế và pip cache có thể lớn hơn. Chưa có tiến trình bot hoặc số đo RAM/CPU cho ứng dụng.

## Khi build bot

Tiếp tục dùng môi trường riêng trong dự án. Chỉ cài thư viện Telegram/HTTP cần thiết và ghi phiên bản vào manifest runtime riêng. SQLite không cần cài dịch vụ. Gemini qua Internet nên không tải mô hình lớn hoặc cần GPU.

Đề xuất chạy long polling trong cửa sổ PowerShell, Ctrl+C dừng. Không tạo service, tác vụ tự khởi động hoặc mở port inbound mặc định. Máy ngủ/tắt, mất mạng hoặc đóng tiến trình sẽ làm bot ngừng phản hồi. Chỉ một poller cho một token; bot cũ có webhook/poller thì cần kiểm tra trước, không tự xóa webhook của bot đang dùng.

Chưa có code bot nên chưa có lệnh start hợp lệ. Credential chỉ nhập cục bộ khi kết nối: `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, `GEMINI_MODEL`, danh sách user ID thử, cùng cấu hình bàn giao kỹ sư khi bật handoff (`ENGINEER_GROUP_CHAT_ID`, `SUPPORT_HOURS`). Không dán khóa hoặc ID nhóm nội bộ vào tài liệu/chat/GitHub.

## Gỡ dễ dàng

Không cần gỡ Python của hệ thống. Sau khi dừng các script bằng Ctrl+C, có thể xóa **riêng thư mục `.venv`** bằng File Explorer để bỏ toàn bộ thư viện đã cài cho dự án. Xóa môi trường không xóa code hoặc dữ liệu. Nếu muốn giữ kết quả, sao lưu file Excel sạch/DB trước khi xóa riêng `data/cleaned/` hoặc audit. Không xóa file gốc trừ khi bạn chủ động muốn bỏ chúng.

Pip có thể lưu cache chung bên ngoài dự án; không tự dọn cache chung vì ứng dụng khác có thể đang dùng. Sau này nếu chạy VPS, dừng/xóa máy chủ hoặc dịch vụ bên nhà cung cấp mới ngừng chi phí hạ tầng; việc xóa `.venv` trên Windows không tác động VPS.

## GitHub dùng để làm gì

Lưu code và kế hoạch, theo dõi thay đổi, kiểm thử qua CI. Các file nguồn có chat log/nội dung nội bộ và bản xuất được `.gitignore` chặn để khỏi vô tình đẩy lên. Chưa khởi tạo repo hoặc upload gì trong phiên này.

GitHub Pages không chạy bot Python liên tục. Actions phù hợp test/build, không dùng giữ long polling chạy thường trực. Muốn 24/7 sau giai đoạn thử, dùng VPS nhỏ hoặc dịch vụ worker rồi đo tài nguyên thực tế trước khi chọn gói. Nên repo private cho code nội bộ, nhưng secrets vẫn không được commit vào repo private.
