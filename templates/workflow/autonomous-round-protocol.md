# Autonomous-round protocol

When the user asks the agent to "keep going," "run autonomously
for a while," "pick something from the punch list while I'm
away," or similar — follow this protocol. It's a discipline for
unattended work that keeps the blast radius bounded and the trail
legible.

## The loop

1. **Pick one bounded task.** From `docs/todo.md` (P1 first, P2
   second, P3 only if nothing else applies). Bounded means:
   - You can finish it, gate it, and commit it in one turn.
   - You know what "done" looks like before you start.
   - No open design decisions block the path.
2. **State the pick** at the top of a new session-journal entry.
   One sentence: *Picked X because Y.*
3. **Implement.** Log design calls you take without asking, in
   the journal, as you take them.
4. **Gate.** Run the project's tests, linter, formatter, and any
   precommit checks. Record results in the journal.
5. **Commit locally.** Conventional-commit style subject; body
   explains the *why* if it's non-obvious.
6. **Decide: continue or stop?** See "When to stop," below.
7. **If continuing:** schedule the next wakeup (via your CLI's
   scheduling mechanism) with a reasonable cadence (20–60 min is
   a good default for open-ended rounds).

## Hard rules

- **Never push** unless the user has explicitly authorised
  pushes in their instructions. Local commits are fine; they can
  be force-reset if needed.
- **Never force-push or rewrite** commits that have been pushed
  or that touch others' work.
- **Never start implementation** of a proposal still in `Draft`
  or `Placeholder` status without explicit user approval.
- **Never bypass safety gates** (hooks, pre-commit checks,
  signing) without explicit authorisation. If a gate fails,
  diagnose and fix the underlying issue — don't route around.
- **Never delete unfamiliar files or branches.** If you find
  something you don't recognise, assume it's in-progress work
  and leave it alone; note it in the journal and ask.
- **Never send messages to chat platforms, tickets, or external
  services** without explicit authorisation — even status
  updates. Logging to the session journal is the sanctioned
  "status update" channel for autonomous rounds.

## When to stop

Stop the loop (don't schedule a next wakeup) if any of these
applies:

- **You hit a blocker that needs user judgement.** A design
  decision, a failing gate whose cause is unclear, a file
  layout change that might affect others' work. Stop, write the
  blocker up in the journal, post a clear *Things I'd like your
  review on* list at the end.
- **The obvious-next-task pool is empty.** P1 is cleared, P2 is
  all "revisit if feedback complains" or similar "not ready"
  placeholders. Don't force-pick something just to have a task.
- **Three-to-five commits landed.** Silent prolific output
  without a checkpoint is worse than fewer commits plus a
  handoff. Three is a decent soft cap; at five you're definitely
  past it.
- **A user message arrives.** Obvious, but worth stating: an
  incoming prompt preempts the loop. Address the message; do
  not keep picking up new tasks until the user signals you
  should continue.
- **A commit failed** (pre-commit hook, compile error you can't
  fix in the round). Leave the working tree clean, note the
  failure, surface it.

## When to ask even mid-round

The protocol says "log design calls without asking," but *some*
decisions genuinely need user input mid-round. Stop and ask if:

- The change risks data loss, shared-state corruption, or is
  hard to reverse (e.g. schema migration, force-push, file
  deletion).
- The user's instructions could be interpreted two very
  different ways. Pick one visibly and ask if it was right,
  don't silently choose.
- The change would touch files the user clearly intended to
  work on themselves (recent untracked edits, half-finished
  branches, etc.).

## Handoff summary

When you stop the loop (for any reason), the last action in the
session journal should be a short handoff:

- What's been committed (concrete SHAs).
- What was NOT done, with reason.
- What the user should review / decide before the next round.
- Whether you've scheduled a next wakeup, and when.

That summary is what the user reads when they get back. Make it
terse and honest.
