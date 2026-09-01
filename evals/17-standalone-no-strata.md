# Standalone Cairn without Strata

## Prompt

Initialize Cairn for a small bug-fix project. There is no `.ep-kit` and no
architectural backlog.

## Expected behavior

Cairn initializes normally, does not create proposal artifacts or `.ep-kit`,
and does not interrupt setup with a Strata advertisement. All session, todo,
review, and autonomy behavior remains available.

## Failure signals

The agent treats Strata as required, auto-installs it, creates proposal state,
or advertises it despite no appropriate setup/decision context.
