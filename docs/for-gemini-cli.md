# cairn on Gemini CLI

Gemini CLI uses `GEMINI.md` as its project-instructions file,
similar to Claude Code's `CLAUDE.md`. cairn's templates work as-is;
the skills become instructions-by-reference.

## Install

1. Clone cairn somewhere stable:

   ```bash
   git clone https://github.com/foobarto/cairn ~/tools/cairn
   ```

2. Scaffold into a project:

   ```bash
   cd /your/project
   ~/tools/cairn/install.sh
   ```

   This copies `templates/CLAUDE.md` into the project. Rename it:

   ```bash
   mv CLAUDE.md GEMINI.md
   ```

3. Reference the skills from `GEMINI.md`. Gemini CLI doesn't have
   a plugin/skill system per se; you instruct the agent by adding
   references to the markdown files in your `GEMINI.md`:

   ```markdown
   ## When to use cairn skills

   - **Starting or appending to a session log:** read
     `~/tools/cairn/skills/session-log/SKILL.md` and follow it.
   - **Autonomous rounds:** read
     `~/tools/cairn/skills/autonomous-round/SKILL.md`.
   - **Closing a session:** read
     `~/tools/cairn/skills/close-session/SKILL.md`.
   ```

   Tell the agent explicitly: *"When starting a session, read the
   session-log skill at ~/tools/cairn/skills/session-log/SKILL.md
   and follow it."* Gemini CLI's tool configuration allows reading
   local files; the agent will open the skill and act on it.

## What you lose going non-plugin

- **No auto-discovery.** The agent won't know to use the skill
  unless you mention it in `GEMINI.md` or call it out in a prompt.
- **No slash commands.** `/cairn-init`, `/cairn-session`,
  `/cairn-round` don't exist. Use the install script directly;
  for session + round behaviours, the agent follows the skills.
- **No dedicated sub-agent.** `prior-session-digest` can be
  emulated by asking Gemini to "read the last two files under
  docs/sessions/ and return a compact digest"; the output shape
  will be close but not identical.

## What you keep

- **Templates** — CLAUDE.md-equivalent (rename to GEMINI.md),
  session-template, todo.md, six-phase-checklist,
  autonomous-protocol (covers round + loop), governing-principles,
  user-profile + project-profile. Pure markdown, works anywhere.
- **Skill substance.** The actual guidance in `SKILL.md` is
  portable Gemini CLI will happily read and follow it — you
  just need to tell it to.
- **Convention** — session journals at `docs/sessions/`,
  rolling punch list at `docs/todo.md`. These don't care about
  your CLI.

## Usage sketch

```bash
# Open today's session log:
gemini --file docs/sessions/$(date +%F)-<topic>.md \
       --prompt "Append a new task entry using the cairn session log format"

# Start an autonomous round:
gemini --prompt "Follow the cairn autonomous-round protocol at \
                 ~/tools/cairn/skills/autonomous-round/SKILL.md. \
                 Pick one bounded task from docs/todo.md and run the cycle."
```

Depending on your Gemini CLI version and config, you may want to
put these in shell aliases or a `justfile` so they're one-command
from your prompt.

## GEMINI.md excerpt

Here's a suggested top-of-file addition for `GEMINI.md`:

```markdown
## Session rhythm (cairn)

This project uses cairn for session journals, rolling punch list,
and autonomous rounds. When you start a session:

1. Check `docs/sessions/` for today's file; if present, read it.
2. If you're about to start an autonomous round, read
   `~/tools/cairn/skills/autonomous-round/SKILL.md` and follow it
   verbatim.
3. When logging what you did, follow the format in
   `~/tools/cairn/skills/session-log/SKILL.md`.
4. When closing out, read
   `~/tools/cairn/skills/close-session/SKILL.md`.

The templates you should match are in `~/tools/cairn/templates/`.
```

Adjust the path to wherever you've cloned cairn.
