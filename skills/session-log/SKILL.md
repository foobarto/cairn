---
name: cairn-session-log
version: 0.1.0
description: Use when the user wants to start, append to, or close a cairn session log (the detailed runtime journal under `docs/sessions/<date>-<topic>.md`). Triggers on phrases like "open today's session log", "append to the session journal", "log this decision", "close the session", or any pause at a natural commit seam where the session journal should capture what just happened. Also use when starting an autonomous round (create a new log file for this session before picking a task).
---

# cairn: Session log skill

Guide the agent through creating, appending to, or closing a
**session journal** under `docs/sessions/<date>-<topic>.md`.

Session journals are cairn's detailed runtime log: per-task
entries with standardized sub-sections, honest about shortcuts,
with concrete SHAs and yes/no questions parked at the end. They
sit between git history (too terse) and proposals (too formal).

## When to use this skill

- User says "open the session log", "start a new session", "log
  this", "append to today's log", "close out the session", etc.
- A natural commit seam has just happened (commit landed, wave
  of work closed, user asked for a checkpoint).
- You're about to start an autonomous round and need to make
  sure today's log file exists before picking a task.
- You're about to take a non-trivial design decision without
  asking the user — the decision should land in the journal in
  the same turn it's made.

## Do NOT use for

- The user asking you to write a proposal (→ use the proposal
  skill from ep-kit).
- Updating the rolling punch list (`docs/todo.md`) — that's a
  different artefact with different conventions.
- Retroactive session reconstruction from git log. Session
  journals are written as you go; a retroactive one is better
  than nothing but flag it as retroactive.

## Where the log lives

Resolve, in this order:

1. **`CAIRN_SESSIONS_DIR` environment variable** — if set, use it.
2. **`docs/sessions/` in the project root** — the cairn default.
   If the directory doesn't exist, create it on first write.

Filename: `<YYYY-MM-DD>-<topic-slug>.md` where the topic slug is
a 2-4 word kebab-case description of the session's main focus
(e.g. `kanban-ux`, `security-sweep`, `autonomous-round`). When
today's session opens fresh, the agent chooses the slug from
the user's opening prompt; for appending to an existing file,
reuse whatever is already there.

If today's date already has a session file and the current task
fits its existing topic, append. If the current task is clearly a
different topic (user pivoted), open a new file with a distinct
slug. When in doubt, append to the existing file and mark the
pivot with a clear `##` heading.

## Write-as-you-go, not retroactively

Session journals are real-time narrative. Append to the file:

- When you pick a task (start of a new `##` section).
- When you take a design decision without asking the user.
- When you run a gate (tests, lint, format, build).
- When you commit (include the SHA).
- When you notice something worth flagging for user review.
- When the round ends (write the handoff summary).

Retroactive session reconstruction misses the decision moment —
*what you considered and rejected*. That's the most valuable
part of the log.

## Section shape

For each task/topic during the session, add a `##` block with
these sub-sections (in order). Skip sub-sections that don't
apply, but don't rename them — the consistency is what makes
the log skimmable.

```markdown
## <HH:MM or seam tag> — <task picked or topic>

**Task picked:** <one-line description>. <Why this one>.

**What shipped:**

- <concrete bullet>; reference [file path](path) or `file:line`.
- <scope that changed mid-implementation — be honest>.

**Design calls I made without you:**

- **<short name>.** <What was decided>. <Rationale — why this
  beat the alternatives>.

**Gates:**

- `<tool> <command>` — <result>. Name the tool; "tests pass" is
  not enough. Check exit codes where the tool reports warnings
  without non-zero exit.

**Skipped / not done this turn:**

- <What you chose not to do, and why>.

**Commit(s):** `<short-sha>` — `<commit subject>`.
```

## End-of-session handoff

At the end of a session (last action before stopping or before
the user is expected to return), the file must end with:

```markdown
## Things I'd like your review / yes-or-no on when you're back

1. **<short name>.** <Specific question with the alternative you
   considered.>
2. ...
```

Only include questions that genuinely need user input before the
next round. "Let me know if you see any issues" is not a
question. "Should X live in module A or B? I picked A because
<reason>." is.

## Bootstrapping if nothing exists

If `docs/sessions/` doesn't exist:

1. Create the directory.
2. Drop a short `README.md` inside it linking to the cairn
   repo's `templates/session-template.md`.
3. Create today's session file using the template shape above.

Don't silently treat the missing directory as a signal that the
project doesn't use cairn — ask the user if they want cairn
initialised, or defer writing until they confirm.

## Working with the user on an active session

- When the user tells you they value the session log format
  explicitly — save that as a feedback memory if your CLI
  supports it, so future sessions maintain the discipline
  without being reminded.
- When the user pivots topic mid-session, either (a) rename the
  existing file's topic slug if the new topic has fully
  replaced the old, or (b) create a second file for today. (a)
  is cleaner when the pivot is early; (b) is cleaner when both
  topics had real work done.
- When the user asks you to "summarize what happened today",
  they want a reply, not an edit — don't rewrite the journal
  into a summary. Return the summary in chat.

## Commit the journal with the session's work

When committing a session's work, include the updated session
journal in the same commit (or an adjacent commit). Never leave
the journal behind while pushing the code; the journal is the
*why* that the code commit should be referenced against.

A session commit that only updates the journal (no code) is
fine when the session was all planning/discussion. Label it as
such in the commit subject: `docs(session): <topic>` or similar.
