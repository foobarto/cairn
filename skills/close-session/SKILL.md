---
name: cairn-close-session
version: 0.1.0
description: Use when a session is ending — the user says "that's enough for today", "let's wrap up", "stop here", "close the session"; or when the agent itself judges the session is at a natural stopping point and wants to leave a clean handoff. Produces the end-of-session ritual — final journal entry, commit-status snapshot, handoff summary with concrete SHAs and explicit yes/no questions for the next session, and optional memory updates for durable preferences revealed during the session.
---

# cairn: Close-session skill

Guide the agent through the **end-of-session ritual**. The goal
is to leave the project in a state where a future session (human
or agent) can pick up without context loss.

## When to use this skill

- User says "that's enough for today" / "let's wrap up" / "stop
  here" / "close out" / similar.
- The agent judges the session has reached a natural stopping
  point (major feature shipped, wave of work closed, context
  exhausted) and wants to leave a clean handoff.
- Before a long scheduled break (weekend, vacation).
- Before a dramatic context-clearing operation (`/clear`, new
  conversation).

## Do NOT use for

- Brief pauses mid-task. Use the session-log skill to append a
  short update, don't run the full close-out.
- Ending an autonomous round. The autonomous-round skill's
  handoff block is sufficient; close-session is heavier.

## The ritual (in order)

### 1. Take stock

Read:

- `git status -uno` — what's uncommitted?
- `git log <main>..HEAD --oneline` — what's unpushed?
- Today's session journal — is its *Things I'd like your review*
  section up to date with the session's actual open questions?
- `docs/todo.md` — anything the session revealed that should be
  on the punch list but isn't?

### 2. Tidy the working tree

Leaving uncommitted changes across a session break is usually
fine — but flag what's there. Options:

- **Commit** if the diff is substantial and meaningful.
- **Stash** with a descriptive label if the work is paused
  rather than done.
- **Discard** only with explicit user confirmation — never
  autonomous.

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

### 5. Save durable memory (if your CLI supports it)

Save as memory:

- **User preferences** revealed during the session (coding
  style, tool choices, review rituals, keybinding preferences,
  licensing defaults).
- **Feedback on the agent's approach** — things the user
  corrected or confirmed, with the *why*.
- **Project-specific gotchas** that would silently mis-advise a
  future session.

Do NOT save:

- Task-ephemeral state (journal carries it).
- Architectural facts derivable from the code (the code carries
  it).
- Hot opinions without a *why*.

### 6. Commit the doc changes

A `docs(session): close out <date>` commit is standard. Include:

- The updated session journal.
- Any `docs/todo.md` changes.
- Any CHANGELOG entries for shipped work.

### 7. Write the chat-side handoff

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
  close; the session is continuing. Use the session-log skill
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
