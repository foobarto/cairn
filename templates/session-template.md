# <YYYY-MM-DD> — <topic slug>

<!--
  cairn session journal template.
  Filename: docs/sessions/<YYYY-MM-DD>-<topic-slug>.md
  - One file per working session (or per topic if a single day
    touches clearly-distinct topics).
  - Append as you go, not retroactively. Each time you pick a
    task, start a new `##` heading.
  - The file is shared history, not ephemeral scratch. Commit it.
-->

User instruction (paraphrased or verbatim if short):

> <what the user asked for>

---

## <HH:MM or task seam> — <task picked or topic>

**Task picked:** <one-line description>. <Why this one>.

**What shipped:**

- <concrete bullet>; reference [file path](path/to/file.ext) or
  `file:line` where useful.
- Scope that changed mid-implementation (list it honestly).

**Design calls I made without you:**

- **<short name of the call>.** <What was decided.> <Rationale —
  usually 1-2 sentences on why this option beat the alternatives
  you considered.>
- **<next call>.** ...

**Gates:**

- `<tool> <command>` — <result>. (Name the tool. "Tests pass" is
  not enough. E.g. `pytest tests/foo_test.py` — 17/0;
  `cargo clippy --all-targets` — 0 warnings;
  `pnpm typecheck` — clean.)
- Exit codes checked where the tool reports warnings without
  non-zero exit (e.g. `mix credo --strict` — `echo $?`).

**Skipped / not done this turn:**

- <What you chose not to do, and why>.
- Example: "Full browser E2E skipped — no browser available in
  this environment; if you want it run, do it locally."
- Example: "Codex review skipped — docs-only diff, marginal
  value; run on PR if you want the full gate."

**Commit(s):** `<short-sha>` — `<commit subject>`.

---

## <next task picked this session>

...

---

## Things I'd like your review / yes-or-no on when you're back

<!--
  The end-of-file section is for explicit review-requests the
  user should answer before the next working session. Don't list
  everything — pick the decisions that are genuinely on the
  critical path.
-->

1. **<short name of the question>.** <What you chose and the
   alternative. Specifically: is this the right call?>
2. ...
