# Six-phase feature checklist

Every non-trivial feature moves through these six phases, in
order. Skipping phases is how you get to a half-shipped feature
three times in a row.

**Read first:**
[docs/workflow/governing-principles.md](governing-principles.md).
The six phases are *when*; the four principles are *how within
each phase*. Ticking phases mechanically without applying the
principles is the failure mode this doc is designed to prevent.

| # | Phase      | Artefact                                            |
|---|------------|-----------------------------------------------------|
| 1 | **Spec**   | Change classification; proposal only for a durable decision |
| 2 | **Plan**   | Accepted/Partial proposal when required; concrete implementation outline |
| 3 | **Build**  | Code changes + any doc-adjacent updates             |
| 4 | **Test**   | Unit green + E2E/manual where applicable            |
| 5 | **Review** | Self-review (see below) + second opinion            |
| 6 | **Ship**   | Verified handoff; authorized commit/push; affected docs |

Bug fixes, doc tweaks, and dep bumps collapse phases 1–2 (no
proposal) but still pass through 3–6.

---

## Phase 1 — Spec

Classify the change before writing code. Use the project's proposal system
when the change:

- Affects a public contract (API, CLI surface, on-disk layout).
- Touches a load-bearing invariant.
- Reverses or extends a prior proposal.
- Answers a "should we do X or Y?" question that isn't obvious
  from the code.

For bug fixes, contained refactors, and dependency bumps that preserve durable
contracts, skip the proposal and go straight to phase 3. Search existing
proposals before creating a new design artifact. Draft/Placeholder never
authorizes implementation without a specific acknowledged override.

When `.ep-kit` exists, read its public config to resolve the proposal directory
and validator; do not assume `docs/eps/`. Strata owns proposal structure,
Decision Logs, relationships, and lifecycle. Cairn records only work state and
stable references.

## Phase 2 — Plan

When a proposal is required, it is `Accepted` or `Partial`. Outline the
implementation before opening the first file:

1. Modules/files that will change.
2. Tests you'll add or update.
3. Docs that will need updating at phase 6.
4. A rough sequence of commits (not a mandate — a sketch).

This is usually a 5-minute exercise captured in the session
journal, not a separate document.

## Phase 3 — Build

Code. Follow the project's coding discipline in its agent-instructions file.
Keep commits surgical — every changed line should
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

Three passes, in order. **Quality and security consideration are both
mandatory**; second opinion is expected on non-trivial changes
but optional for small diffs.

### 5a. Self-review

Read the diff as if you're seeing it for the first time. Look
for:

- Scope creep (unrelated changes sneaking in).
- Dead variables / unused imports / stale comments.
- Comments explaining *what* instead of *why*.
- Missing docstrings on public API.
- Gate failures you glossed over.

### 5b. Quality pass (mandatory)

Run the project's canonical gate (`mix precommit`, `pnpm run
check`, `cargo clippy --all-targets`, `just check`, etc.) and
any language-specific linter detected for the changed files.

Record tool + command + result in the session journal:

```markdown
**Quality:**
- `mix precommit` — clean (exit 0).
- `mix credo --strict` — 0 issues (exit 0 explicitly verified).
```

### 5c. Proportional security pass (mandatory)

Never skip security consideration. Choose the depth that matches the change:

- **Tool-based:** Run configured, relevant static analysis when available and
  authorized.
- **Manual:** Read the diff against applicable trust boundaries, secret
  handling, authentication/authorization, input and path handling, and
  dependency risk. A docs-only change may make most categories inapplicable;
  state that rather than performing review theater.

Record in the journal. Any high/critical finding is a blocker
— do not proceed to phase 6 until resolved.

### 5d. Second opinion (optional for small changes)

For non-trivial changes (public contracts, persistent formats, trust
boundaries, multi-component behavior): dispatch an available independent
reviewer with a bounded definition of done.

For small diffs (bug fixes under ~50 lines, doc changes, dep
bumps): skip and note the skip with reason.

Apply must-fix feedback inline. Log nice-to-haves to the
session journal.

### 5e. EP conformance (when applicable)

If the change claims to implement an Accepted/Partial proposal, separately
compare it with the proposal's Goals, Non-goals, Design constraints, and
relevant Decision Log entries. A technically correct diff that conflicts with
its governing proposal is a blocker. Record the stable proposal/decision
references, not a duplicate Decision Log.

### If cairn's `cairn-review-phase` skill is available

It orchestrates 5b-5d automatically: tool detection, plan
proposal, invocation of the `review-runner` sub-agent, summary
into the journal. Use it as the default entry point for phase
5 instead of driving these passes manually.

## Phase 6 — Ship

Complete the doc pass and create a verified handoff. Commit or push only when
the request or project policy authorizes it. Consider
updating every one of these:

- `CHANGELOG.md` — what shipped, always.
- `README.md` — if the user-facing pitch or install story
  changed.
- The project's architecture / design doc — if module map,
  invariants, or tech stack changed.
- Proposal lifecycle — run the proposal system's completion
  checkpoint. For Strata, compare every goal and rollout obligation,
  distinguish `Partial` from `Implemented`, update history/index and
  `implemented-in` where required, validate the full proposal set,
  and mutate status only with explicit authority.
- For every proposal referenced this session, also check for stale todo items,
  supersession/rejection routing, and architectural discoveries that must leave
  the journal for proposal governance. Most sessions should record `No
  proposal changes required.`
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
