#!/usr/bin/env python3
"""Tao cau hinh folder AI chuan 1-lan-dung-3-cong-cu cho 1 du an moi.

Cau truc sinh ra (giong clip TikTok @code.web.khng.kh, du an trello-clone):

  <du-an>/
  |-- CLAUDE.md            Claude Code doc
  |-- AGENTS.md            Codex + Antigravity doc (script dong bo tu sinh)
  |-- .claude/             BAN GOC - chi sua o day
  |     |-- skills/  commands/  rules/  agents/
  |     |-- hooks/   policies/  plans/  references/  settings.json  README.md
  |-- .agents/             TU SINH - khong sua tay (Codex + Antigravity)
  |     |-- skills/  rules/
  |-- .codex/
  |     |-- config.toml    cau hinh Codex cho du an (viet tay)
  |     |-- agents/        TU SINH tu .claude/agents/
  |-- docs/  01-tong-quan 02-ky-thuat 03-san-pham 04-van-hanh
  |          05-mau 06-design 99-ghi-chu handoff
  `-- scripts/sync-ai-config.py   script dong bo

Cach chay:
  python scaffold_ai_folder.py <thu-muc-du-an> [--ten "Ten du an"] [--force]
Mac dinh khong ghi de file da ton tai. Chi dung thu vien chuan Python 3.
"""

import argparse
import shutil
import sys
from pathlib import Path

AGENTS_STARTER = {
    "project-manager": (
        "Len ke hoach, viet spec va user story, chia sprint",
        "Ban la Project Manager. Tong hop van de tu nguon that, viet proto-spec va spec, "
        "chia viec thanh sprint co tieu chi nghiem thu ro rang. Khong tu viet code.",
    ),
    "ui-ux-designer": (
        "Thiet ke luong, wireframe, accessibility",
        "Ban la UI UX Designer. Thiet ke luong nguoi dung va wireframe truoc khi code, "
        "kiem tra accessibility va nhat quan design token cua du an.",
    ),
    "software-engineer": (
        "Code theo spec, sua bug co pham vi ro",
        "Ban la Software Engineer. Chi code theo spec da duyet, sua bug trong pham vi duoc giao, "
        "chay test lien quan truoc khi bao xong.",
    ),
    "qa-test-engineer": (
        "Viet va chay test, ra verdict SHIP hoac BLOCK",
        "Ban la QA Test Engineer. Viet va chay test, eval lien tuc, tu sua loi nho trong test, "
        "ket luan ro SHIP hoac BLOCK kem bang chung.",
    ),
    "devops-engineer": (
        "CI CD, deploy, rollback",
        "Ban la DevOps Engineer. Dung CI CD, deploy theo tag da review, luon co ke hoach rollback "
        "truoc khi deploy.",
    ),
    "sre-ops-engineer": (
        "Giam sat, xu ly su co, backup",
        "Ban la SRE Ops Engineer. Giam sat he thong, xu ly su co theo runbook, kiem tra backup "
        "dinh ky va ghi lai intent xu ly su co.",
    ),
}


def claude_md(ten):
    return f"""# {ten} - Huong dan cho AI

> Moi cong cu AI chi doc file dung ten, dung cho cua no. Du an nay giu 1 ban goc la
> `.claude/`, roi dung script sinh ban cho Codex va Antigravity.
> Chi sua ban goc, khong bao gio sua tay cac file tu sinh.

## Tong quan du an

- Muc tieu: [dien muc tieu du an]
- Stack: [dien cong nghe]
- Lenh chay: [dien lenh chay du an]
- Lenh test: [dien lenh chay test]

## Quy tac lam viec

- Doc `docs/02-ky-thuat/architecture.md` truoc khi sua code lon.
- Skill trong `.claude/skills/` tu kich hoat khi mo ta khop viec, go ten skill de ep dung.
- Lenh `/` nam trong `.claude/commands/`, agent con nam trong `.claude/agents/`.
- Sua xong cau hinh AI thi chay `python scripts/sync-ai-config.py` de dong bo.
- Tai lieu tra cuu nam trong `.claude/references/` va `docs/`, khong sinh ban sao.

## So do thu muc

Xem `docs/02-ky-thuat/ai-tool-config.md`.
"""


def ai_tool_config_md(ten):
    return f"""# Cau hinh AI: Claude Code, Codex, Antigravity

Moi cong cu AI chi doc file **dung ten, dung cho** cua no. Du an nay giu **1 ban goc**
la `.claude/`, roi dung script sinh ban cho Codex va Antigravity.

## 1. So do thu muc

```
{ten}/
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
"""


def write(path, content, force, report):
    if path.exists() and not force:
        report.append(f"bo qua (da co): {path.relative_to(path.parents[0]) if False else path.name} - {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    report.append(f"tao: {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--ten", default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    root = Path(args.target).resolve()
    ten = args.ten or root.name
    root.mkdir(parents=True, exist_ok=True)
    report = []

    for d in [
        ".claude/skills", ".claude/commands", ".claude/rules", ".claude/agents",
        ".claude/hooks", ".claude/policies", ".claude/plans", ".claude/references",
        ".agents/skills", ".agents/rules", ".codex/agents", "scripts",
        "docs/01-tong-quan", "docs/02-ky-thuat", "docs/03-san-pham",
        "docs/04-van-hanh", "docs/05-mau", "docs/06-design",
        "docs/99-ghi-chu", "docs/handoff",
    ]:
        (root / d).mkdir(parents=True, exist_ok=True)

    write(root / "CLAUDE.md", claude_md(ten), args.force, report)
    write(root / ".claude/README.md",
          "# Ban goc cau hinh AI\n\nChi sua cau hinh AI o thu muc nay. "
          "Sua xong chay `python scripts/sync-ai-config.py` o thu muc goc du an.\n",
          args.force, report)
    write(root / ".claude/settings.json", "{}\n", args.force, report)
    write(root / ".codex/config.toml",
          "# Cau hinh Codex cho du an - file nay viet tay, script khong ghi de.\n"
          "# Vi du:\n# model = \"gpt-5-codex\"\n# approval_policy = \"on-request\"\n",
          args.force, report)
    write(root / "docs/02-ky-thuat/ai-tool-config.md", ai_tool_config_md(ten), args.force, report)

    write(root / ".claude/skills/vi-du-skill/SKILL.md",
          "---\nname: vi-du-skill\ndescription: Skill mau - tu kich hoat khi mo ta khop viec, "
          "hoac go ten skill de ep dung. Thay bang skill that cua du an.\n---\n\n"
          "# Skill mau\n\n- Buoc 1: [dien buoc lam]\n- Buoc 2: [dien buoc kiem tra]\n",
          args.force, report)
    write(root / ".claude/commands/kiem-tra.md",
          "---\ndescription: Kiem tra nhanh trang thai du an truoc khi lam viec\n---\n\n"
          "Doc CLAUDE.md va docs/02-ky-thuat/ai-tool-config.md, liet ke skill, lenh va agent dang co.\n",
          args.force, report)
    write(root / ".claude/rules/code-folder-structure.md",
          "# Cau truc folder code\n\n- [dien quy tac dat file code cua du an vao day]\n",
          args.force, report)

    for name, (desc, body) in AGENTS_STARTER.items():
        write(root / f".claude/agents/{name}.md",
              f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}\n",
              args.force, report)

    sync_src = Path(__file__).resolve().parent / "sync-ai-config.py"
    sync_dst = root / "scripts/sync-ai-config.py"
    if sync_dst.exists() and not args.force:
        report.append(f"bo qua (da co): {sync_dst}")
    else:
        shutil.copyfile(sync_src, sync_dst)
        report.append(f"tao: {sync_dst}")

    print(f"Da tao cau hinh folder AI cho du an '{ten}' tai {root}")
    for line in report:
        print(" -", line)
    print("Buoc tiep theo: dien noi dung that vao CLAUDE.md va .claude/, "
          "roi chay: python scripts/sync-ai-config.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
