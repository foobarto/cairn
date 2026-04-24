---
cairn-artifact: project-profile
version: 1
last-synthesised: YYYY-MM-DD
---

# Project profile

<!--
  cairn project-profile template.

  Default location: docs/project-profile.md (tracked in git,
  shared with all contributors).

  This file captures *what this project values* — code style,
  architecture stance, risk tolerance, security posture,
  quality bar, contribution norms, tech-debt policy.

  It differs from CLAUDE.md/AGENTS.md/GEMINI.md in role:
    - CLAUDE.md = operational (commands, file paths, skills).
    - project-profile = dispositional (stances, values,
      aesthetic calls, tradeoff preferences).

  Written declaratively. Every section is a stance the
  project has settled on, with enough context that a new
  contributor (human or agent) can apply it consistently.

  Each section should be SHORT. If a section grows past ~10
  bullets, some of it is probably actually documentation that
  belongs elsewhere (architecture doc, style guide, etc.) —
  link out rather than inline.
-->

Short statement of this project's values, stances, and
tradeoff preferences. Read at session start by every
contributor (human or agent) to calibrate implementation
choices without having to re-infer them from the code.

## Code style

<!-- Indent conventions, naming, comment policy, file organization. Keep short. Link to a style guide if one exists. -->

- ...

## Architecture style

<!-- Preferred patterns, module boundary discipline, testing philosophy, what "done" looks like structurally. -->

- ...

## Risk tolerance

<!--
  Calibrate the autonomy menu here. E.g.:
  - "Conservative — cap autonomous rounds at L1 until v1.0."
  - "Moderate — L2 default, L3 with explicit user sign-off."
  - "Aggressive — L3 default; security-adjacent changes still
    require L2 cap."
-->

**Level:** <Conservative | Moderate | Aggressive>

<!-- Elaboration: what kinds of changes are you cautious about? Breaking changes, dep updates, new features, schema migrations? -->

- ...

## Security posture

<!--
  What the security pass during Review (phase 5) must cover.
  Known-sensitive areas, past incidents, project-specific
  threat model notes.
-->

**Stance:** <Paranoid | Standard | Permissive>

<!--
  Sensitive areas — list files, modules, or patterns that
  need extra care. Past-incident-informed items especially.
-->

- **Sensitive area:** <path / module> — <why>.
- ...

**Required review tools** (if any cannot be skipped even when
the project's main linter is clean):

- ...

## Quality bar

<!--
  Coverage expectations, performance targets, what "good
  enough to ship" means for this project.
-->

- **Test coverage:** <minimum %, or "every public function
  has at least one test", or "integration test required for
  anything crossing a module boundary">.
- **Performance:** <target latency, memory ceiling, or "no
  explicit target — regressions flagged in code review">.
- **Docs:** <every public function has a docstring | README
  examples kept in sync | etc.>
- ...

## Contribution norms

<!--
  PR size expectations, commit granularity, review depth, when
  second-opinion is required. What earns vs blocks a merge.
-->

- **Commit granularity:** <small atomic commits | feature-per-
  commit | squash at merge>.
- **PR size:** <keep under N lines | feature-granularity | no
  limit>.
- **Second-opinion review:** <always required | non-trivial
  only | discretionary>.
- **Autonomous commits:** <allowed (at what autonomy level) |
  require checkpoint every N | not allowed>.

## Tech-debt stance

<!--
  When to pay down vs defer. What counts as "actively wrong"
  (P0 tier in the punch list).
-->

- **Pay down when:** <triggers — e.g., "touching a module
  for a feature change surfaces it", "blocks a new feature",
  "security implication">.
- **Defer when:** <triggers — e.g., "isolated in deprecated
  code path", "cost-benefit unclear", "pre-1.0 still">.
- **What counts as P0:** <criteria — e.g., "anything breaking
  the primary user workflow", "security incident in the
  wild", "CI failing for >24h">.

## Design aesthetic

<!--
  Optional — the hard-to-articulate "flavor" of the project.
  Simplicity over cleverness? Performance over ergonomics?
  Explicit over magical? If nothing notable here, delete
  this section.
-->

- ...

## Open tensions

<!-- Where the project is still figuring out its stance. Keep honest. -->

- ...

---

<!--
  Update protocol:

  1. Update in-place as stances solidify. Each change is a PR
     — the team reviews profile changes the same way they
     review code.
  2. `last-synthesised:` in the frontmatter tracks when
     someone last did a full-file read-through.
  3. If a section grows past ~10 bullets, split it out into
     a dedicated doc (architecture.md, style-guide.md,
     threat-model.md) and link from here.
  4. Don't inherit everything from parent-project profiles
     blindly — each project has its own context. But do
     reference them in "see-also" where appropriate.
-->
