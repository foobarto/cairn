# Cairn on Codex

## Native plugin installation

```bash
codex plugin marketplace add foobarto/cairn
codex plugin add cairn@cairn
```

The plugin exposes Cairn's canonical Agent Skills. It does not create project
workflow documents or modify project instructions; use the portable installer
for that scaffolding.

## Portable project installation

Cairn's portable install defaults to the project entry point Codex uses:
`AGENTS.md`.

```bash
git clone https://github.com/foobarto/cairn ~/tools/cairn
cd /your/project
~/tools/cairn/install.sh
```

This writes the workflow files, `AGENTS.md`, and canonical skill packages under
`.agents/skills/`. Confirm the `cairn-*` skills appear in the current Codex
surface before relying on automatic activation. If that distribution does not
discover project `.agents/skills/`, keep the installed packages and reference
the relevant `SKILL.md` from `AGENTS.md` or install them through the Codex skill
or plugin mechanism documented by that distribution.

The fallback remains useful because every Cairn skill is plain Markdown and
self-contained. Canonical paths include:

- `.agents/skills/cairn-session-log/SKILL.md`
- `.agents/skills/cairn-autonomous-round/SKILL.md`
- `.agents/skills/cairn-autonomous-loop/SKILL.md`
- `.agents/skills/cairn-review-phase/SKILL.md`

## Capability mapping

- `AGENTS.md` carries stable project instructions; detailed procedures remain
  progressively disclosed in skills and `docs/workflow/`.
- If subagents are available, Cairn can delegate bounded planning or skeptical
  review. If not, the main agent performs the work and reports the gap.
- A normal Codex run can complete one autonomous round. A repeated loop needs
  an actual continued-run, recurring-task, or resume capability; the skill
  never invents one.
- Cairn never treats Codex memory as interchangeable with the user profile.
  Persistent personal writes require explicit authorization.

The Claude-only `commands/` and `agents/` directories are adapters, not
requirements for Codex use. Codex behavior comes from the canonical `skills/`
packages referenced by `.codex-plugin/plugin.json`.
