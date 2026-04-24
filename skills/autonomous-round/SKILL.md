---
name: cairn-autonomous-round
version: 0.2.0
description: Use when the user wants ONE bounded autonomous cycle — pick a task from docs/todo.md, implement, gate, commit, hand control back. Not a loop; one round and done. Triggers on phrases like "do one task from the punch list", "pick one thing and run it", "finish the Kanban refactor autonomously" when scoped to a single item. For repeating "keep going until I stop you" mode, use the cairn-autonomous-loop skill instead.
---

# cairn: Autonomous-round skill

Drive exactly **one** bounded autonomous cycle. One task, one
commit, one journal entry, explicit handoff. No re-scheduling,
no chaining — when the cycle is done, control goes back to the
user.

For repeating cycles, see the sibling
[`cairn-autonomous-loop`](../autonomous-loop/SKILL.md) skill.

## When to use this skill

- User says "do one task", "pick one from the punch list and
  run it", "finish the Kanban refactor autonomously" (scoped to
  one item), "take this one to done then stop".
- A scheduled wakeup fired (loop mode) but the user has asked
  to convert the remaining work to a single round.

## Do NOT use for

- Interactive sessions where the user is actively typing — use
  your normal flow; the round protocol is overkill mid-dialog.
- Multi-step plans that need user checkpoints between steps.
  If the "task" is actually "build feature X" with three design
  decisions along the way, stop and ask before starting.
- Open-ended "keep going while I sleep" — that's
  `cairn-autonomous-loop`, not this skill.

## Protocol

The substance — autonomy-level menu, task-pick rules, gate
requirements, hard rules, mid-cycle ask-anyway cases — lives in
[`<project>/docs/workflow/autonomous-protocol.md`](../../templates/workflow/autonomous-protocol.md).
Read that before proceeding; this skill is a thin orchestration
wrapper over the protocol, specialised for *one cycle only*.

Summary of the round-specific shape:

1. Check for new user input; abandon if present.
2. **Calibrate autonomy level** (menu; L2 default). Log the
   selected level in the session journal.
3. Verify prerequisites (clean tree, journal exists or is
   creatable, `docs/todo.md` exists).
4. **Pick one bounded task.** If cairn's `autonomous-planner`
   sub-agent is available, dispatch it for a recommendation;
   otherwise scan `docs/todo.md` directly per the autonomy
   level's rules.
5. Announce the pick in the journal: *Picked X because Y.
   Autonomy level: LN.*
6. Implement.
7. Gate. If the `review-phase` skill is available, invoke it
   for quality + security passes.
8. Commit locally. No push.
9. **Write the handoff summary** and stop. Do NOT schedule a
   next wakeup — this skill is one-cycle-only.

## Handoff format

The final action in the session journal (written by this
skill's last step) must match the protocol's handoff block:

```markdown
## Handoff — <timestamp>

**Shipped this round:** <SHA> — <commit subject>.

**Autonomy level used:** <L0/L1/L2/L3/L4>.

**Stopped because:** round complete (single-cycle scope).

**Queued if you want more:** <next bounded tasks, or "nothing
obvious">.

**For your review:** <numbered yes/no questions>.
```

## Relationship to the loop skill

- `autonomous-round` = this skill. One cycle. Stop.
- `autonomous-loop` = sibling skill. Multiple cycles with
  checkpoint pauses and wakeup scheduling.

Both dispatch the same underlying protocol. Pick the skill that
matches what the user asked for; don't try to run a loop
through this skill by invoking it repeatedly.
