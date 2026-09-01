---
description: Scaffold cairn's workflow artefacts into the current project
allowed-tools: Bash(mkdir:*), Bash(cp:*), Bash(test:*), Bash(ls:*), Bash(git rev-parse:*), Read, Write, Edit
---

# /cairn-init

Scaffold cairn's workflow artefacts into the current project
(the one you're `cd`'d into). Existing workflow files are skipped. An existing
`CLAUDE.md` or `.gitignore` changes only after the specific prompt described
below.

## What gets created

Relative to the current project root:

| Path                                    | Source                                              |
|-----------------------------------------|-----------------------------------------------------|
| `docs/sessions/`                        | new directory                                       |
| `docs/sessions/README.md`               | short journal convention                            |
| `docs/todo.md`                          | `cairn/templates/todo.md`                           |
| `docs/project-profile.md`               | `cairn/templates/project-profile.md`                |
| `docs/workflow/governing-principles.md` | `cairn/templates/workflow/governing-principles.md`  |
| `docs/workflow/six-phase-checklist.md`  | `cairn/templates/workflow/six-phase-checklist.md`   |
| `docs/workflow/autonomous-protocol.md`  | `cairn/templates/workflow/autonomous-protocol.md`   |

Plus one **interactive prompt** for the user-profile location.

## CLAUDE.md handling

If no `CLAUDE.md` exists at the project root: drop
`cairn/templates/agent-instructions.md` as `CLAUDE.md`, telling the user to customise
the "Project-specific notes" section at the bottom.

If `CLAUDE.md` already exists: **do not overwrite.** Instead,
offer to append the "Governing principles," "Session rhythm,"
and "Autonomous-round cadence" sections from the template,
preserving the user's existing content above them. Ask before
appending.

## User-profile location prompt

The user profile is cairn's synthesis of *how the user thinks*
across projects. Before scaffolding, ask where it should live:

```
Where should cairn keep your user profile?

  [1] Global (recommended) — ~/.config/cairn/user-profile.md
      One profile across all your cairn projects. Private to you.
  [2] Project-local, gitignored — .cairn/user-profile.md
      Per-project, not shared with collaborators.
  [4] Skip — no profile feature.

Pick [1/2/4] (default: 1):
```

Record the choice:

- **Option 1 (global):** create `~/.config/cairn/user-profile.md`
  from template if missing. No per-project config needed.
- **Option 2 (local, gitignored):** create
  `<project>/.cairn/user-profile.md` from template. Add
  `/.cairn/` to the project's `.gitignore` (ask before editing).
  Write `<project>/.cairn/config.json` with
  `{"user_profile_path": ".cairn/user-profile.md"}`.
- **Option 4 (skip):** do not create the profile file or
  config.

Tracked personal profiles are intentionally unsupported. If the user asks for
one, explain the publication boundary and require an explicit project-specific
decision rather than treating it as an install mode.

## Steps

1. Identify the project root. If the user ran this from a
   subdirectory, locate the git root via `git rev-parse
   --show-toplevel`. If no git repo, use CWD and warn.
2. Locate cairn's install root. Typically the plugin's own
   directory — introspect from the skill's path (e.g.
   `<cairn-root>/templates/...`).
3. For each template listed above:
   - Check if the target file exists.
   - If missing, create parent dirs + copy.
   - If present, skip and note in the report.
4. Handle `CLAUDE.md` per the rules above.
5. Print a report:

```
cairn initialised.
  ✓ docs/sessions/ (created)
  ✓ docs/todo.md (created from template)
  ✓ docs/workflow/six-phase-checklist.md (created)
  ✓ docs/workflow/autonomous-protocol.md (created)
  ✓ docs/workflow/governing-principles.md (created)
  ✓ docs/project-profile.md (created)
  · CLAUDE.md (already exists; appended Session rhythm + Autonomous-round cadence sections)

Next: customise docs/todo.md and CLAUDE.md's "Project-specific
notes" section with your project's actual commands and invariants.
```

6. Do NOT auto-commit. Let the user review the scaffolding and
   commit as part of their normal workflow.
7. If `<target>/.ep-kit` exists, report that Cairn will use its configured
   proposal directory, prefix, validator, and version through the
   `cairn-strata-interop` skill. Do not install or modify Strata.
8. If `.ep-kit` is absent and the user's setup context explicitly identifies a
   clearly architectural P3/design backlog, include one optional line:
   `Optional: this project is accumulating durable design decisions. Strata
   adds numbered proposals, decision logs, lifecycle, and validation:
   https://github.com/foobarto/strata`
   Do not show this line for ordinary setup, repeat it in later sessions, or
   create state solely to track the suggestion.

## Non-goals

- Does not install Strata. If the project wants structured
  proposals, run Strata's own installer separately.
- Modifies `.gitignore` only when the user selects option 2, which explicitly
  requests a project-local ignored profile.
- Does not scan existing code or infer project specifics.
  Customisation of the selected agent-instructions file's project-specific section is
  the user's call.
