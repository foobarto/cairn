# Changelog

All notable changes to cairn will be recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project skeleton — extracted from the workflow running in
  the Glorbo project as of 2026-04-24.
- `.claude-plugin/plugin.json` so cairn is installable as a Claude
  Code plugin.
- Slash commands: `/cairn-init`, `/cairn-session`, `/cairn-round`.
- Skills: `session-log`, `autonomous-round`, `close-session`.
- Sub-agent: `prior-session-digest`.
- Templates: `CLAUDE.md`, `session-template.md`, `todo.md`,
  `workflow/six-phase-checklist.md`,
  `workflow/autonomous-round-protocol.md`.
- **`templates/workflow/governing-principles.md`** — four
  governing principles adapted from Karpathy's guidelines (Think
  before coding / Simplicity first / Surgical changes /
  Goal-driven execution). Named explicitly as the backbone of
  the kit; every other artefact is shaped to make following them
  easier.
- CLI-adapter docs for Claude Code, Gemini CLI, Codex CLI,
  opencode.
- `install.sh` per-project scaffolder.

### Queued for v0.2.0

These were discussed during initial authoring and are planned
for the next cut; not in this initial commit:

- Autonomy-level menu (L0–L4) with L2 as default; applied at
  autonomous-round / autonomous-loop start.
- Split `autonomous-round` (one cycle) from `autonomous-loop`
  (repeat with checkpoints); shared core.
- `agents/autonomous-planner.md` sub-agent for bounded task
  recommendation.
- `skills/review-phase/SKILL.md` with tool detection + mandatory
  quality + security passes.
- `agents/review-runner.md` for parallel tool invocation.
- User profile (global, `~/.config/cairn/user-profile.md`) +
  project profile (tracked, `docs/project-profile.md`) with
  dedicated `build-*-profile` skills and install-time location
  prompt.
- `/cairn-loop` command counterpart to `/cairn-round`.
