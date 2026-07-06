# AGENTS.md

This project uses a compact harness for AI-assisted development.

Start here:
1. Read `harness/MAIN_HARNESS.md`.
2. Use `harness/ROUTING.md` to select only the needed files.
3. For UI design, use `harness/skills/design-skill.md`.
4. For checks, use only the relevant files in `harness/checks/`.

Hard reminders:
- Do not modify `backend/` for React UI tasks.
- Never put API keys in React code.
- Never expose `.env` values.
- Do not change the `/analyze` response schema.
- Prefer one file, one task, one change.

If the task is educational support, also follow:
- `harness/agents/ai-tutor-rules.md`