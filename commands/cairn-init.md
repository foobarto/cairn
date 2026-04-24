---
description: Scaffold cairn's workflow artefacts into the current project
allowed-tools: Bash(mkdir:*), Bash(cp:*), Bash(test:*), Bash(ls:*), Read, Write, Edit
---

# /cairn-init

Scaffold cairn's workflow artefacts into the current project
(the one you're `cd`'d into). Non-destructive — existing files
are left alone; new ones are created from templates.

## What gets created

Relative to the current project root:

| Path                                    | Source                                              |
|-----------------------------------------|-----------------------------------------------------|
| `docs/sessions/`                        | new directory                                       |
| `docs/sessions/README.md`               | short pointer to the template                       |
| `docs/todo.md`                          | `cairn/templates/todo.md`                           |
| `docs/project-profile.md`               | `cairn/templates/project-profile.md`                |
| `docs/workflow/governing-principles.md` | `cairn/templates/workflow/governing-principles.md`  |
| `docs/workflow/six-phase-checklist.md`  | `cairn/templates/workflow/six-phase-checklist.md`   |
| `docs/workflow/autonomous-protocol.md`  | `cairn/templates/workflow/autonomous-protocol.md`   |

Plus one **interactive prompt** for the user-profile location.

## CLAUDE.md handling

If no `CLAUDE.md` exists at the project root: drop
`cairn/templates/CLAUDE.md` as-is, telling the user to customise
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
  [3] Project-local, tracked — docs/user-profiles/<handle>.md
      Per-project, shared with collaborators (handle = git user).
  [4] Skip — no profile feature.

Pick [1/2/3/4] (default: 1):
```

Record the choice:

- **Option 1 (global):** create `~/.config/cairn/user-profile.md`
  from template if missing. No per-project config needed.
- **Option 2 (local, gitignored):** create
  `<project>/.cairn/user-profile.md` from template. Add
  `/.cairn/` to the project's `.gitignore` (ask before editing).
  Write `<project>/.cairn/config.json` with
  `{"user_profile_path": ".cairn/user-profile.md"}`.
- **Option 3 (local, tracked):** resolve `<handle>` from `git
  config user.name` (fall back to `$USER`). Create
  `<project>/docs/user-profiles/<handle>.md` from template.
  Write `<project>/.cairn/config.json` with
  `{"user_profile_path": "docs/user-profiles/<handle>.md"}`.
- **Option 4 (skip):** do not create the profile file or
  config.

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

## Non-goals

- Does not install ep-kit. If the project wants structured
  proposals, run ep-kit's own installer separately.
- Does not modify `.gitignore`.
- Does not scan existing code or infer project specifics.
  Customisation of `CLAUDE.md`'s project-specific section is
  the user's call.
