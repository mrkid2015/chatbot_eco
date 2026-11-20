---
description: Kiểm tra cấu hình và mức sẵn sàng của dự án chatbot Eco Agro
---

Đọc `CLAUDE.md`, `docs/01-tong-quan/project-brief.md` và `docs/02-ky-thuat/architecture.md`.

1. Chạy `python -X utf8 scripts/verify-ai-config.py`; nếu bản sinh lệch, sửa bản gốc rồi đồng bộ.
2. Đọc discovery/kế hoạch Telegram; kiểm tra 5 ID, bản sạch và SQLite staging bằng `.\.venv\Scripts\python.exe -X utf8 scripts/verify-cleaned-data.py`. Không yêu cầu bước người duyệt hoặc catalog bán hàng để chặn MVP sâu bệnh.
3. Nếu đã có code, tìm lệnh thực tế trong manifest/README rồi chạy kiểm tra phù hợp. Không tự báo đã test ứng dụng khi chưa có code.
4. Báo kết quả: cấu hình hợp lệ hay lỗi, thông tin còn thiếu, bước tiếp theo có thể thực hiện.
