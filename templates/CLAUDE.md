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
| Session start                              | Read today's `docs/sessions/<date>-<topic>.md` if any + `docs/project-profile.md` for stance + user profile for collaboration calibration |
| As you work                                | Append to today's `docs/sessions/<date>-<topic>.md`   |
| When you notice something worth tracking   | `docs/todo.md` under the appropriate priority tier    |
| When a stance settles                      | `docs/project-profile.md` (project-wide) / user profile (personal) |
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

### Autonomous work — round vs loop

When running unattended, pick the shape that matches the ask:

- **Round** — one bounded cycle, stop when done. Triggered by
  "do one task from the punch list", "finish the Kanban refactor
  autonomously", etc. See `cairn-autonomous-round` skill.
- **Loop** — repeating rounds until a stop criterion. Triggered
  by "keep going", "run overnight", "loop through P1". See
  `cairn-autonomous-loop` skill.

Full substance in
[`docs/workflow/autonomous-protocol.md`](workflow/autonomous-protocol.md) —
covers autonomy levels (L0–L4, default L2), task-pick rules,
gate requirements, commit checkpoints (3-commit soft pause,
5-commit hard stop in loop mode), and hard rules.

First step of every round/loop: **calibrate the autonomy
level**. L2 is the default (finish in-progress partials; don't
start greenfield work autonomously; no status promotions; no
pushes). The project profile's risk tolerance can cap the
menu below the user's global preference.

Hard rules (always, every level):

- No pushes unless L4 + explicit authorisation.
- No force-pushes or rewriting shared history.
- No bypassing safety gates (`--no-verify`, `--no-gpg-sign`).
- No deleting unfamiliar files/branches.
- No messages to chat/ticket systems without authorisation.
- One task per turn.

### Review phase (always quality + security)

Phase 5 of the six-phase checklist requires both a **quality
pass** (project gate + linter) and a **security pass** (SAST
tool if available, manual OWASP review otherwise). Neither is
optional. If cairn's `cairn-review-phase` skill is available
it orchestrates both with tool detection + a
`review-runner` sub-agent.

## Proposals via ep-kit

Non-trivial design changes go through the **proposal** process
provided by [ep-kit](https://github.com/foobarto/ep-kit) (or
whatever the project named its proposal directory —
`docs/eps/`, `docs/rfcs/`, `docs/geps/`, …).

Touch a proposal when the change affects a public contract,
on-disk layout, CLI surface, load-bearing invariant, or any
"should we do X or Y?" question that isn't obvious from the code.
Skip it for bug fixes, contained refactors, and dep bumps.

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
