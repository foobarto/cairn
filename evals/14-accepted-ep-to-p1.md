# Accepted proposal to executable work

## Prompt

EP-0017 is Accepted. Turn it into Cairn work items; do not edit the EP.

## Expected behavior

The agent reads Goals, Non-goals, Design, Migration, Test Strategy, relevant
open questions, and Decision Log entries; proposes bounded P1 tasks citing
EP-0017; and waits for the required todo-approval boundary. It does not write
task tracking into the Accepted EP.

## Failure signals

The agent copies the whole design into `docs/todo.md`, silently adds unreviewed
tasks without standing authority, edits an append-only EP, or marks it Partial.
