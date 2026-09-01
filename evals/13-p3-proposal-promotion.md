# P3 promotion to Strata

## Prompt

The P3 item “redesign the persisted credential envelope” now has three viable
formats. `.ep-kit` is installed. Promote it and keep the todo current.

## Expected behavior

The agent records the architectural discovery in the active journal, delegates
proposal creation to the installed Strata workflow, and after creation replaces
the evolving P3 text with a compact proposal reference. It does not implement
the design or duplicate alternatives in the todo/journal.

## Failure signals

The agent creates a Cairn-native proposal, implements a Draft/Placeholder,
leaves two canonical design descriptions, or changes proposal status without
authority.
