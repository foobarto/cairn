---
name: cairn-close-session
description: Close an active Cairn work session when the user asks to wrap up or the current Cairn workflow reaches its explicit close step. Finalize the journal and return an evidence-based handoff without publishing or updating memory unless authorized.
metadata:
  version: "0.3.0"
---

# cairn: Close-session skill

Guide the agent through the **end-of-session ritual**. The goal
is to leave the project in a state where a future session (human
or agent) can pick up without context loss.

## When to use this skill

- User says "that's enough for today" / "let's wrap up" / "stop
  here" / "close out" / similar.
- An active Cairn workflow reaches an explicit close step after
  the scoped work is complete.
- Before a long scheduled break (weekend, vacation).
- Before a dramatic context-clearing operation (`/clear`, new
  conversation).

## Do NOT use for

- Brief pauses mid-task. Use the `cairn-session-log` skill to append a
  short update, don't run the full close-out.
- Ending an autonomous round. The `cairn-autonomous-round` skill's
  handoff block is sufficient; `cairn-close-session` is heavier.

## The ritual (in order)

### 1. Take stock

Read:

- `git status --short --branch` — what is modified or untracked?
- `git log <main>..HEAD --oneline` — what's unpushed?
- Today's session journal — is its *Things I'd like your review*
  section up to date with the session's actual open questions?
- `docs/todo.md` — anything the session revealed that should be
  on the punch list but isn't?
- If `.ep-kit` exists, resolve it through `cairn-strata-interop` and list every
  proposal reference used in the session.

### 2. Account for the working tree

Leaving uncommitted changes across a session break is usually
fine — but flag what's there. Options:

- **Commit** only when the user request or project policy authorizes it.
- **Stash** only when the user asks to pause work that way.
- **Discard** only with explicit user confirmation.

Do not push unless the user's instructions authorise it.

### 3. Update the punch list

- Items shipped this session: move to the *Shipped this cycle*
  block at the bottom, check `[x]`.
- Items noticed during the session but not addressed: add to P1
  / P2 / P3 per urgency.
- Items that turned out to be wrong / superseded: delete, with
  a one-line note in the journal.

### 4. Finalise today's session journal

Write (or check) these sections:

- One closing `##` heading: `## Closing — <what shipped>`.
  Bullet list of the session's deliverables with SHAs.
- `## Skipped / not done this session` — honest list of what
  was deferred, with rationale.
- `## Things I'd like your review / yes-or-no on when you're
  back` — the explicit-questions block. Only questions that
  genuinely need user input before the next session.
- If the session included autonomous rounds, confirm each
  round's handoff block is intact — don't delete them during
  consolidation.

### 5. Offer profile updates when authorized

Two profiles — user (global, personal) and project (per-project,
shared):

- **User profile** (via `cairn-build-user-profile` skill): update
  only when the user explicitly asks to record a durable preference
  or has already authorized profile synthesis. Do not infer consent
  from ordinary conversation.
- **Project profile** (via `cairn-build-project-profile` skill):
  If a session settled a project-wide stance (risk tolerance,
  security posture, quality bar, contribution norm), update
  `docs/project-profile.md` only when the close request or standing project
  policy authorizes that durable change.

If the client has a separate memory system, do not update it unless the
user explicitly authorizes memory changes. A Cairn profile update does
not imply permission to change another memory store.

Do NOT save:

- Task-ephemeral state (journal carries it).
- Architectural facts derivable from the code (the code carries
  it).
- Hot opinions without a *why*.
- Frustration, impatience, or emotional reactions.

### 6. Reconcile referenced proposals

For each proposal referenced this session, use `cairn-strata-interop` to assess
status truthfulness, partial/full delivery, conformance conflicts,
architectural discoveries, and todo items made stale by supersession,
withdrawal, or rejection. Most sessions should record `No proposal changes
required.`

If that sibling skill is unavailable, read `.ep-kit` directly as its public
`key=value` contract (`dir` defaults to `docs/eps`; `validator` is optional),
follow the installed lifecycle, and perform the same read-only reconciliation.
Stop on malformed configuration rather than guessing.

Do not mutate proposal lifecycle metadata without explicit project authority.
When an authorized mutation occurs, update required history and release
metadata through Strata, then run its configured validator and record the exact
result.

### 7. Commit doc changes when authorized

When commit authority exists, a `docs(session): close out <date>` commit is a
reasonable convention. Include:

- The updated session journal.
- Any `docs/todo.md` changes.
- Any CHANGELOG entries for shipped work.

### 8. Write the chat-side handoff

The final response in chat is a compact summary of what the user
will see when they next open the project. Shape:

```markdown
**Session closing — <date>.**

Shipped: <bullet list with SHAs>.

Open questions for your review (in the journal): <numbered list
of the yes/no questions>.

Not done / deferred: <bullet list>.

Next session starting point: <one sentence>.
```

Keep it under ~200 words. The full detail lives in the session
journal; chat is just the pointer.

## Edge cases

- **Session had no substantive output.** Write the journal
  entry anyway, short. Future sessions benefit from knowing a
  session happened and what was discussed, even if no code
  shipped.
- **Session was entirely planning / discussion.** A
  `docs(session): <topic> planning` commit is fine; no code
  changes needed.
- **User wants to dramatically pivot (same session).** Don't
  close; the session is continuing. Use the `cairn-session-log` skill
  to write a pivot marker and keep going.
- **Session ended because of a blocker.** The handoff should
  explicitly call out the blocker + what the user needs to
  unblock it. Don't hide it at the bottom of the
  open-questions list.

## Remind the user of `/compact` if applicable

Many CLIs support `/compact` or similar context-reduction
operations. At session close, a gentle reminder:

> "Session closed cleanly. If you're continuing later, `/compact`
> is a good next step to free context — the journal + punch list
> carry everything the next session needs."

Only suggest it if your CLI actually has it. Don't invent one.
