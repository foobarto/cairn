---
name: cairn-autonomous-loop
version: 0.2.0
description: Use when the user wants the agent to keep picking up tasks autonomously and repeat the round cycle until a stop criterion is met — "keep going while I sleep", "run autonomously until you hit a blocker or clear P1", "loop through the punch list". Runs one round, schedules the next wakeup, repeats. Enforces commit checkpoints (3-commit soft pause, 5-commit hard stop) so silent prolific output doesn't erode trust. For exactly one cycle, use cairn-autonomous-round instead.
---

# cairn: Autonomous-loop skill

Repeat the autonomous cycle until a stop criterion is met. After
each cycle, schedule the next wakeup; at checkpoints, pause and
wait for user approval before continuing.

For exactly one cycle, see the sibling
[`cairn-autonomous-round`](../autonomous-round/SKILL.md).

## When to use this skill

- User says "keep going", "run autonomously until I stop you",
  "loop through the punch list", "work while I sleep", "run
  overnight and check back".
- A scheduled wakeup fired with the autonomous-loop sentinel
  and the previous round didn't hit a stop criterion.

## Do NOT use for

- Scoped single-task work — use `cairn-autonomous-round`.
- Interactive sessions.
- Dispatching multiple tasks in parallel — the loop is strictly
  serial, one task per cycle.

## Protocol

Substance in
[`<project>/docs/workflow/autonomous-protocol.md`](../../templates/workflow/autonomous-protocol.md).
This skill is the loop-specialisation of that protocol.

One cycle of the loop:

1. **Check for user input.** If new message, abandon; address
   the message.
2. **First cycle only: calibrate autonomy level** (menu; L2
   default). Cache the choice for the session; subsequent
   cycles reuse it.
3. Verify prerequisites.
4. Pick one bounded task (use `autonomous-planner` sub-agent
   if available).
5. Announce the pick in the session journal with autonomy
   level.
6. Implement. Log design calls as taken.
7. Gate (via `review-phase` skill if available).
8. Commit locally.
9. **Check commit-count checkpoints:**
   - **3rd commit of session (soft checkpoint):** write a
     checkpoint-handoff block in the journal, notify the user,
     do NOT schedule next wakeup. Wait for approval to continue.
   - **5th commit (hard stop):** stop unconditionally. Write
     the final handoff. No next wakeup.
10. **Check stop criteria:**
    - Blocker beyond your authority.
    - No bounded task available.
    - User message arrived during this cycle.
    - Commit just failed (hook rejection, compile error).

    If any stop criterion applies: write the final handoff,
    stop.

11. **Otherwise: schedule the next wakeup.** Cadence: 20-60
    min default; shorter if watching a specific condition
    (build ETA, scheduled task firing).

## Checkpoint-handoff format (3-commit soft pause)

```markdown
## Checkpoint — <timestamp> — 3 commits this session

**Shipped so far:**
- `<sha>` — <subject>
- `<sha>` — <subject>
- `<sha>` — <subject>

**Autonomy level:** LN (cached from first cycle).

**Pausing because:** 3-commit soft checkpoint. Not scheduling
the next wakeup; waiting for your approval to continue.

**Next candidates if you want to continue:** <tasks the
planner recommends for the next round>.

**For your review:** <numbered yes/no questions>.
```

Next time the user says "continue" or "keep going," the loop
resumes from the next cycle; the 3-commit counter resets only
if the user explicitly says "reset" or starts a new day.

## Final handoff (hard stop or stop criterion)

Same shape as the round skill's handoff, with:

- `**Shipped this loop:**` listing every SHA from the session.
- `**Stopped because:**` naming the specific criterion (5-commit
  hard stop, blocker, empty pool, user message, gate failure).
- `**Total autonomous cycles this session:** <count>`.

## Scheduling the next wakeup

Via your CLI's wakeup mechanism. In Claude Code:

```
ScheduleWakeup({
  delaySeconds: 2700,          # 45 min is a sane default
  prompt: "<<autonomous-loop-dynamic>>",
  reason: "Next loop cycle — <what you're continuing>"
})
```

In other CLIs: use whatever scheduling exists. If none is
available, the loop degrades to a single round per invocation
and the user re-invokes it manually.

## Graceful degradation if tools missing

- **No `autonomous-planner` sub-agent:** the main agent picks
  the task directly, following the autonomy-level rules.
- **No `review-phase` skill:** the main agent runs the project's
  gates manually (tests, lint, format). Quality + security are
  still mandatory — if no security tool is available, the main
  agent does a manual diff review against OWASP Top 10,
  secret handling, authz/authn boundaries, and input validation
  at system edges.
- **No wakeup scheduling:** loop becomes a single round per
  invocation. Not ideal, but functional.
