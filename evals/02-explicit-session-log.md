# Explicit session log

## Prompt

Open today's Cairn session log for the parser cleanup and record the checks we
just ran.

## Expected

Use `cairn-session-log`, create or append the correctly dated topic file, and
record concrete commands and results without inventing work.

## Fail conditions

The agent only summarizes in chat, invokes full close-session, or reconstructs
unverified events.
