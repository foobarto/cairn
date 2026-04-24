---
description: Run the autonomous loop — one round, schedule next wakeup, repeat until stop criterion
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /cairn-loop

Run the **autonomous loop** per cairn's `cairn-autonomous-loop`
skill. Unlike `/cairn-round` (one cycle, stop), the loop keeps
picking up tasks and scheduling the next wakeup after each one,
until a stop criterion is met.

## Stop criteria

The loop stops on any of:

- **3-commit soft checkpoint** — pause, wait for user approval
  to continue.
- **5-commit hard stop** — stop unconditionally.
- **Blocker** beyond the agent's authority.
- **No bounded task** available.
- **User message** arrives mid-cycle.
- **Commit failure** that can't be resolved in-cycle.

## Autonomy level

On the first cycle, if the user's instruction is ambiguous, the
loop presents the autonomy menu (L0–L4, default L2) and caches
the choice for the session. Subsequent cycles reuse the cached
level.

## Usage

```
/cairn-loop                      # Let cairn pick tasks; L2 default
/cairn-loop --autonomy L1        # Force a specific autonomy level
/cairn-loop --until <condition>  # Stop when condition met (e.g. "P1 empty")
```

## Steps (at a glance)

Per cycle:

1. Check for user input; abandon if present.
2. First cycle only: calibrate autonomy level (menu).
3. Verify prerequisites (clean tree, journal exists).
4. Dispatch `autonomous-planner` sub-agent (if available) for
   task recommendation, or scan `docs/todo.md` directly.
5. Announce pick in the session journal with level.
6. Implement; log design calls as taken.
7. Gate (via `review-phase` skill if available).
8. Commit locally (never push unless L4 + authorised).
9. Check commit checkpoint:
   - 3rd: checkpoint pause, notify user, no wakeup.
   - 5th: hard stop.
10. Otherwise: schedule next wakeup (20-60 min default).

## Hard rules (ALWAYS)

Inherited from `cairn-autonomous-loop` skill:

- No pushes without L4 + authorisation.
- No force-pushes.
- No implementation of Draft/Placeholder proposals except at
  L2+ for completing in-progress partials.
- No bypassing safety gates.
- No deleting unfamiliar files/branches.
- No messages to chat/ticket systems without authorisation.
- One task per cycle.

## Related commands

- `/cairn-round` — single cycle, no loop, stop when done.
- `/cairn-session` — manually append an entry to today's
  session journal.
- `/cairn-init` — scaffold cairn into a new project.
