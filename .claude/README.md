# Bản gốc cấu hình AI Eco Agro

Nguồn chung là `CLAUDE.md` và `.claude/`. Ngữ cảnh tập trung tại `references/project-context.json`, diễn giải tại `references/eco-agro-context.md`; nhu cầu gốc và kế hoạch nằm trong `docs/` theo các liên kết ở CLAUDE.md.

MVP hiện hành: Telegram nội bộ, Gemini, sầu riêng, 5 ID, mẫu kỹ thuật cố định không icon, dữ liệu đầy đủ theo section, không người duyệt trước trả lời. `eco-agro-diagnostics` là skill chính; `eco-agro-knowledge` dùng dữ liệu, `eco-agro-sales` cho giai đoạn sau.

Sau khi sửa bản gốc, chạy `python -X utf8 scripts/sync-ai-config.py` rồi `python -X utf8 scripts/verify-ai-config.py`. Không sửa tay bản sinh trong `.agents/`, `.codex/agents/` và `AGENTS.md`. Tham chiếu JSON là ngữ cảnh cho AI lập trình, không phải cấu hình executable hay nơi đặt API key.
