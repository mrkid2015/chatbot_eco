# Cau hinh AI: Claude Code, Codex, Antigravity

Moi cong cu AI chi doc file **dung ten, dung cho** cua no. Du an nay giu **1 ban goc**
la `.claude/`, roi dung script sinh ban cho Codex va Antigravity.

## 1. So do thu muc

```
Eco Agro - Chatbot tư vấn bán hàng/
|-- CLAUDE.md                 Claude Code doc
|-- AGENTS.md                 Codex + Antigravity doc
|-- .claude/                  BAN GOC - chi sua o day
|     |-- skills/  commands/  rules/  agents/
|     |-- plans/   references/  (tai lieu tra cuu, khong sinh ban sao)
|     |-- hooks/   policies/  settings.json
|-- .agents/                  TU SINH - khong sua tay
|     |-- skills/             Codex + Antigravity
|     |-- rules/              Antigravity
|-- .codex/
|     |-- config.toml         cau hinh Codex cho du an (viet tay)
|     |-- agents/             TU SINH tu .claude/agents/
`-- scripts/sync-ai-config.py script dong bo
```

## 2. Moi cong cu doc gi

| Loai | Claude Code | Codex | Antigravity |
|---|---|---|---|
| Huong dan chung | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| Skills | `.claude/skills/` | `.agents/skills/` | `.agents/skills/` |
| Lenh `/` | `.claude/commands/` | da bo, dung skill | da bo, dung skill |
| Agent con | `.claude/agents/*.md` | `.codex/agents/*.toml` | khong co |
| Cau hinh | `.claude/settings.json` | `.codex/config.toml` | qua giao dien |

## 3. Script doi gi

| Ban goc | Sinh ra | Ghi chu |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | copy kem dong GENERATED |
| `.claude/skills/<x>/` | `.agents/skills/<x>/` | copy nguyen |
| `.claude/commands/a/b.md` | `.agents/skills/a-b/SKILL.md` | lenh thanh skill |
| `.claude/rules/a/b.md` | `.agents/rules/a-b.md` | them `trigger:` |
| `.claude/agents/<ten>.md` | `.codex/agents/<ten>.toml` | name, description, developer_instructions |

Chay dong bo: `python scripts/sync-ai-config.py`
Sua xong phai mo phien AI moi thi agent va skill moi duoc nap.

## 4. Áp dụng cho Eco Agro

- Nguồn gốc: `CLAUDE.md` và `.claude/`. Chỉ sửa các bản này rồi đồng bộ.
- Ba skills nghiệp vụ: `eco-agro-diagnostics` cho MVP, `eco-agro-knowledge` cho dữ liệu, `eco-agro-sales` cho mở rộng; lệnh `kiem-tra` chuyển thành skill cho công cụ dùng `.agents/skills/`.
- Bốn rules: cấu trúc code, MVP chẩn đoán, tư vấn bán hàng và bảo vệ dữ liệu. `CLAUDE.md`/`AGENTS.md` yêu cầu đọc trực tiếp rules để không phụ thuộc vào khả năng tự nạp của từng công cụ.
- Ngữ cảnh tổng hợp ở `.claude/references/project-context.json`; file này không phải runtime config. Nhu cầu đã trao đổi ở `docs/01-tong-quan/requirements-discovery.md`, kế hoạch ở `docs/03-san-pham/ke-hoach-chatbot-telegram.md`. AI đọc tham chiếu tại chỗ, không tạo bản sao để tránh lệch phiên bản.
- Sáu vai trò: project-manager, ui-ux-designer, software-engineer, qa-test-engineer, devops-engineer, sre-ops-engineer. Đây là định nghĩa vai trò, không tự khởi chạy nhiều agent.
- Python 3.11+; dùng `python -X utf8 scripts/sync-ai-config.py` và `python -X utf8 scripts/verify-ai-config.py` để tránh lỗi encoding trên Windows.
- Script sync dựng lại `.agents/skills/`, `.agents/rules/`, `.codex/agents/`; không lưu nội dung viết tay tại đó. `AGENTS.md` viết tay không có dấu GENERATED sẽ được giữ nguyên.

Ma trận phía trên phản ánh quy ước của bộ mẫu được cung cấp. Khả năng nhận agents, skills và rules phụ thuộc công cụ/phiên bản đang dùng; tệp TOML parse được chưa chứng minh công cụ hỗ trợ toàn bộ tính năng. Bộ cấu hình này không tự cài plugin hoặc MCP, không thay đổi quyền thực thi và không thêm cấu hình OpenCode riêng.

Nếu công cụ không tự đọc hướng dẫn, yêu cầu nó đọc `AGENTS.md` hoặc `CLAUDE.md`. Khi thêm skills/agents, mở phiên AI mới để công cụ có cơ hội nạp cấu hình mới.
