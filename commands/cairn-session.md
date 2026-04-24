---
description: Open or append to today's cairn session log
allowed-tools: Bash(date:*), Bash(ls:*), Bash(test:*), Read, Write, Edit
---

# /cairn-session

Open today's session journal, or append the most recent seam
(commit + gate results + deciscions taken since the last entry)
to an existing one. Calls into the `cairn-session-log` skill for
the detailed format rules.

## What this command does

1. Resolve today's date (`date +%Y-%m-%d`).
2. Scan `docs/sessions/` (or `CAIRN_SESSIONS_DIR` if set) for a
   file matching `<today>-*.md`.
3. If **no file exists**: ask the user for a topic slug (or
   infer from the current conversation context — e.g. if the
   last few turns have been about a specific feature). Create
   `docs/sessions/<today>-<slug>.md` from the cairn session
   template.
4. If **one file exists**: append a new `##` entry for the
   current task/seam.
5. If **multiple files exist for today**: ask which to append
   to (or start a new one if the current task is clearly a new
   topic).

Follow the `cairn-session-log` skill's section shape:

- `**Task picked:**`
- `**What shipped:**`
- `**Design calls I made without you:**`
- `**Gates:**`
- `**Skipped / not done this turn:**`
- `**Commit(s):**`

Before writing, pull the facts from recent context:

- Last few commits (`git log -n 5 --oneline`).
- Last test/gate results if any were run this turn.
- Any design decisions the agent took autonomously.

## Usage

```
/cairn-session                    # Open or append, inferring topic
/cairn-session <topic-slug>       # Force a specific topic slug
```

## Edge cases

- No `docs/sessions/` directory: offer to run `/cairn-init`
  first, or create the directory inline.
- Current task is clearly a new topic (user pivoted): append a
  clear `##` heading marking the pivot, or open a second
  file for today with a different slug.
- Session is ending: this command only appends. For the
  end-of-session ritual (punch-list update, handoff summary,
  durable memory), use the `cairn-close-session` skill or the
  `/cairn-round` command's stop branch.
