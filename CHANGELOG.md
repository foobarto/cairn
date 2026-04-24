# Changelog

All notable changes to cairn will be recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — v0.2.0 in progress

### Added

- **Autonomy-level calibration** (L0–L4, default **L2**) as the
  first step of every autonomous round/loop. Menu shown when
  user intent is ambiguous; cached per session. Project-
  profile risk tolerance can cap the menu below the user's
  choice.
- **Split `autonomous-round` and `autonomous-loop` skills** —
  round = one cycle, stop when done; loop = repeating cycles
  with 3-commit soft checkpoint / 5-commit hard stop. Shared
  substance in `templates/workflow/autonomous-protocol.md`
  (renamed from `autonomous-round-protocol.md`).
- **`skills/review-phase/SKILL.md`** — orchestrates phase 5
  of the six-phase checklist. Detects available review tools
  (`codex`, `semgrep`, language linters, project gates),
  proposes a plan, runs **mandatory quality + mandatory
  security passes**. Manual OWASP fallback when no SAST tool
  is reachable.
- **`agents/autonomous-planner.md`** sub-agent — read-only
  task-selection recommender. Reads `docs/todo.md` + recent
  journals + project profile, returns a structured
  recommendation so the main agent's context stays clean.
- **`agents/review-runner.md`** sub-agent — runs detected
  review tools in parallel and returns a compressed verdict.
- **Dual profile system:**
  - `templates/user-profile.md` — global synthesis of *how the
    user thinks*. Default location `~/.config/cairn/user-profile.md`.
    Install-time menu offers global / project-gitignored /
    project-tracked / skip. Observations with evidence,
    periodically re-synthesised not blindly appended.
  - `templates/project-profile.md` — declarative statement of
    the project's stances (risk tolerance, security posture,
    quality bar, contribution norms, tech-debt stance).
    Tracked in git at `docs/project-profile.md`. Consumed
    by the planner, review-phase, and autonomy menu.
- **Two profile skills** — `cairn-build-user-profile` and
  `cairn-build-project-profile`.
- **`/cairn-loop` slash command** — repeating-cycles
  counterpart to `/cairn-round`.
- **`install.sh`** gains a `--profile-scope` option and an
  interactive prompt for user-profile location; scaffolds
  `.cairn/config.json` when a project-local scope is chosen.
- **`close-session` skill** extended with step 5 — invoke
  `build-user-profile` / `build-project-profile` when new
  signal appeared this session.
- **Six-phase checklist** phase 5 (Review) rewritten to
  make quality + security both mandatory; second opinion
  required for non-trivial changes, optional for small.

### Changed

- `templates/CLAUDE.md` → session-rhythm table now includes
  "Read project-profile for stance + user profile for
  collaboration calibration" at session start.
- `templates/CLAUDE.md` → "Autonomous-round cadence" section
  rewritten as "Autonomous work — round vs loop" with the
  autonomy-menu preamble and the protocol's hard rules.
- `README.md` layout diagram updated for v0.2.0 skills +
  agents + templates.

### Removed

- `templates/workflow/autonomous-round-protocol.md` —
  superseded by `autonomous-protocol.md` (covers both round
  and loop).

## [v0.1.0] — 2026-04-24

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
- `templates/workflow/governing-principles.md` — four
  governing principles adapted from Karpathy's guidelines (Think
  before coding / Simplicity first / Surgical changes /
  Goal-driven execution). Named explicitly as the backbone of
  the kit; every other artefact is shaped to make following them
  easier.
- CLI-adapter docs for Claude Code, Gemini CLI, Codex CLI,
  opencode.
- `install.sh` per-project scaffolder.
