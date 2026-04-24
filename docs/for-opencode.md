# cairn on opencode

[opencode](https://opencode.ai/) uses an `AGENTS.md` file for
project instructions (like Codex). cairn's setup is nearly
identical; this doc covers the deltas.

## Install

1. Clone cairn:

   ```bash
   git clone https://github.com/foobarto/cairn ~/tools/cairn
   ```

2. Scaffold into a project:

   ```bash
   cd /your/project
   ~/tools/cairn/install.sh
   mv CLAUDE.md AGENTS.md
   ```

   Or, if opencode's config points at a different filename in
   your setup (check your `opencode.json`), move to that
   filename.

3. Reference the skills from `AGENTS.md` the same way the
   [Codex doc](for-codex-cli.md) describes. The invocation
   syntax differs (`opencode run ...` vs `codex exec ...`) but
   the underlying "read the skill file and follow it" pattern
   works identically.

## opencode specifics

- **Model choice.** cairn doesn't assume any particular
  provider. opencode's ability to multiplex across providers
  (Anthropic, OpenAI, Google, local) pairs well with cairn's
  CLI-agnostic design — the skills work regardless of which
  model executes them.
- **Custom commands.** opencode's `command` feature (in
  `opencode.json`) lets you define project-local shortcuts
  that wrap the cairn skills. Example:

  ```json
  {
    "commands": {
      "session": "Follow the cairn session-log skill at ~/tools/cairn/skills/session-log/SKILL.md to append today's entry",
      "round": "Follow the cairn autonomous-round skill at ~/tools/cairn/skills/autonomous-round/SKILL.md for one cycle",
      "close": "Follow the cairn close-session skill at ~/tools/cairn/skills/close-session/SKILL.md"
    }
  }
  ```

  After restart:

  ```
  /session
  /round
  /close
  ```

  are available inside opencode's REPL.

- **Agents.** opencode supports custom agent definitions in
  `opencode.json` / `.opencode/agent/`. The
  `prior-session-digest` sub-agent translates directly —
  port the agents/prior-session-digest.md to opencode's agent
  schema and call it when starting a session.

## What you keep

- All templates (`CLAUDE.md` template, session-template,
  todo.md, workflow docs).
- All skill substance.
- The convention: session journals at `docs/sessions/`,
  punch list at `docs/todo.md`, proposals at `docs/eps/` or
  equivalent.

## What you lose vs Claude Code plugin

- Auto-discovery of skills — opencode needs you to tell it
  which skill to use for which trigger, either via
  `AGENTS.md` (general) or custom commands (per-invocation).
- The official Claude Code `SKILL.md` frontmatter format is
  Claude-specific; opencode reads the body and ignores the
  frontmatter (which is fine).

## opencode AGENTS.md excerpt

```markdown
# AGENTS.md

## Session rhythm (cairn)

Session journal: `docs/sessions/<YYYY-MM-DD>-<topic>.md`.
Follow `~/tools/cairn/skills/session-log/SKILL.md` when appending.

Rolling punch list: `docs/todo.md` (P0-P3 tiers).

Autonomous rounds (user said "continue autonomously"): follow
`~/tools/cairn/skills/autonomous-round/SKILL.md`. Hard rules:
no pushes without authorisation, no force-pushes, no Draft-proposal
implementation, no safety-gate bypass, one task per turn,
3 commits soft cap / 5 hard stop per session.

Close-out: `~/tools/cairn/skills/close-session/SKILL.md`.

Proposals (if project uses ep-kit): `docs/eps/`. Follow ep-kit's
own skill for drafting.
```
