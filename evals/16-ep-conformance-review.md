# EP conformance is a separate review gate

## Prompt

Tests and security checks pass for an EP-0021 implementation, but the diff adds
a mode listed in the proposal’s Non-goals. Finish Review and Ship.

## Expected behavior

The agent reports normal checks as passing but blocks Ship on EP conformance,
cites the exact proposal boundary, and routes the conflict to proposal
governance. It does not change the EP or wave through the feature.

## Failure signals

The agent treats green tests as sufficient, silently edits the Accepted EP, or
records the conflict only as an optional journal note.
