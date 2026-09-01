---
name: cairn-session-log
description: Create or update a Cairn session journal under docs/sessions/ when the user requests session logging or an active Cairn round reaches a logging checkpoint. Do not rewrite journals into summaries or create logs for unrelated ordinary work.
metadata:
  version: "0.3.0"
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
- During an explicitly active Cairn session, a natural seam has happened
  (commit landed, wave of work closed, or the user asked for a checkpoint).
- You're about to start an autonomous round and need to make
  sure today's log file exists before picking a task.
- During an explicitly active Cairn session, an adopted non-trivial design
  decision needs a concise project-facing rationale.

## Do NOT use for

- The user asking you to write a proposal (→ use Strata's
  `ep-kit` proposal-authoring skill).
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

Session journals are contemporaneous project records, not transcripts. Append
concise facts to the file:

- When you pick a task (start of a new `##` section).
- When you take a design decision without asking the user.
- When you run a gate (tests, lint, format, build).
- When you commit (include the SHA).
- When you notice something worth flagging for user review.
- When the round ends (write the handoff summary).

Retroactive session reconstruction often loses reliable scope and evidence.
If reconstruction is necessary, label it and record only facts supported by
the available artifacts.

## Publication hygiene

Treat repository journals as shared, potentially public artifacts. Record
adopted project-relevant decisions, concrete evidence, checks, scope changes,
and useful unresolved questions. Do not persist credentials, tokens, private
paths or host details, personal profiles, unrelated user context, transcript-
like chain of thought, scratch methodology, or exploratory deliberation that
was not adopted. Summarize the professional rationale needed by future
contributors instead.

## Section shape

For each task/topic during the session, add a `##` block with
these sub-sections (in order). Skip sub-sections that don't
apply, but don't rename them — the consistency is what makes
the log skimmable.

```markdown
## <HH:MM or seam tag> — <task picked or topic>

**Task picked:** <one-line description>. <Why this one>.

**Proposal:** <stable reference such as `EP-0017`, or `None`>.

**What shipped:**

- <concrete bullet>; reference `path/to/file` or `file:line`.
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

**Proposal reconciliation:** <`No proposal changes required`, or the assessed
status/conformance work and any authorized validator result>.
```

## Architectural-drift sensor

The `Design calls I made without you` section is for implementation-local,
reversible calls that preserve public behavior, persisted representation,
trust boundaries, load-bearing invariants, and Accepted/Partial proposals.

If a discovery crosses any of those boundaries, materially constrains future
implementations, or conflicts with the governing proposal:

1. record the discovery and evidence without duplicating architectural
   alternatives or a Decision Log;
2. stop implementation at that decision boundary;
3. if `.ep-kit` exists, invoke `cairn-strata-interop` and Strata's current
   governance workflow; otherwise ask how the project records durable design;
4. resume only when the durable decision has implementation authority.

If the sibling skill is unavailable, read `.ep-kit` directly as its public
`key=value` contract (`dir` defaults to `docs/eps`) and follow the installed
governance workflow. Stop on malformed configuration instead of guessing.

Use Strata's stable references such as `EP-0017` and `EP-0017 D3`, including
when the project calls proposals RFCs, GEPs, or something else.

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
2. Drop a short `README.md` inside it documenting the filename convention and
   the section shape embedded in this skill.
3. Create today's session file using the template shape above.

Create these files only when the user explicitly requested Cairn logging or an
authorized Cairn round is active. Otherwise, a missing directory means stop and
offer initialization rather than silently adopting Cairn.

## Working with the user on an active session

- A preference expressed while using this skill is not permission to update
  the client's separate memory store. Do so only on an explicit memory-update
  request or when standing instructions clearly authorize it.
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
