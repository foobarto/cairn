---
name: cairn-autonomous-round
description: Run exactly one bounded Cairn work cycle when the user asks the agent to pick or complete one task autonomously, verify it, and hand control back. Use cairn-autonomous-loop only for explicit repeated execution.
metadata:
  version: "0.3.0"
---

# cairn: Autonomous-round skill

Drive exactly **one** bounded autonomous cycle. One task, one
verified result, one journal entry, explicit handoff. No re-scheduling,
no chaining — when the cycle is done, control goes back to the
user.

For repeating cycles, use the `cairn-autonomous-loop` skill.

## When to use this skill

- User says "do one task", "pick one from the punch list and
  run it", "finish the Kanban refactor autonomously" (scoped to
  one item), "take this one to done then stop".
- A resumed loop was narrowed by the user to one remaining round.

## Do NOT use for

- Interactive sessions where the user is actively typing — use
  your normal flow; the round protocol is overkill mid-dialog.
- Multi-step plans that need user checkpoints between steps.
  If the "task" is actually "build feature X" with three design
  decisions along the way, stop and ask before starting.
- Open-ended "keep going while I sleep" — that's
  `cairn-autonomous-loop`, not this skill.

## Protocol

If the target project contains `docs/workflow/autonomous-protocol.md`,
read it before proceeding. It owns the detailed autonomy menu,
task-selection rules, gates, hard rules, and ask-anyway cases. The
summary below is the portable fallback when that project file is absent.

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
   If `.ep-kit` exists and the item cites a proposal, invoke
   `cairn-strata-interop` first; only status-authorized work is eligible.
   If that sibling skill is unavailable, read `.ep-kit` directly as its public
   `key=value` contract (`dir` defaults to `docs/eps`) and inspect the installed
   proposal process. Placeholder and Draft are ineligible unless a separate,
   scoped pre-acceptance override explicitly acknowledges the unaccepted
   status; Withdrawn and Rejected remain ineligible; Accepted and Partial are
   eligible; Implemented permits only maintenance; Superseded follows its
   replacement.
5. Announce the pick in the journal: *Picked X because Y.
   Autonomy level: LN.*
6. Implement.
7. Gate. If the `cairn-review-phase` skill is available, invoke it
   for quality + security passes.
8. Commit locally only when the user's request or project policy
   authorizes commits. Never infer permission to push.
9. **Write the handoff summary** and stop. Do NOT schedule a
   continuation — this skill is one-cycle-only.

## Handoff format

The final action in the session journal (written by this
skill's last step) must match the protocol's handoff block:

```markdown
## Handoff — <timestamp>

**Shipped this round:** <SHA and subject, or verified uncommitted result>.

**Autonomy level used:** <L0/L1/L2/L3/L4>.

**Stopped because:** round complete (single-cycle scope).

**Queued if you want more:** <next bounded tasks, or "nothing
obvious">.

**For your review:** <numbered yes/no questions>.
```

## Relationship to the loop skill

- `cairn-autonomous-round` = this skill. One cycle. Stop.
- `cairn-autonomous-loop` = sibling skill. Multiple serial cycles with
  checkpoint pauses and client-supported continuation.

Both dispatch the same underlying protocol. Pick the skill that
matches what the user asked for; don't try to run a loop
through this skill by invoking it repeatedly.
