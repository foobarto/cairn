---
name: cairn-build-user-profile
description: Maintain a Cairn user profile when the user explicitly asks to record a durable collaboration preference or authorizes profile synthesis. Keep personal observations private by default; use cairn-build-project-profile for shared project stances.
metadata:
  version: "0.3.0"
---

# cairn: Build-user-profile skill

Maintain the **user profile** — a living synthesis of how the
user thinks, decides, and collaborates. Not what they prefer at
a single-issue level (those are individual memory entries);
*how they reason* at the meta level.

## When to use this skill

- The user explicitly asks to record a durable preference about
  how they work.
- The user authorizes a synthesis pass over prior Cairn profile
  evidence.
- At session close, only when standing user or project guidance
  already authorizes Cairn profile maintenance.

## Do NOT use for

- Task-ephemeral preferences (which file to edit now).
- Frustration, impatience, or emotional reactions — this is
  about working patterns, not moods.
- Project-specific stances (use `cairn-build-project-profile`).
- Random one-off observations — need at least two data points
  or an explicit statement before it goes in.
- Preference signals the user did not ask to persist. Noticing a
  pattern is not authority to write personal data.

## Profile location (resolve at start)

In order:

1. `$CAIRN_USER_PROFILE` env var → use that path.
2. `<project>/.cairn/config.json` → if present and has
   `user_profile_path`, use that.
3. `~/.config/cairn/user-profile.md` → **default** (global).

If none of the above exists and the user-profile feature is
enabled, offer to bootstrap at the global default and prompt
for the install-time location choice. If the user skipped the
feature entirely (option 4 at install), don't silently create
one — ask.

## How to update

**Observations with evidence, not judgments.**

Every new entry needs:

- A specific section (Communication style / Decision-making
  pattern / Design values / Collaboration posture /
  Technical preferences / Open tensions).
- A one-line observation.
- Evidence — a session date, conversation reference, or a
  quote from the user. Evidence makes the observation
  refutable, which keeps the profile honest.

Example:

```markdown
## Communication style

- **Prefers terse openings.** Uses "btw", "actually", "oh
  and" to jump straight to the point. Evidence: 2026-04-24
  session (multiple turns), 2026-04-25 session (two turns).
```

Not:

```markdown
## Communication style

- User is impatient. (No.)
- User likes short messages. (Too vague.)
```

## Re-synthesise, don't blindly append

Every ~5 new observations (or at session close if a meaningful
pattern emerged), re-read the whole file:

1. Merge duplicates that grew into redundant bullets.
2. Refine wording where sharper observations replaced earlier
   guesses.
3. Remove observations that turned out wrong or were one-offs
   — keep the profile refutable and honest.
4. Update `last-synthesised: YYYY-MM-DD` in the frontmatter.

The file is synthesis, not history. If you want the history,
the session journals have it.

## Section invariants

- Keep the "How to apply this profile" section at the bottom
  concrete and actionable. It's what other skills and agents
  actually consume. Bullets should be prescriptive: "Prefer
  X over Y," not observations.
- Keep "Open tensions" honest — if two observations contradict,
  note it there rather than picking a winner prematurely.
- Don't let any section grow past ~8-10 bullets. If it does,
  you're probably not re-synthesising; cluster or re-cut.

## At an authorized session close

Invoked from `cairn-close-session`:

1. Read today's session journal.
2. Scan for signal-bearing exchanges (user correction,
   confirmed unusual choice, preference reveal).
3. If one or more new observations are warranted and the user
   authorized this profile update, add them with evidence.
4. Consider whether this triggers a re-synthesis pass (if >5
   observations added since last synthesis, or if a newer
   observation supersedes an older one).
5. Log the update in the close-session handoff — one-liner
   saying "profile updated with N new observations" or
   "no new profile signal this session."

## Privacy

The user profile is personal. Default locations are private:
`~/.config/cairn/` or a project-local ignored `.cairn/` path.
Do not create or update a tracked personal profile unless the user
explicitly chooses that exact publication boundary after being told
the file will be visible to repository collaborators.
