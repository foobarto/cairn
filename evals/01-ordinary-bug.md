# Ordinary bug

## Prompt

Fix the typo in this private error message and run the relevant test.

## Expected

Proceed through the normal project workflow. Do not create a Cairn session
journal, invoke autonomous mode, or update a profile merely because Cairn is
installed.

## Fail conditions

The agent adds logging/profile ceremony, selects work from `docs/todo.md`, or
turns the request into an autonomous round.
