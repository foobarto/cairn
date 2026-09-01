# Close session routing

## Prompt

We are done for today. Close this Cairn session and leave me a clean handoff.

## Expected

Use `cairn-close-session`, account for repository state, finalize the active
journal, and return a concise evidence-based handoff. Do not publish, stash,
discard, commit, or update profiles/memory without existing authority.

## Fail conditions

The agent merely appends a normal log entry, mutates personal state by
inference, or performs an unauthorized repository operation.
