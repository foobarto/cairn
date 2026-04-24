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

1. **Check for user input** since the last wakeup. If there is
   any, abandon the round and address the message.
2. **Verify the working tree is clean** and `docs/todo.md`
   exists. If not, stop and ask.
3. **Pick one bounded task** from `docs/todo.md` (P1 first, P2
   second). Criteria: you can finish in one turn, no open design
   decisions block the path, low blast radius.
4. **Announce the pick** in today's session journal (one
   sentence: *Picked X because Y.*). Auto-create today's journal
   if missing.
5. **Implement.** Log design calls you take without asking to
   the journal as you make them.
6. **Gate.** Run the project's tests, linter, formatter,
   precommit checks. Record results in the journal.
7. **Commit locally** (never push unless authorised). Use
   conventional-commit style. Reference the task you picked.
8. **Check commit count for the session.** If this is the third
   commit (soft cap) or fifth (hard stop), **stop** and write
   the handoff — don't schedule another wakeup.
9. **Otherwise:** schedule the next wakeup (20-60 min cadence
   for open-ended rounds).

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
