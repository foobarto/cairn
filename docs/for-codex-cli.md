# cairn on Codex CLI

Codex CLI uses `AGENTS.md` as its project instructions file. cairn's
templates and skills are Codex-compatible; only the file names
and invocation style differ from Claude Code.

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

3. In `AGENTS.md`, reference the cairn skills as read-and-follow
   instructions:

   ```markdown
   ## Session rhythm (cairn)

   Before any working session: read `docs/sessions/` for today's
   entry (if any), and read `docs/todo.md` for the active punch
   list.

   When the user asks for a new session log entry or says
   something worth logging, follow
   `~/tools/cairn/skills/session-log/SKILL.md` verbatim.

   When the user says "continue autonomously" or similar, follow
   `~/tools/cairn/skills/autonomous-round/SKILL.md` verbatim —
   including the hard rules (no pushes without authorisation,
   no force-pushes, no implementation of Draft proposals, no
   bypass of safety gates).

   When closing out, follow
   `~/tools/cairn/skills/close-session/SKILL.md`.
   ```

## What Codex maps cleanly

- **`AGENTS.md`** ↔ cairn's `CLAUDE.md` template (same shape,
  different filename).
- **Codex's tool-use** reads arbitrary local files — the `.md`
  skill files are directly actionable.
- **Codex's session persistence** (if using `codex exec` with a
  session id) pairs well with cairn's per-date journals —
  consider naming session ids after the journal slug.

## What Codex CLI doesn't have built-in

- Slash commands — emulate by invoking through a shell alias or
  your shell history. Example:

  ```bash
  # ~/.bashrc
  alias cairn-session='codex exec "Follow the cairn session-log skill at \
    ~/tools/cairn/skills/session-log/SKILL.md to append today'\''s entry"'
  alias cairn-round='codex exec "Follow the cairn autonomous-round skill at \
    ~/tools/cairn/skills/autonomous-round/SKILL.md for one cycle"'
  ```

- Auto-memory — cairn's skills mention "save as memory" for
  user preferences; Codex has partial memory support via its
  `memory/` directory. Skills degrade gracefully if memory
  isn't available.

- Sub-agents — `prior-session-digest` has no direct analog. A
  `codex exec --model haiku` call with the agent prompt pinned
  does the same job cheaply.

## Tradeoffs

- **Plus:** `codex exec` from CI is straightforward; cairn's
  autonomous-round protocol maps cleanly onto scheduled CI
  runs.
- **Minus:** No auto-skill-discovery. Every session is slightly
  more explicit about which skill to apply.
- **Plus:** Codex's `--sandbox` mode gives cairn the "safe
  autonomous run" story for free.

## AGENTS.md excerpt

```markdown
# AGENTS.md

<!-- Keep short. Project-specific detail lives in docs/. -->

## Session rhythm (cairn)

This project uses cairn for session journals, rolling punch list,
and autonomous rounds. See docs/workflow.md for the shape.

- Session journal: `docs/sessions/<YYYY-MM-DD>-<topic>.md`.
  Append as you go. See
  `~/tools/cairn/skills/session-log/SKILL.md`.
- Rolling punch list: `docs/todo.md`. P0/P1/P2/P3 priorities.
- Autonomous rounds: `~/tools/cairn/skills/autonomous-round/SKILL.md`.
  Hard rules: no pushes without authorisation, no force-pushes,
  no Draft-proposal implementation, no safety-gate bypass.
- Close-out: `~/tools/cairn/skills/close-session/SKILL.md`.

## Coding discipline

1. Think before coding; state assumptions.
2. Simplicity first; no speculative abstractions.
3. Surgical changes; preserve existing style.
4. Goal-driven execution; loop until verified.
```
