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

| Path                           | Source                                     |
|--------------------------------|--------------------------------------------|
| `docs/sessions/`               | new directory                              |
| `docs/sessions/README.md`      | short pointer to the template              |
| `docs/todo.md`                 | `cairn/templates/todo.md`                  |
| `docs/workflow/six-phase-checklist.md` | `cairn/templates/workflow/six-phase-checklist.md` |
| `docs/workflow/autonomous-round-protocol.md` | `cairn/templates/workflow/autonomous-round-protocol.md` |

## CLAUDE.md handling

If no `CLAUDE.md` exists at the project root: drop
`cairn/templates/CLAUDE.md` as-is, telling the user to customise
the "Project-specific notes" section at the bottom.

If `CLAUDE.md` already exists: **do not overwrite.** Instead,
offer to append the "Session rhythm" and "Autonomous-round
cadence" sections from the template, preserving the user's
existing content above them. Ask before appending.

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
  ✓ docs/workflow/autonomous-round-protocol.md (created)
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
