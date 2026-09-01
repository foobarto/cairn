---
name: cairn-build-project-profile
description: Maintain docs/project-profile.md when a project explicitly adopts or revises a shared stance on risk, security, quality, architecture, or contribution norms. Do not use for personal preferences or unsettled ideas.
metadata:
  version: "0.3.0"
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
  `cairn-build-user-profile`).
- Operational details (how to run tests, where files live
  — those belong in the project's agent-instructions file).
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
bootstrap it only when the user authorized creating the shared profile. Use
frontmatter with `cairn-artifact: project-profile`, `version: 1`, and
`last-synthesised`, followed by these headings: Code style, Architecture style,
Risk tolerance, Security posture, Quality bar, Contribution norms, Tech-debt
stance, Design aesthetic, and Open tensions. Do not depend on a repository-only
template path.

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
5. Include it in the normal review flow. Commit it only when the request or
   project policy authorizes commits.

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
  add it only when the close request or standing policy authorizes a durable
  shared-profile update.
- If not, note in the handoff: "No project-profile updates
  this session."

## One-time bootstrap

For projects adopting cairn mid-life, the first
project-profile pass is an intentional exercise, not an
accidental accumulation. Sit with a maintainer and fill in
each section from scratch using the section reminders above. Don't copy another project's
profile — these stances are project-specific.
