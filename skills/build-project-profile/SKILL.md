---
name: cairn-build-project-profile
version: 0.2.0
description: Use to maintain the project profile at docs/project-profile.md — declarative statement of the project's values, risk tolerance, security posture, quality bar, and contribution norms. Triggers when the project settles a stance on a cross-cutting concern (e.g., "we don't mock databases in tests", "pre-1.0, no backwards-compat shims", "security posture is paranoid about injection"). Tracked in git; shared with all contributors. Updated in-place as part of normal PR workflow, NOT synthesis of individual sessions.
---

# cairn: Build-project-profile skill

Maintain the **project profile** — a declarative statement of
what this project values, stands for, and how it makes
tradeoffs. Unlike the user profile (synthesis of observations),
the project profile is negotiated consensus — the team's agreed
stances, written declaratively.

## When to use this skill

- A project decision settles a cross-cutting stance ("we
  don't mock databases in tests", "pre-1.0 means no backwards-
  compat shims", "Credo warnings are blocking").
- A code review surfaces a stance worth codifying ("we've
  rejected this pattern three times, let's write it down").
- An incident or near-miss reveals a gap in the current
  posture ("security: paranoid about path traversal after
  the `../../` bypass incident").
- The project formally adopts a risk tolerance level or
  security posture.

## Do NOT use for

- Per-session observations about the user (that's
  `build-user-profile`).
- Operational details (how to run tests, where files live
  — that's CLAUDE.md).
- Speculative stances. Only codify what the project has
  actually settled.
- Architecture documentation. If it needs a diagram or 500
  words, it belongs in `docs/architecture.md` or similar;
  link from the profile.

## Profile location

**Always `docs/project-profile.md` in the project root**, tracked
in git. Not configurable — the whole point is it's shared
history every contributor sees.

If the file doesn't exist when this skill is first invoked,
bootstrap from `templates/project-profile.md` and commit it as
part of the PR that introduces the first real stance.

## How to update

**Declarative, not observational.** The user profile captures
*"the user tends to prefer X"*; the project profile says
*"this project values X."*

Each section has a fixed shape; consult the template for
what belongs where. Typical update sequence:

1. Identify the section the stance belongs in (Risk
   tolerance, Security posture, Contribution norms, etc.).
2. Replace or refine the existing bullet, or add a new one.
3. Keep it short. A project profile bullet is 1-3 sentences
   of stance; elaboration links out to dedicated docs.
4. Update `last-synthesised:` in the frontmatter.
5. Commit as part of a regular PR — profile changes go
   through code review like any other change.

## What belongs in each section (reminders)

- **Code style** — indent, naming, comment policy. One level
  up from a style guide.
- **Architecture style** — patterns accepted / rejected,
  module boundary discipline, testing philosophy.
- **Risk tolerance** — Conservative / Moderate / Aggressive,
  plus elaboration on which kinds of changes are flagged.
- **Security posture** — Paranoid / Standard / Permissive,
  plus known-sensitive areas and required review tools.
- **Quality bar** — coverage minimums, performance targets,
  doc expectations.
- **Contribution norms** — PR size, commit granularity,
  second-opinion requirements, autonomous-commit policy.
- **Tech-debt stance** — pay down vs defer rules, P0 criteria.
- **Design aesthetic** — optional, the hard-to-articulate
  "flavor" of the project.
- **Open tensions** — where the project is still figuring
  things out. Keep honest.

## Integration with autonomous workflow

The project profile is consumed by several other cairn skills:

- **`cairn-autonomous-round` / `-loop`** — reads Risk
  tolerance to cap the autonomy menu. A "Conservative"
  project caps at L1 even if the user's global preference is
  L2.
- **`cairn-review-phase`** — reads Security posture to pin
  the security pass as mandatory with specific tools, not
  just a generic check.
- **`autonomous-planner` sub-agent** — reads the profile to
  filter candidate tasks by the project's risk posture.

This means keeping the profile up-to-date pays off directly in
every autonomous cycle. If you find yourself repeatedly
explaining "but this project is more conservative than that,"
that's a signal to update the profile.

## Size discipline

Each section should stay under ~10 bullets. If a section keeps
growing, move the detail to a dedicated document:

- Architecture detail → `docs/architecture.md`
- Security threat model → `docs/threat-model.md` or
  `docs/testing/threatmodel.md`
- Style rules → `docs/style-guide.md`
- Test philosophy → `docs/testing/philosophy.md`

Link from the project profile; don't duplicate.

## At session close

Invoked optionally from `cairn-close-session`:

- If a session settled a stance that belongs in the profile,
  add it now (as part of the close-out commit, so it rides
  with the shipping PR).
- If not, note in the handoff: "No project-profile updates
  this session."

## One-time bootstrap

For projects adopting cairn mid-life, the first
project-profile pass is an intentional exercise, not an
accidental accumulation. Sit with a maintainer and fill in
each section from scratch. The template has comments to
prompt the right questions. Don't copy another project's
profile — these stances are project-specific.
