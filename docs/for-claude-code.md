# Cairn on Claude Code

Claude Code can load Cairn as a native plugin. The plugin packages the same
canonical Agent Skills from `skills/` and adds Claude-specific commands and
subagents.

## Install the plugin

From Claude Code:

```text
/plugin marketplace add foobarto/cairn
/plugin install cairn@cairn
```

For local development, launch `claude --plugin-dir /path/to/cairn`. Do not
manually copy a checkout into a plugin directory; use the marketplace or
`--plugin-dir` so Claude validates and loads the package correctly.

Run `claude plugin validate --strict /path/to/cairn` before publishing plugin
changes. See the current [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins)
for installation scopes and skill namespacing.

## Scaffold a project

Use `/cairn-init` for the Claude-specific interactive path. It can offer a
reviewed merge into an existing `CLAUDE.md` and does not duplicate plugin
skills into the project.

From a shell, the equivalent non-overwriting scaffold is:

```bash
/path/to/cairn/install.sh --agents-file CLAUDE.md --no-skills
```

The two paths intentionally differ when `CLAUDE.md` already exists: the
command can ask to merge Cairn sections; the shell installer always skips.

## Claude-only adapters

- `/cairn-session`, `/cairn-round`, and `/cairn-loop` are thin command
  adapters over canonical skills.
- `prior-session-digest`, `autonomous-planner`, and `review-runner` are optional
  subagents. Canonical skills capability-detect them and degrade honestly.
- A recurring-task or scheduling capability may resume
  `cairn-autonomous-loop`; `cairn-autonomous-round` never schedules another
  cycle.
- Claude memory is separate from Cairn profiles. Neither may be updated unless
  the user or standing project instructions authorize that persistence.
