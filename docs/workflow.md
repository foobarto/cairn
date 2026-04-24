# The cairn workflow

This is the full picture of how cairn organizes AI-assisted
software work. It's descriptive (what the artefacts are and how
they relate) rather than prescriptive — you'll adapt pieces to
your project.

## The artefacts

Four documents carry the workflow state. They're all markdown,
all tracked in git, all in `docs/` by default.

```
your-project/
├── CLAUDE.md                     (or AGENTS.md / GEMINI.md — rename per your CLI)
└── docs/
    ├── sessions/                 Detailed runtime log, per-session
    │   ├── 2026-04-24-kanban-ux.md
    │   └── 2026-04-25-security-sweep.md
    ├── todo.md                   Rolling punch list (P0-P3 tiers)
    ├── workflow/
    │   ├── six-phase-checklist.md
    │   └── autonomous-round-protocol.md
    └── eps/                      (optional — ep-kit territory)
        ├── 0001-ep-purpose-and-guidelines.md
        └── 0002-...
```

Each artefact has a specific job. They don't overlap.

### CLAUDE.md / AGENTS.md / GEMINI.md

Project-level agent instructions. Short (≤ 250 lines is a good
target), authoritative. Carries:

- The session rhythm (pointer to the session journal convention).
- The six-phase checklist (pointer to the full doc).
- The autonomous-round protocol (pointer).
- Project-specific notes: common commands, load-bearing
  invariants, local idiosyncrasies, links to architecture.

This file is the first thing every session reads. It's the
"constitution" — don't let it sprawl.

### docs/sessions/<date>-<topic>.md

The **session journal**. Detailed runtime log, written as you
go. Per-task entries with standardized sub-sections:

- *Task picked* — one sentence on why this task.
- *What shipped* — concrete bullets, file paths, scope that
  moved during implementation.
- *Design calls I made without you* — explicit decisions taken
  autonomously, each with rationale.
- *Gates* — named tools + commands + results.
- *Skipped / not done this turn* — honest about shortcuts.
- *Commit(s)* — SHAs.

End of file: explicit *Things I'd like your review* block with
yes/no questions.

Why detailed: chat contexts rot, commit messages are terse,
proposals are formal. The session journal captures *what was
considered and rejected* — the most valuable decision-moment
detail.

Why tracked in git: journals are shared history. Future
sessions (or colleagues) read them to ground context. Ephemeral
scratch goes elsewhere.

### docs/todo.md

The **rolling punch list**. Priority tiers:

| Tier | Meaning                                          |
|------|--------------------------------------------------|
| P0   | Actively wrong (broken/lying/crashy). Rare.      |
| P1   | Next cycle — bounded, ready to pick up.          |
| P2   | Nice to have. Revisit later.                     |
| P3   | Thinking out loud. Might become proposals.       |

At the bottom: *Shipped this cycle* — items completed since the
last version cut. At release time, roll these into CHANGELOG
and clear.

Not in todo.md: architectural decisions (→ proposal), shipped
work (→ CHANGELOG), autonomous-session review notes (→ journal).

### docs/workflow/six-phase-checklist.md

Reference for the six-phase feature development cycle: **Spec →
Plan → Build → Test → Review → Ship**. Ship means the code AND
every doc that should reflect the change have been updated in
the same session.

### docs/workflow/autonomous-round-protocol.md

Reference for unattended work. Covers: how to pick a task, hard
rules (no pushes, no force-pushes, no Draft-proposal
implementation), and stop criteria (blocker, empty pool, commit
cap, user message arrived).

### docs/eps/ (optional, via ep-kit)

Proposals with decision logs. cairn's templates reference them;
ep-kit provides them. The two are designed to work together.

## The rhythm

A typical session:

1. **Read.** Session journal for today (if any) + any
   outstanding open questions from recent journals.
2. **Align.** User states the goal. Agent re-states it in its
   own words if there's any ambiguity.
3. **Work.** Implement. Run gates. Commit.
4. **Log.** Append to the session journal after each natural
   seam (task done, commit landed, gate run).
5. **Decide.** Next task from punch list? Pause for user input?
   End of session?
6. **Close.** If ending: punch-list update, handoff summary,
   durable memory saved.

Autonomous rounds slot into step 3–5 and are governed by the
protocol doc.

## Why these four artefacts

Each plays a role the others can't:

| Artefact         | Time scope       | Audience             | Updated when          |
|------------------|------------------|----------------------|-----------------------|
| CLAUDE.md        | Project lifetime | Every session starts | Rarely; stable rules  |
| Proposals        | Per-decision     | Long-form reviewers  | Once, then append-only|
| Session journal  | Per session      | Next session + user  | Continuously during   |
| `docs/todo.md`   | Per sprint/cycle | Current + near-next  | End of each task      |

Together they give a complete answer to "why is this code the
way it is?" at four zoom levels — project, decision, session,
task.

## Adapting to your project

- **Different naming.** Call proposals RFCs, ADRs, or whatever
  your team uses. cairn's templates reference ep-kit's "EP"
  naming but the shape is portable.
- **Different layout.** If your project already has `docs/`
  conventions, fit in around them. Don't force `docs/sessions/`
  if `notes/sessions/` is more natural.
- **Single-player vs team.** cairn was extracted from a
  single-maintainer project. For teams, treat the session
  journal as "what I did" — each contributor writes their own;
  they interleave by date filename.
- **Language/framework.** None of this is language-specific.
  cairn's templates don't mention any build tool, test runner,
  or framework. The project's `CLAUDE.md` fills those in.

## What cairn doesn't solve

- **Test writing.** Your test framework is yours.
- **Code review tooling.** Codex, Greptile, in-person — use
  whatever. cairn's journal just expects you to record that
  review happened in the *Gates* or a dedicated sub-section.
- **Project management.** Punch list ≠ ticket system. For
  cross-team work, your team's PM tool is the source of truth;
  cairn's `docs/todo.md` is a local scratchpad.
- **Knowledge graph / architecture map.** cairn's templates
  reference "knowledge graph notes" as a hook point. Providing
  a graphing tool is out of scope — use graphify, Sourcegraph,
  an LLM-generated summary, or whatever you prefer.
