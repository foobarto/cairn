---
name: cairn-autonomous-round
version: 0.1.0
description: Use when the user has said "continue autonomously", "keep going", "pick something from the todo list while I'm away", "run unattended for a while", or similar. Guides the agent through one bounded autonomous-round cycle — pick a single task from docs/todo.md, log design calls as you take them, gate with the project's tests, commit locally, and write a handoff summary. Enforces the hard rules (no pushes without authorisation, no force-pushes, no implementation of Draft/Placeholder proposals) and the "when to stop" criteria (3-5 commits soft cap, user message arrives, blocker hit, obvious-next-task pool empty).
---

# cairn: Autonomous-round skill

Drive one bounded **autonomous-round cycle**. This is the
discipline cairn enforces for unattended work: one task, one
commit, one journal entry, explicit handoff.

## When to use this skill

- User said "continue autonomously" / "keep going" / "run
  unattended" / "pick something from the todo" / similar.
- A scheduled wakeup fired the autonomous-loop sentinel.
- You just finished a task unattended and are deciding whether
  to pick up the next one.

## Do NOT use for

- Interactive sessions where the user is actively typing. Use
  your normal flow — autonomous-round discipline is overkill
  when the user is in the loop.
- Tasks the user has explicitly directed you to work on (those
  just need the session-log skill, not the full round
  protocol).
- Multi-step plans that need user checkpoints between steps. If
  the "task" is actually "build feature X" with three design
  decisions along the way, stop and ask before starting.

## The loop (one cycle)

1. **Check for user input.** If the user has messaged since the
   last wakeup, abandon the round and address the message.
2. **Verify prerequisites.** `docs/todo.md` exists. Session
   journal for today exists or will be created. The working
   tree is clean (no uncommitted changes from an earlier task).
3. **Pick one bounded task.** Scan `docs/todo.md`:
   - P0 items first.
   - Then P1 items (the "next cycle" pool — this is usually
     where autonomous rounds draw from).
   - P2 if the user's instructions permit; otherwise skip.
   - P3 only if explicitly allowed.
   Choose the task that is:
   - Bounded (can finish in one turn).
   - Unambiguous (no open design decisions block the path).
   - Low-blast-radius (no schema migrations, deletions, or
     shared-state mutations without user sign-off).
4. **Announce the pick in the session journal.** One sentence:
   *Picked X because Y.* If multiple plausible tasks exist,
   name the ones you passed over and why.
5. **Implement.** Stick to the six-phase checklist. When you
   take a design call without user input, log it to the
   journal in the same turn.
6. **Gate.** Run the project's tests, linter, formatter, and
   any precommit checks. Record tool + command + result in the
   *Gates* section of the journal entry. Check exit codes
   explicitly where the tool reports warnings without non-zero
   exit.
7. **Commit locally.** Conventional-commit style:
   `<type>(<scope>): <subject>`. The body explains the *why* if
   non-obvious; reference the task you picked from the punch
   list.
8. **Decide: continue or stop.** See "When to stop."
9. **If continuing:** schedule the next wakeup using your CLI's
   mechanism. Cadence guidance: 20-60 min for open-ended rounds
   where the next task isn't time-sensitive. Use shorter if
   you're watching a specific condition.
10. **If stopping:** write the handoff summary at the end of
    the session journal. No scheduled wakeup.

## Hard rules (NEVER)

- **Never push to a remote** unless the user's instructions
  explicitly authorise it. Local commits are fine; they're
  easy to undo.
- **Never force-push** or rewrite commits that have been
  pushed, or that touch others' work.
- **Never start implementation** of a proposal whose status is
  `Draft` or `Placeholder`. Those are explicitly under-review;
  implementing them is a user call.
- **Never bypass safety gates** (commit hooks, signing, test
  runners) by passing `--no-verify`, `--no-gpg-sign`, etc. If a
  gate fails, diagnose. The gate is there for a reason.
- **Never delete or move unfamiliar files.** If you find
  something you don't recognise (untracked file, unknown
  branch), leave it alone. Note it in the journal and ask.
- **Never send messages to chat platforms, ticket systems, or
  external services** without explicit authorisation — even
  harmless-seeming status updates. The session journal is the
  sanctioned status-update channel.
- **Never start a second task in the same turn.** One task per
  turn, period.

## When to stop the loop

Stop (don't schedule a next wakeup) if:

- **Blocker hit.** Design decision beyond your authority,
  ambiguous failing gate, risk of data loss or shared-state
  corruption. Write up the blocker, list what you considered,
  and stop.
- **Obvious-next-task pool is empty.** P1 is cleared, P2 is all
  "revisit if feedback complains" placeholders. Don't force a
  pick.
- **Commit cap reached.** Three commits is a soft cap; five is
  a hard stop. Silent prolific output without a user checkpoint
  erodes trust.
- **Incoming user message.** Abandon the loop immediately,
  address the message.
- **Commit failed** (pre-commit hook, unresolvable compile
  error). Leave the tree clean, note the failure, surface it.
- **Your own judgement says "this deserves a checkpoint."**
  Not every instinct needs justification. If something feels
  like it needs the user's eyes before the next step, that's
  enough.

## Mid-round "ask anyway" cases

Even within an autonomous round, some decisions deserve stopping
to ask:

- The change risks data loss, shared-state corruption, or is
  hard to reverse (schema migration, force-push, file
  deletion, force-reset).
- The user's instructions could be interpreted two very
  different ways. Pick one visibly and ask whether it was
  right; don't silently choose.
- The change would touch files the user clearly intended to
  work on themselves (recent untracked edits, half-finished
  branches, half-typed commit message, etc.).
- The scope of the "bounded task" you picked ballooned mid-
  implementation. If the task you thought was ~30 lines is now
  ~300 lines touching five files, stop. Either re-scope or ask.

## Handoff summary

When the loop ends (for any reason), the last action in the
session journal must be a handoff block:

```markdown
## Handoff — <timestamp>

**Shipped this round:** <commit SHAs + one-liners>.

**Stopped because:** <which stop criterion applied>.

**Queued if you want more:** <tasks I considered next but
didn't pick — or "nothing obvious">.

**For your review:** <specific yes/no questions parked above>.
```

That's what the user reads when they get back. Terse, honest,
no filler.

## Memory

If your CLI has persistent memory, save:

- User preferences revealed during the round (coding style,
  tool choices, review rituals).
- Project-specific gotchas you discovered (flaky tests, surprising
  call chains, invariants enforced in unusual places).
- Decisions taken autonomously that the user might want to
  revisit — flag them in memory as "provisional, review on next
  session."

Don't save:

- Task-ephemeral state (the session journal already carries this).
- Hot opinions about the codebase; memories are for load-bearing
  facts, not colour.
