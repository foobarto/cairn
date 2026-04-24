# CLAUDE.md (cairn-flavored)

<!--
  This file is a *template* shipped by cairn. It gets copied into
  target projects as-is and then locally customised. If the target
  project has no CLAUDE.md, install.sh drops this in. If one
  exists, install.sh appends the "Session rhythm" section only —
  it does not overwrite.

  Equivalent files for other CLIs: AGENTS.md (Codex CLI),
  GEMINI.md (Gemini CLI). The substance is identical; rename as
  your CLI expects.
-->

Guidance for Claude Code (and other LLM assistants) working in
this repository. Kept deliberately short; project-specific detail
lives in `docs/`.

## Session rhythm

This project uses **cairn** to structure AI-agent sessions. Four
artefacts you should touch every working session:

| When                                       | Update                                                |
|--------------------------------------------|-------------------------------------------------------|
| Session start                              | Read today's `docs/sessions/<date>-<topic>.md` if any |
| As you work                                | Append to today's `docs/sessions/<date>-<topic>.md`   |
| When you notice something worth tracking   | `docs/todo.md` under the appropriate priority tier    |
| When you finish a feature                  | Every doc the change affects (see six-phase checklist)|

### Session journal (`docs/sessions/<date>-<topic>.md`)

A detailed runtime log. Write as you go, not retroactively. Per-
task entries use this sub-section structure:

```markdown
## <YYYY-MM-DD> — <task picked or topic>

**Task picked:** One-line description. Why this one.

**What shipped:**
- Concrete bullets. Reference file paths where useful.
- Scope that changed during implementation. Be honest.

**Design calls I made without you:**
- Decisions taken without waiting for user input.
- Include rationale — future you (or user) needs to judge it.

**Gates:**
- `<tool> <command>` — result. (`mix test` 42/0, `cargo test --all`,
  `pnpm typecheck`, etc.) Name the tool; "tests pass" is not enough.

**Skipped / not done this turn:**
- What you chose not to do, and why. Codex review skipped?
  E2E not run? Docs not regenerated? Flag it.

**Commit(s):** `<short-sha>` — `<commit message subject>`.
```

At the end of the file, park explicit yes/no questions for user
review:

```markdown
## Things I'd like your review / yes-or-no on when you're back

1. **Design shape.** Did we pick the right abstraction? Option A
   was `<X>`, I went with `<Y>`.
2. ...
```

Directory is tracked in git. Session logs are shared history, not
ephemeral scratch — future sessions read them to ground context.

### Rolling punch list (`docs/todo.md`)

Priority tiers:

- **P0 — actively wrong** (broken/lying/crashy). Rare; empty most
  of the time.
- **P1 — next cycle**. Bounded, owner-known, ready to pick up.
- **P2 — nice to have**. Real but deferrable.
- **P3 — thinking out loud**. Bigger items that might be worth a
  proposal later.

One bullet per item, prefixed with `[ ]` or `[x]`. Check off when
shipped; delete once it's been in CHANGELOG for a cycle.

Not in todo.md:

- Architectural decisions → see [ep-kit](#proposals-via-ep-kit).
- Shipped work → CHANGELOG.md.
- Autonomous-session review notes → session journal.
- Load-bearing invariants → this file or the project's
  architecture doc.

### Six-phase feature checklist

Every non-trivial feature moves through six phases in order:

1. **Spec** — proposal draft (see
   [`workflow/six-phase-checklist.md`](workflow/six-phase-checklist.md)
   for details).
2. **Plan** — proposal accepted, concrete implementation outline.
3. **Build** — code + adjacent docs.
4. **Test** — unit green + integration/E2E where applicable +
   manual-test checklist updated.
5. **Review** — self-review + second opinion (peer, codex,
   etc.).
6. **Ship** — commit + push, AND every doc the change affects.

Bug fixes, doc tweaks, and dep bumps collapse 1–2 (no proposal)
but still move through 3–6.

### Autonomous-round cadence

When running unattended (user said "continue autonomously" or
similar), follow the
[autonomous-round protocol](workflow/autonomous-round-protocol.md):

1. Pick ONE bounded task from `docs/todo.md`. Bounded = you can
   finish it, gate it, and commit it in one turn.
2. Log the task pick and the design calls you take without asking
   in the session journal.
3. Gate (tests, lint, format, build) before claiming done.
4. Commit locally. Do NOT push unless the user has explicitly
   authorised pushes in their instructions.
5. Schedule the next wakeup if there's more to do; otherwise
   stop and write the handoff summary.

Never:

- Start implementation work on a proposal still in Draft without
  the user's explicit green-light.
- Push to a remote without explicit authorisation.
- Force-push or rewrite commits visible to others.
- Start a new "round" if the current one hit an unresolved
  blocker — surface the blocker and wait.

## Proposals via ep-kit

Non-trivial design changes go through the **proposal** process
provided by [ep-kit](https://github.com/foobarto/ep-kit) (or
whatever the project named its proposal directory —
`docs/eps/`, `docs/rfcs/`, `docs/geps/`, …).

Touch a proposal when the change affects a public contract,
on-disk layout, CLI surface, load-bearing invariant, or any
"should we do X or Y?" question that isn't obvious from the code.
Skip it for bug fixes, contained refactors, and dep bumps.

## Coding discipline

These override the "move fast" impulse:

1. **Think before coding.** State assumptions, surface tradeoffs.
   When a request has multiple interpretations, pick one visibly —
   don't silently choose.
2. **Simplicity first.** Minimum code that solves the problem. No
   speculative abstractions, no unrequested configurability, no
   defensive handling for impossible scenarios.
3. **Surgical changes.** Touch only what you must. Preserve
   existing style. Don't rename / reformat / "improve" unrelated
   sections while passing through.
4. **Goal-driven execution.** Define success concretely before
   implementing. Loop until the test passes / the diff is closed,
   not until you feel done.

## Project-specific notes

<!--
  Add project-specific guidance below this line: architecture
  map pointers, invariants, common commands, env setup, known
  gotchas. Keep it short — depth lives in docs/.
-->

### Common commands

| Action  | Command                          |
|---------|----------------------------------|
| Setup   | `<your build tool here>`         |
| Tests   | `<your test runner here>`        |
| Gates   | `<your precommit command here>`  |

### Load-bearing invariants

<!-- Replace with your project's top 3-5 invariants. -->

- ...
- ...
- ...
