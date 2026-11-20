# Eco Agro — chatbot Telegram nội bộ

Đã làm rõ nhu cầu, làm sạch hai Excel và chuẩn bị kế hoạch. Chưa có bot runtime hoặc kết nối Gemini/Telegram thật.

MVP: sầu riêng, 5 hồ sơ thuộc xì mủ/vàng lá/thối trái. Gemini hiểu hội thoại; đáp án kỹ thuật lấy mẫu cố định theo ID, không icon, chia mục/tin ngắn. Không thêm cổng duyệt trước trả lời.

## Đọc để bắt đầu

- [Kế hoạch triển khai](docs/03-san-pham/ke-hoach-chatbot-telegram.md)
- [Câu hỏi và câu trả lời đã ghi nhận](docs/01-tong-quan/requirements-discovery.md)
- [Báo cáo làm sạch dữ liệu](docs/02-ky-thuat/data-cleaning-report.md)
- [Kiến trúc Python + SQLite + Gemini](docs/02-ky-thuat/architecture.md)
- [Database và cập nhật lâu dài](docs/02-ky-thuat/data-model.md)
- [Windows, GitHub và cách gỡ](docs/04-van-hanh/windows-local.md)

## Dữ liệu đã tạo

Trong `data/cleaned/`: hai workbook `.cleaned.xlsx`, `eco_agro.sqlite`, bản ghi JSONL, danh sách vấn đề CSV/JSON, manifest và bản xem trước tin nhắn 5 ID. File gốc không đổi. `data/private/audit/` lưu đối chiếu nguồn, gồm nhật ký chat không đưa vào kiến thức bot. Các thư mục này và workbook gốc đã được thêm vào `.gitignore`.

## Công cụ dữ liệu

Yêu cầu Python 3.11+, máy này đã có `.venv` với thư viện Excel. Nếu tạo môi trường mới:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-data.txt
```

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/clean-eco-data.py
.\.venv\Scripts\python.exe -X utf8 scripts/verify-cleaned-data.py
```

Lệnh clean tái tạo staging, không phải cơ chế sửa dữ liệu runtime lâu dài. Không có lệnh chạy bot cho đến khi code được triển khai.

## Cấu hình AI

Giữ bản gốc trong `CLAUDE.md` và `.claude/`, đồng bộ sang `AGENTS.md`, `.agents/` và `.codex/agents/`:

```powershell
python -X utf8 scripts/sync-ai-config.py
python -X utf8 scripts/verify-ai-config.py
```

Mở phiên AI mới sau khi cập nhật skills/agents. Bộ mẫu gốc trong `skill-cau-hinh-folder-ai/` giữ nguyên; các tài liệu mẫu bán hàng trong `docs/05-mau/` dành cho giai đoạn sau, không phải điều kiện chặn MVP Telegram.
