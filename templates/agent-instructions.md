# Agent instructions (cairn-flavored)

<!--
  This file is a *template* shipped by cairn. It gets copied into
  target projects as-is and then locally customised. If the target
  project has no selected agent-instructions file, install.sh drops
  this in. If one
  already exists, install.sh leaves it untouched (reports it
  "skipped"). Use --agents-file to select AGENTS.md, CLAUDE.md,
  GEMINI.md, or another project-relative path your client documents.
-->

Guidance for AI agents working in this repository. Kept deliberately
short; project-specific detail
lives in `docs/`.

## Governing principles (the backbone)

Four principles, adapted from
[Karpathy's guidelines](https://karpathy.bearblog.dev/dev/),
that override the "move fast" impulse. Full text at
[docs/workflow/governing-principles.md](docs/workflow/governing-principles.md);
every other artefact in this repo is shaped to make following
them easier.

1. **Think before coding.** State assumptions, surface
   tradeoffs. When a request has multiple interpretations,
   pick one visibly — don't silently choose.
2. **Simplicity first.** Minimum that solves the problem.
   No speculative abstractions, no unrequested configurability,
   no defensive handling for impossible scenarios.
3. **Surgical changes.** Touch only what you must. Preserve
   existing style. Every changed line should trace to the
   user's request.
4. **Goal-driven execution.** Define success concretely before
   implementing. Loop until the test passes / the diff is
   closed, not until you *feel* done.

These are load-bearing. The session rhythm, six-phase
checklist, autonomous protocol, and review phase are all
shapes that make these four easier to honour. When any shape
conflicts with a principle, the principle wins.

## Session rhythm

This project uses **cairn** to structure AI-agent sessions.
Artefacts you should touch every working session:

| When                                       | Update                                                |
|--------------------------------------------|-------------------------------------------------------|
| Session start                              | Read today's `docs/sessions/<date>-<topic>.md` if any + `docs/project-profile.md` for stance; read a user profile only when its configured path is available and authorized |
| As you work                                | Append to today's `docs/sessions/<date>-<topic>.md`   |
| When you notice something worth tracking   | `docs/todo.md` under the appropriate priority tier    |
| When a project stance settles and its update is authorized | `docs/project-profile.md` (project-wide) |
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
- What you chose not to do, and why. Independent review skipped?
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

- Architectural decisions → see [Strata](#proposals-via-strata).
- Shipped work → CHANGELOG.md.
- Autonomous-session review notes → session journal.
- Load-bearing invariants → this file or the project's
  architecture doc.

### Six-phase feature checklist

Every non-trivial feature moves through six phases in order:

1. **Spec** — classify the change; use an accepted proposal when a durable
   design decision requires one (see
   [`docs/workflow/six-phase-checklist.md`](docs/workflow/six-phase-checklist.md)
   for details).
2. **Plan** — proposal accepted, concrete implementation outline.
3. **Build** — code + adjacent docs.
4. **Test** — unit green + integration/E2E where applicable +
   manual-test checklist updated.
5. **Review** — self-review + second opinion (peer, codex,
   etc.).
6. **Ship** — verified handoff, authorized commit/push, AND every doc the
   change affects.

Bug fixes, doc tweaks, and dep bumps collapse 1–2 (no proposal)
but still move through 3–6.

### Autonomous work — round vs loop

When running unattended, pick the shape that matches the ask:

- **Round** — one bounded cycle, stop when done. Triggered by
  "do one task from the punch list", "finish the Kanban refactor
  autonomously", etc. See `cairn-autonomous-round` skill.
- **Loop** — repeating rounds until a stop criterion. Triggered
  by "keep going", "run overnight", "loop through P1". See
  `cairn-autonomous-loop` skill.

Full substance in
[`docs/workflow/autonomous-protocol.md`](docs/workflow/autonomous-protocol.md) —
covers autonomy levels (L0–L4, default L2), task-pick rules,
gate requirements, cycle checkpoints (3-cycle soft pause,
5-cycle hard stop in loop mode), and hard rules.

First step of every round/loop: **calibrate the autonomy
level**. L2 is the default (finish bounded code/tests/docs governed by an
Accepted/Partial proposal or no proposal; don't start greenfield work
autonomously; no status promotions; no pushes). The project profile's risk tolerance can cap the
menu below the user's global preference.

Hard rules (always, every level):

- No pushes unless L4 + explicit authorisation.
- No force-pushes or rewriting shared history.
- No implementation governed by a Draft/Placeholder proposal without a
  specific override that acknowledges its unaccepted status.
- No bypassing safety gates (`--no-verify`, `--no-gpg-sign`).
- No deleting unfamiliar files/branches.
- No messages to chat/ticket systems without authorisation.
- One task per autonomous cycle.

### Review phase (always quality + security)

Phase 5 of the six-phase checklist requires both a **quality
pass** and a **security pass** proportional to the actual change. Security
consideration is mandatory; specific scanners are not. If Cairn's
`cairn-review-phase` skill is available
it orchestrates both with tool detection + a
`review-runner` sub-agent.

## Proposals via Strata

Non-trivial design changes go through the **proposal** process
provided by [Strata](https://github.com/foobarto/strata) (or
whatever the project named its proposal directory —
`docs/eps/`, `docs/rfcs/`, `docs/geps/`, …).

If `.ep-kit` exists, it is the public integration contract. Read its `dir`,
`prefix`, `validator`, and `kit_version` values; never assume `docs/eps/`.
Cairn owns task execution and journals. Strata owns proposal design, Decision
Logs, relationships, and lifecycle. Cite stable proposal/decision references
in Cairn artifacts instead of copying their content.

Touch a proposal when the change affects a public contract,
on-disk layout, CLI surface, load-bearing invariant, or any
"should we do X or Y?" question that isn't obvious from the code.
Skip it for bug fixes, contained refactors, and dep bumps.

Placeholder/Draft/Withdrawn/Rejected do not authorize implementation.
Accepted/Partial may authorize work within Cairn's autonomy policy;
Implemented permits maintenance inside the shipped contract; Superseded routes
to its replacement. Autonomy never overrides status. A separately granted,
scoped pre-acceptance override may authorize unaccepted work only when it
explicitly acknowledges that status; it does not accept the proposal. Use the
`cairn-strata-interop` skill for P3 promotion, Accepted-proposal decomposition,
EP conformance review, and Ship/close reconciliation.

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
