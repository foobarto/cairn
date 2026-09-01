---
name: cairn-autonomous-loop
description: Run repeated, serial Cairn work cycles when the user explicitly asks the agent to keep going until a stop condition. Requires a client that can continue or resume work; use cairn-autonomous-round for exactly one cycle.
metadata:
  version: "0.3.0"
---

# cairn: Autonomous-loop skill

Repeat the autonomous cycle serially until a stop criterion is met.
Continue in the current run when the client supports it, or use a
client-provided resume mechanism. At checkpoints, yield to the user.

For exactly one cycle, use the `cairn-autonomous-round` skill.

## When to use this skill

- User says "keep going", "run autonomously until I stop you",
  "loop through the punch list", "work while I sleep", "run
  overnight and check back".
- A client resumes a previously authorized loop and the previous
  round did not hit a stop criterion.

## Do NOT use for

- Scoped single-task work — use `cairn-autonomous-round`.
- Interactive sessions.
- Dispatching multiple tasks in parallel — the loop is strictly
  serial, one task per cycle.

## Protocol

If the target project contains `docs/workflow/autonomous-protocol.md`,
read it before proceeding. This skill is the loop-specialisation of
that installed protocol; the rules below are the portable fallback.

One cycle of the loop:

1. **Check for user input.** If the client exposes new input, stop
   the loop and address it.
2. **First cycle only: calibrate autonomy level** (menu; L2
   default). Cache the choice for the session; subsequent
   cycles reuse it.
3. Verify prerequisites.
4. Pick one bounded task (use `autonomous-planner` sub-agent
   if available). If `.ep-kit` exists and the item cites a proposal, invoke
   `cairn-strata-interop`; only status-authorized work is eligible.
   If that sibling skill is unavailable, read `.ep-kit` directly as its public
   `key=value` contract (`dir` defaults to `docs/eps`) and inspect the installed
   proposal process. Placeholder and Draft are ineligible unless a separate,
   scoped pre-acceptance override explicitly acknowledges the unaccepted
   status; Withdrawn and Rejected remain ineligible; Accepted and Partial are
   eligible; Implemented permits only maintenance; Superseded follows its
   replacement.
5. Announce the pick in the session journal with autonomy
   level.
6. Implement. Log design calls as taken.
7. Gate (via `cairn-review-phase` skill if available).
8. Commit locally only when the request or project policy authorizes it. Never
   infer permission to push.
9. **Check completed-change checkpoints:**
   - **3rd completed cycle (soft checkpoint):** write a
     checkpoint-handoff block in the journal, notify the user,
     do not resume the loop. Wait for approval to continue.
   - **5th completed cycle (hard stop):** stop unconditionally. Write
     the final handoff. No next continuation.
10. **Check stop criteria:**
    - Blocker beyond your authority.
    - No bounded task available.
    - User message arrived during this cycle.
    - Commit just failed (hook rejection, compile error).

    If any stop criterion applies: write the final handoff,
    stop.

11. **Otherwise: continue or arrange a resume** using a capability
    the current client actually provides. If no continuation mechanism
    exists, stop after this round and report that limitation.

## Checkpoint-handoff format (3-cycle soft pause)

```markdown
## Checkpoint — <timestamp> — 3 cycles this session

**Shipped so far:**
- `<sha>` — <subject>
- `<sha>` — <subject>
- `<sha>` — <subject>

**Autonomy level:** LN (cached from first cycle).

**Pausing because:** 3-cycle soft checkpoint. Not resuming the
loop; waiting for your approval to continue.

**Next candidates if you want to continue:** <tasks the
planner recommends for the next round>.

**For your review:** <numbered yes/no questions>.
```

Next time the user says "continue" or "keep going," the loop
resumes from the next cycle; the 3-cycle counter resets only
if the user explicitly says "reset" or starts a new day.

## Final handoff (hard stop or stop criterion)

Same shape as the round skill's handoff, with:

- `**Shipped this loop:**` listing every SHA from the session.
- `**Stopped because:**` naming the specific criterion (5-cycle
  hard stop, blocker, empty pool, user message, gate failure).
- `**Total autonomous cycles this session:** <count>`.

## Continuing the loop

Use only a continuation mechanism the current client documents and
actually exposes: continued execution in the same run, a recurring task,
or a scheduled resume. Do not invent a tool name or claim that a future
resume was scheduled when it was not. Record the mechanism and its stop
condition in the journal. If the client cannot continue autonomously,
complete one round, return the handoff, and tell the user how to resume.

## Graceful degradation if tools missing

- **No `autonomous-planner` sub-agent:** the main agent picks
  the task directly, following the autonomy-level rules.
- **No `cairn-review-phase` skill:** the main agent runs the project's
  gates manually (tests, lint, format). Quality + security are
  still mandatory — if no security tool is available, the main
  agent performs a proportional manual review of applicable trust boundaries,
  secret handling, authorization, path/command handling, and external input.
- **No continuation mechanism:** loop becomes a single round per
  invocation, with an explicit limitation in the handoff.
