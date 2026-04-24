---
description: Run one bounded autonomous-round cycle
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /cairn-round

Run one bounded **autonomous-round cycle** per cairn's
`cairn-autonomous-round` skill. Pick a task from `docs/todo.md`,
implement it, gate it, commit it, update the session journal.

## Scope

Exactly one task, one commit, one journal entry. If you want to
run multiple rounds back-to-back, schedule a next wakeup at the
end of each round — don't chain them in a single `/cairn-round`
invocation.

## Steps (at a glance)

Per the autonomous protocol:

1. **Check for user input** since the triggering message. If
   present, abandon the round.
2. **Calibrate autonomy level** (L0–L4, default L2). If
   cached from an earlier round in the same session, reuse.
3. **Verify prerequisites** — clean tree, journal exists or
   creatable, `docs/todo.md` exists.
4. **Pick one bounded task.** Dispatch `autonomous-planner`
   sub-agent if available; else scan `docs/todo.md` directly
   per the autonomy level's rules.
5. **Announce the pick** in today's session journal with the
   autonomy level.
6. **Implement.** Log design calls as taken.
7. **Gate.** Via `review-phase` skill if available (quality +
   security both mandatory); else run the project's tests,
   linter, formatter manually.
8. **Commit locally** (never push unless L4 + authorised).
9. **Write the handoff summary and stop.** Do NOT schedule a
   next wakeup — this command is single-cycle only. For
   repeating cycles, use `/cairn-loop`.

## Hard rules (ALWAYS)

- No pushes without explicit user authorisation.
- No force-pushes.
- No implementation of `Draft` / `Placeholder` proposals.
- No bypassing safety gates (`--no-verify`, `--no-gpg-sign`).
- No deleting unfamiliar files/branches.
- No messages to chat / ticket systems without authorisation.
- One task per turn.

## Stop criteria

Stop (don't schedule next wakeup) if:

- Blocker beyond your authority (design call, unresolvable
  gate failure, shared-state risk).
- No bounded task available in `docs/todo.md`.
- 3rd commit of the session (soft cap) or 5th (hard stop).
- User message arrived mid-round.
- Commit failed (hook rejection, compile error).

Always write a handoff summary at session close.

## Usage

```
/cairn-round                 # Let cairn pick a task
/cairn-round <task-hint>     # Prefer tasks matching the hint
```

The `<task-hint>` is a soft filter — the agent still checks
bounded-ness and prerequisites; a hint that doesn't match any
bounded P1/P2 task is ignored with a note.
