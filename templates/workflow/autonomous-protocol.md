# Autonomous-work protocol

When the user asks the agent to "keep going," "run autonomously
for a while," "pick something from the punch list while I'm
away," or similar — follow this protocol. It's a discipline for
unattended work that keeps the blast radius bounded and the
trail legible.

This doc covers both modes:

- **Round** — one cycle, stop when done, hand control back.
- **Loop** — repeat rounds using a client-supported continuation
  mechanism, stopping at a checkpoint or stop criterion.

The substance (task pick, gates, commit, journal) is identical.
The delta is *what happens after step 8*: stop (round) or
continue through a capability the current client actually exposes (loop).

## Governing principles apply first

Before anything else, re-read
[governing-principles.md](governing-principles.md). The loop is
how you execute; the principles are what make execution
legible. Every decision the protocol asks you to log is a
chance to apply them.

## Autonomy-level calibration (first step of every round / loop)

At the **start** of autonomous work, confirm which level of
autonomy is expected. If the user's instruction unambiguously
specifies a scope ("just finish the Kanban refactor" → L2 on
that specific work), skip the menu. Otherwise present this
menu once, cache the answer for the session:

```
Autonomy level for this <round|loop>?

  [L0] Supervised — ask before picking any task. Default for
       risky or unfamiliar projects.
  [L1] Conservative — pick unambiguously bounded P0/P1 tasks.
       Do not pick unfinished implementation or proposal work.
  [L2] Partials too (default) — L1 plus incomplete bounded code,
       tests, or docs. Proposal-governed code requires an Accepted
       or Partial proposal; Draft/Placeholder never authorizes it.
  [L3] Expansive — L2 plus proposal research or drafting and
       bounded P2 work. Never infer authority to change proposal
       status, accept a design, or publish.
  [L4] Publish — L3 plus: push to remote after all gates green.
       Rare and opt-in.

Pick [L0/L1/L2/L3/L4] (default: L2):
```

**Default is L2.** Here, an in-progress partial means code, tests, or
documentation whose governing design is already accepted (or does not
need a proposal). It never means implementation governed by an
unaccepted proposal.

The project profile (if present) can cap the menu — e.g., a
project profile declaring "risk tolerance: conservative" caps
at L1 even when the user's global preference is L2.

Record the selected level in the session journal as part of
the round's first entry.

## The loop (one cycle)

1. **Check for user input** since the last continuation (loop mode)
   or since the user's triggering message (round mode), when the
   client exposes that state. If a new message has arrived, stop the
   cycle and address it.
2. **Verify prerequisites.** `docs/todo.md` exists. Session
   journal for today exists or will be created. Working tree
   is clean (no uncommitted changes from an earlier task).
3. **Pick one bounded task** from `docs/todo.md`:
   - L0: ask the user.
   - L1: P0 first → P1 only if no open Draft/Placeholder
     blocks the path.
   - L2: P0 → P1 → in-progress implementation, tests, or docs
     governed by an Accepted/Partial proposal or no proposal.
   - L3: L2 plus bounded P2 work and proposal research/drafting.
     Proposal lifecycle changes still require explicit authority.
   - L4: L3 plus push authority after green gates.

   The `autonomous-planner` helper, when the client supports
   subagents, can inspect
   `docs/todo.md` + recent journals and returns a task
   recommendation with rationale.

   If `.ep-kit` exists and the task cites a proposal, resolve its configured
   directory and status first. Only Accepted/Partial implementation work is
   eligible. Implemented permits maintenance within the shipped contract;
   Superseded routes to its replacement; all other statuses are ineligible.

   Bounded means: you can finish, gate, and commit in one turn,
   you know what "done" looks like before starting, and no open
   design decisions block the path.
4. **Announce the pick** in today's session journal. One
   sentence: *Picked X because Y. Autonomy level: LN.* If
   multiple plausible tasks exist, list the ones passed over
   and why.
5. **Implement.** Log design calls you take without asking, in
   the journal, as you take them. Follow the governing
   principles — surgical changes, simplicity first.
6. **Gate.** Run the project's tests, linter, formatter, and
   any precommit checks. Record tool + command + result in the
   *Gates* block. Check exit codes where the tool reports
   warnings without non-zero exit.

   If the `cairn-review-phase` skill is available (cairn v0.2.0+), run
   it here: it orchestrates quality + security passes using
   whatever tools the project has.
7. **Commit locally when authorized.** Use the project's commit
   conventions and explain the *why* if non-obvious. If neither the
   request nor project policy authorizes commits, leave a verified
   working tree and report it. No pushes unless L4 and the user
   explicitly authorizes that external action.
8. **Decide: continue or stop.** See "When to stop," below.

## Round mode — after step 8

- Write the handoff summary at the end of the session journal.
  No continuation is scheduled.
- Return control to the user. The round is done.

## Loop mode — after step 8

- Check completed-cycle checkpoints (see below).
- If continuing: use only a continuation or resume mechanism the
  current client documents and exposes.
- If none exists: stop after the round and explain how the user can
  resume the loop.

## Hard rules (ALWAYS, every level)

- **Never push** unless you're at L4 *and* the user's
  instructions have explicitly authorised pushes.
- **Never force-push or rewrite** commits that have been
  pushed, or that touch others' work.
- **Never treat `Draft` or `Placeholder` as implementation
  authority.** A specific override must explicitly acknowledge the
  unaccepted status and authorize implementation before acceptance;
  choosing L2/L3/L4 is not such an override. Proposal lifecycle
  changes require separate explicit authority.
- **Never implement from Withdrawn or Rejected proposals.** Follow the
  replacement of a Superseded proposal. Treat Implemented as a shipped
  contract, not an open implementation queue.
- **Never bypass safety gates** (`--no-verify`, `--no-gpg-sign`,
  skipping precommit). If a gate fails, diagnose the underlying
  issue.
- **Never delete unfamiliar files or branches.** If you find
  something you don't recognise, leave it alone and note it in
  the journal.
- **Never send messages to chat platforms, ticket systems, or
  external services** without explicit authorisation. The
  session journal is the sanctioned status-update channel for
  autonomous work.
- **Never start a second task in the same cycle.** One task per
  cycle, period.

## Mid-cycle "ask anyway" cases

Even mid-round, some decisions deserve stopping to ask:

- Risk of data loss, shared-state corruption, or a hard-to-
  reverse action (schema migration, force-push, file deletion).
- The user's instructions could be interpreted two very
  different ways — pick one visibly and ask, don't silently
  choose.
- The change would touch files the user clearly intended to
  work on themselves (recent untracked edits, half-finished
  branches, etc.).
- The "bounded" task ballooned mid-implementation (30 lines →
  300 lines, 1 file → 5 files). Stop. Either re-scope or ask.

## When to stop the loop

Stop (do not continue or schedule a resume) if:

- **Blocker hit** beyond your authority — design decision,
  ambiguous failing gate, shared-state risk.
- **No bounded task available** — P1 cleared, P2 items are all
  "revisit if feedback complains" placeholders. Don't force a
  pick.
- **Cycle checkpoint reached** — see below.
- **User message arrived** mid-cycle.
- **Commit failed** (hook rejection, unresolvable compile
  error).

## Cycle checkpoints (loop mode only)

- **3 completed cycles in the session** (soft checkpoint): notify the
  user via the journal's handoff section, wait for approval to
  continue past the checkpoint. Don't auto-schedule another
  continuation.
- **5 completed cycles in the session** (hard stop): stop
  unconditionally. Silent prolific output without a user
  checkpoint erodes trust faster than fewer commits plus a
  clear handoff.

These are overridable: if the user explicitly asks for a long
loop ("run all night"), the checkpoint shifts to "every N
hours of wall time" or "until the punch list clears." Log the
override in the journal.

## Handoff summary

When the loop or round ends (for any reason), the last action
in the session journal must be a handoff block:

```markdown
## Handoff — <timestamp>

**Shipped this <round|loop>:** <commit SHAs + one-liners>.

**Autonomy level used:** <L0/L1/L2/L3/L4>.

**Stopped because:** <which stop criterion applied>.

**Queued if you want more:** <tasks considered next but not
picked — or "nothing obvious">.

**For your review:** <specific yes/no questions parked above>.
```

Terse, honest, no filler. That's what the user reads when
they get back.
