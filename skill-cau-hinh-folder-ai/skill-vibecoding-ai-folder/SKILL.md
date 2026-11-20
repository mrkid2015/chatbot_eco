# Vibecoding AI Folder Setup for Claude Code, Codex and Antigravity

## Set up one master folder for all three AI tools

- Scaffold a new project by running `python3 ~/workspace/custom-skills/vibecoding_ai_folder/scripts/scaffold_ai_folder.py <project-folder>` with `muse.exec`.

- Pass the project display name with the `--ten` flag when the user gives one, and leave the flag out to use the folder name.

- Never pass `--force` unless the user asks to overwrite files that already exist in the target project.

- Read the full structure, the per tool reading table and the sync mapping in [the folder structure reference](references/cau-truc-folder.md) before you explain the layout or adapt it.

## Keep one master copy and generate the rest

- Treat `.claude/` plus the root `CLAUDE.md` as the only master copy, and write every skill, command, rule and agent only there.

- Generate `AGENTS.md` from `CLAUDE.md` so Codex and Antigravity read the same guidance that Claude Code reads.

- Generate `.agents/skills/` and `.agents/rules/` for Codex and Antigravity, and never edit those generated files by hand.

- Generate `.codex/agents/*.toml` from `.claude/agents/*.md`, and keep `.codex/config.toml` as the one hand written Codex file.

- Leave `.claude/plans/` and `.claude/references/` without generated copies because the tools read reference material in place.

## Sync after every master edit

- Run `python3 scripts/sync-ai-config.py` from the project root after any edit inside `.claude/` or to `CLAUDE.md`.

- Copy skills from `.claude/skills/` to `.agents/skills/` unchanged during the sync.

- Convert each file under `.claude/commands/` into a skill under `.agents/skills/` during the sync because Codex and Antigravity dropped slash commands in favour of skills.

- Flatten each file under `.claude/rules/` into `.agents/rules/` during the sync and add a `trigger` frontmatter field, with `always_on` as the default and `model_decision` for large reference style rules listed in the script.

- Convert each agent under `.claude/agents/` into a TOML file under `.codex/agents/` during the sync, carrying `name`, `description` and `developer_instructions`.

- Tell the user to open a new AI session after a sync because newly added agents and skills only load at session start.

## Verify the generated project

- Run the scaffold and then the sync on a throwaway folder before you claim the setup works for a new variant.

- Parse every generated TOML file with a TOML reader and check that each one has `name`, `description` and `developer_instructions`.

- Check that `.agents/skills/` holds both the copied skills and the skills converted from commands, and that `.agents/rules/` files carry a `trigger` line.

- Check that a hand written `AGENTS.md` survives a sync untouched, because the sync only regenerates `AGENTS.md` when it carries the generated header.

## Start from the six starter agents

- Ship the six starter agents from the source video, named project-manager, ui-ux-designer, software-engineer, qa-test-engineer, devops-engineer and sre-ops-engineer.

- Replace the starter agent bodies, the sample skill, the sample command and the sample rule with the real project content before real use.

- Keep the docs skeleton with `01-tong-quan`, `02-ky-thuat`, `03-san-pham`, `04-van-hanh`, `05-mau`, `06-design`, `99-ghi-chu` and `handoff` only when the user wants the project docs layout from the video as well.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Offer to import an existing agent, skill or rule library into `.claude/` first and sync second, instead of starting from the starter set, when the user already has a library such as a GitHub agent collection.

- Offer a copy of the generated starter project as a zip in the user files when the user wants to try the layout on their own Windows machine before adopting it.
