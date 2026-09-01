# TODO — running punch list

<!--
  cairn's rolling punch list template. Ships at `docs/todo.md`.

  This file carries *noticed-but-not-yet-shipped* items that
  don't warrant a full proposal. When `.ep-kit` exists, resolve its
  configured proposal directory instead of assuming `docs/eps/`.
-->

Rolling list of noticed-but-not-yet-shipped items. Updated at the
end of every working cycle.

- **What lives here:** observations, follow-ups, visual polish,
  small UX tweaks, and deferred sub-tasks that don't warrant a
  proposal.
- **What doesn't:** architectural decisions (→ proposal), shipped
  work (→ CHANGELOG), autonomous-session review notes (→ session
  journal under `docs/sessions/`), load-bearing invariants (→
  agent-instructions file or the project's architecture doc).

Format: one bullet per item. Check `[x]` when shipped; delete
once it's been in CHANGELOG for a cycle.

---

## P0 — actively wrong (broken/lying/crashy)

*(empty — knock on wood)*

## P1 — next cycle

<!--
  Bounded, owner-known, ready to pick up. These are the items an
  autonomous round should draw from.
-->

- [ ] ...

## P2 — nice to have

<!--
  Real but deferrable. Not blocking; revisit in a later cycle.
-->

- [ ] ...

## P3 — thinking out loud

<!--
  Bigger items that might be worth a proposal later. Park them
  here so the idea isn't lost. If one crosses a public contract,
  persisted representation, trust boundary, load-bearing invariant,
  or durable design-choice boundary, promote it through the installed
  proposal system. Replace the evolving design text with a compact
  reference such as `- [x] Provider contract design -> EP-0017` and
  record the promotion in the current session journal.
-->

- [ ] ...

---

## Shipped this cycle (<YYYY-MM-DD> to <YYYY-MM-DD>)

<!--
  Running log of items that shipped since the last version cut.
  At each version bump, roll these into the CHANGELOG and clear
  the section.
-->

- [x] ...
