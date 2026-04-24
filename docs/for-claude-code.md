# cairn on Claude Code

cairn ships as a native Claude Code plugin. This is the most
integrated experience — slash commands, skills that the agent
auto-discovers, and sub-agents.

## Install

### Option A — as a Claude Code plugin (recommended)

```bash
# From a git clone:
git clone https://github.com/foobarto/cairn ~/.claude/plugins/user/cairn

# Or copy from a local checkout:
cp -r /path/to/cairn ~/.claude/plugins/user/cairn
```

Claude Code picks up plugins from `~/.claude/plugins/user/` at
session start. Verify:

```bash
ls ~/.claude/plugins/user/cairn/.claude-plugin/plugin.json
```

After restarting Claude Code:

- `/cairn-init`, `/cairn-session`, `/cairn-round` slash
  commands are available.
- The `cairn-session-log`, `cairn-autonomous-round`, and
  `cairn-close-session` skills are discoverable.
- The `prior-session-digest` sub-agent is available.

### Option B — per-project, without plugin install

If you can't or don't want to install a user-level plugin, copy
cairn into the project:

```bash
cd /your/project
cp -r /path/to/cairn/.claude-plugin ./
cp -r /path/to/cairn/commands ./.claude/commands/
cp -r /path/to/cairn/skills ./.claude/skills/
cp -r /path/to/cairn/agents ./.claude/agents/
```

This is heavier-touch but keeps cairn scoped to the single
project.

## Per-project scaffolding

Once cairn is installed as a plugin, inside any project:

```
/cairn-init
```

This copies the templates into the project's `docs/` directory
and merges cairn's conventions into the project's `CLAUDE.md`
(or creates one if none exists).

## Usage reference

| Slash command       | Purpose                                             |
|---------------------|-----------------------------------------------------|
| `/cairn-init`       | Scaffold templates into the current project        |
| `/cairn-session`    | Open or append to today's session journal          |
| `/cairn-round`      | Run one bounded autonomous-round cycle             |

| Skill                    | When Claude triggers it                         |
|--------------------------|-------------------------------------------------|
| `cairn-session-log`      | Any explicit "open / append / close the session log" phrasing or at natural commit seams |
| `cairn-autonomous-round` | User said "continue autonomously" / "keep going" / "pick something from todo" |
| `cairn-close-session`    | "That's enough for today" / "let's wrap up" / end-of-session signals |

| Sub-agent                | Use when                                        |
|--------------------------|-------------------------------------------------|
| `prior-session-digest`   | Session start — compress recent journals into 800 words without reading full files |

## Interaction with Claude Code's own conventions

- **Memory.** Claude Code's auto-memory at
  `~/.claude/projects/<slug>/memory/` is a natural fit for
  cairn's "save user preferences" guidance. The skills
  explicitly point at it.
- **Subagents.** `prior-session-digest` is a standard Claude
  Code sub-agent definition; use via the Agent tool with
  `subagent_type: "prior-session-digest"`.
- **Scheduled wakeups.** `/cairn-round` expects to schedule a
  next wakeup after each round; use `ScheduleWakeup` with
  the `<<autonomous-loop-dynamic>>` sentinel.
- **Hooks.** cairn doesn't ship hooks yet. A `SessionStart` or
  `UserPromptSubmit` hook that auto-opens today's session
  journal is a candidate enhancement.

## Known gotchas

- **Skill auto-discovery only works for user-level plugins.**
  If you chose Option B above, skills in `.claude/skills/`
  are project-scoped and need explicit invocation.
- **`/cairn-init` is non-destructive by default.** If you want
  to re-run it after changing cairn's templates, delete the
  existing files first or merge manually.
- **Session journal filenames** should use the literal date,
  not offsets. `date +%Y-%m-%d` in `/cairn-session` uses the
  host clock — if you're in an unusual timezone and want the
  "project-local" date, override via `CAIRN_TZ` or similar
  (not implemented yet; file an issue if this matters).
