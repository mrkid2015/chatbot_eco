# Cau hinh AI: Claude Code, Codex, Antigravity

Moi cong cu AI chi doc file **dung ten, dung cho** cua no. Du an nay giu **1 ban goc**
la `.claude/`, roi dung script sinh ban cho Codex va Antigravity.

## 1. So do thu muc

```
du-an-mau/
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
