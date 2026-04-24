---
cairn-artifact: user-profile
version: 1
scope: global  # global | project-local-gitignored | project-local-tracked
last-synthesised: YYYY-MM-DD
---

# User profile

<!--
  cairn user-profile template.

  Default location: ~/.config/cairn/user-profile.md (global,
  private, cross-project). Other locations supported at
  install time:
    - .cairn/user-profile.md (project-local, gitignored)
    - docs/user-profiles/<handle>.md (project-local, tracked)

  This file is a *synthesis*, not an append-only log. Each entry
  is an observation with evidence. At natural seams, the agent
  re-reads and consolidates; it does NOT just keep appending.

  Rule of thumb: if you can't point to a specific session or
  exchange that shows the pattern, it doesn't belong here.
-->

Synthesis of *how the user thinks* — decision-making patterns,
design values, communication style, collaboration posture. Read
by the agent at session start to calibrate framing, defaults,
and autonomy choices.

Observations are **with evidence, not judgments**. Not
*"user is impatient"* but *"user has corrected me for long
preambles twice — prefer terse framing."* The evidence link
keeps the profile refutable.

## Communication style

<!-- How the user prefers to communicate — tone, length, formality, cadence. -->

- ...

## Decision-making pattern

<!-- How the user reasons toward decisions — exploratory vs decisive, alone vs with input, interrogates rationale or outcomes. -->

- ...

## Design values

<!-- What the user values in design + architecture — simplicity, specificity, risk tolerance in their own work, product vs system thinking, etc. -->

- ...

## Collaboration posture

<!-- How the user works with AI agents — autonomy comfort, review expectations, what earns trust vs erodes it. -->

- ...

## Technical preferences

<!-- Tool choices, languages, licenses, editor/keybinding preferences. Persistent across projects. -->

- ...

## Open tensions

<!-- Observations that seem to conflict with each other, or where the user is still calibrating. Keep honest — don't force-resolve. -->

- ...

## How to apply this profile

<!-- Derived guidance for making decisions that match the profile. -->

When choosing between framings or defaults:

- ...

When in doubt about whether to interrupt:

- ...

---

<!--
  Update protocol:

  1. Append new observations under the relevant section as they
     arise during sessions. Always with evidence.
  2. At natural seams (session close, monthly, after a big
     project), re-read the whole file. Merge duplicates,
     refine wording, remove observations that turned out wrong
     or were one-offs.
  3. Update `last-synthesised:` in the frontmatter.
  4. Don't save frustration, impatience, or emotional reactions.
     This is about working patterns, not moods.
-->
