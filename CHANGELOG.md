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
- CLI-adapter docs for Claude Code, Gemini CLI, Codex CLI,
  opencode.
- `install.sh` per-project scaffolder.
