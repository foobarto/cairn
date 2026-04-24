# 2026-04-24 — kanban-ux-polish

<!--
  Example session log illustrating the cairn format.
  Fictional project; illustrative content only.
-->

User instruction:

> Pick up the kanban stuck-banner work — it's been sitting in P1
> for two cycles. Take it to done if you can in one round.

---

## 14:20 — picked "kanban stuck-banner (issue #274)"

**Task picked:** Visual banner in TaskLive when a task has been
parked in the "review" column for >24h. Issue #274, tier P1.
Picked because it's the oldest P1 item and it's bounded — one
LiveView template + one query + a css utility class.

**What shipped:**

- [lib/app_web/live/task_live.ex:218-242](lib/app_web/live/task_live.ex) —
  `stuck?/1` helper and conditional render of a `.gl-stuck-banner`
  span above the task title.
- [lib/app_web/live/task_live.ex:340-348](lib/app_web/live/task_live.ex) —
  query gains `reviewed_at` field so the 24h comparison doesn't
  have to parse the audit JSONL.
- [assets/css/app.css:1120-1130](assets/css/app.css) — new
  `.gl-stuck-banner` utility class (muted amber chip with a
  clock glyph).

**Design calls I made without you:**

- **24h threshold vs configurable.** Hard-coded 24h. A
  per-project threshold could become a config later; for now a
  single number that works for a weekend-plus-one-workday cycle
  is fine. Easy to flip to config if anyone complains.
- **Banner placement — above vs beside title.** Above. The row
  already has tight horizontal space at narrow viewports;
  stacking is safer than cramping.
- **Clock glyph vs warning triangle.** Clock. A triangle says
  "error", but "review has stalled" is not an error — it's a
  reminder.

**Gates:**

- `pnpm test lib/app_web/live/task_live_test.exs` — 31/0
  (3 new tests on `stuck?/1`).
- `pnpm typecheck` — clean.
- `pnpm format --check` — clean.
- Manual: opened `/companies/demo/tasks/demo-01`, verified banner
  appears when `reviewed_at` is >24h old, disappears when
  fresh.

**Skipped / not done this turn:**

- No E2E test. The `TaskLive` rendering path is already covered
  by unit tests; the banner is a presentational addition on an
  existing query. If you'd rather see a Playwright assertion
  added, I'll do it in a follow-up.
- No CHANGELOG entry — #274 is small enough to ride in with the
  next release's consolidated note.

**Commit:** `a3f2c91` — `feat(task): stuck banner for reviews
parked > 24h (#274)`.

---

## Handoff — 15:05

**Shipped this round:** `a3f2c91` stuck-banner on TaskLive.

**Stopped because:** first commit of the session + 3-commits
soft cap is the ceiling; user asked for "one round" explicitly,
so I'm stopping rather than scheduling the next wakeup.

**Queued if you want more (none picked):**

- #278 — Kanban filter-chip colour inconsistency (P2).
- #280 — Audit log CSV export (P2).

**For your review:**

1. **24h threshold hard-coded?** I picked a fixed 24h rather
   than adding a per-project config. Happy to invert if you'd
   rather have the knob.
2. **E2E coverage?** No Playwright assertion added this round.
   If stuck-banner regressions would be embarrassing, I can
   follow up with one; if you're fine with the unit-test
   coverage, mark this closed.

---

## Things I'd like your review / yes-or-no on when you're back

See the Handoff block above — same two items.
