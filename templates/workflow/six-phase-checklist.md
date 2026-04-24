# Six-phase feature checklist

Every non-trivial feature moves through these six phases, in
order. Skipping phases is how you get to a half-shipped feature
three times in a row.

| # | Phase      | Artefact                                            |
|---|------------|-----------------------------------------------------|
| 1 | **Spec**   | Proposal draft (via ep-kit, in `docs/eps/` or the equivalent) |
| 2 | **Plan**   | Proposal accepted; concrete implementation outline  |
| 3 | **Build**  | Code changes + any doc-adjacent updates             |
| 4 | **Test**   | Unit green + E2E/manual where applicable            |
| 5 | **Review** | Self-review (see below) + second opinion            |
| 6 | **Ship**   | Commit + push, AND every doc the change affects     |

Bug fixes, doc tweaks, and dep bumps collapse phases 1–2 (no
proposal) but still pass through 3–6.

---

## Phase 1 — Spec

Write a proposal before writing code when the change:

- Affects a public contract (API, CLI surface, on-disk layout).
- Touches a load-bearing invariant.
- Reverses or extends a prior proposal.
- Answers a "should we do X or Y?" question that isn't obvious
  from the code.

For bug fixes, contained refactors, dep bumps — skip the
proposal, go straight to phase 3. Trust the commit message + PR
description to carry the rationale.

## Phase 2 — Plan

Proposal is `Accepted`. Outline the implementation before
opening the first file:

1. Modules/files that will change.
2. Tests you'll add or update.
3. Docs that will need updating at phase 6.
4. A rough sequence of commits (not a mandate — a sketch).

This is usually a 5-minute exercise captured in the session
journal, not a separate document.

## Phase 3 — Build

Code. Follow the project's coding discipline (usually pinned in
`CLAUDE.md`). Keep commits surgical — every changed line should
trace to the user's request.

Touch adjacent docs **in the same commit** where it's cheap:
function docstrings, README examples, schema diagrams. Save the
sweeping doc pass for phase 6.

## Phase 4 — Test

- **Unit tests** for the pure logic you changed.
- **Integration / E2E** if the change crosses module boundaries
  or user-facing behaviour.
- **Manual test checklist** update if the project has one.

Run the tests. Record results in the session journal's *Gates*
block. Do not claim done before this.

## Phase 5 — Review

Two reviewers, in order:

1. **Self-review.** Read the diff as if you're seeing it for the
   first time. Look for:
   - Scope creep (unrelated changes sneaking in).
   - Dead variables / unused imports / stale comments.
   - Comments explaining *what* instead of *why*.
   - Missing docstrings on public API.
   - Gate failures you glossed over.
2. **Second opinion.** Another person (or agent like codex,
   GEP-style reviewer, etc.). The goal is catching what you
   couldn't see yourself — assumptions you made, edge cases you
   missed, phrasing that reads differently to a fresh eye.

Apply must-fix feedback inline. Log nice-to-haves to the session
journal.

## Phase 6 — Ship

Commit + push if authorised. **Then** do the doc pass. Consider
updating every one of these:

- `CHANGELOG.md` — what shipped, always.
- `README.md` — if the user-facing pitch or install story
  changed.
- The project's architecture / design doc — if module map,
  invariants, or tech stack changed.
- Proposal status — flip `Accepted → Implemented` when the
  implementation lands.
- `docs/todo.md` — cross off whatever this change addressed.
- Manual test checklist — if a UI surface was added.
- Knowledge-graph notes — if you uncovered a gotcha, surprising
  call chain, or load-bearing invariant.

"Ship" is not done until the docs that lie about the code have
been updated. Stale docs are technical debt that compounds.

---

## Anti-patterns to catch yourself doing

| Signal | What it usually means |
|---|---|
| "I'll document it later." | Phase 6 will be skipped. Do it now. |
| "The tests will catch it." | Phase 4 was rushed. Add tests *before* the implementation settles. |
| "I didn't need a proposal for this." | Phase 1 was skipped. If the change touches a contract, pause and write one. |
| "Let me just improve this adjacent bit." | Scope creep. Note it in `docs/todo.md` and move on. |
| Shipping without second opinion | Phase 5 half-done. For trivial changes it's OK; flag it honestly in the session journal. |
