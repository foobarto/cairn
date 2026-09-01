# Behavioral evaluations

These harness-neutral scenarios test Cairn's activation and authority
boundaries. They complement deterministic tests; they are not exact-output
goldens.

Run each case in an isolated fixture containing the installed
`.agents/skills/cairn-*` packages and the minimum project files named in the
prompt. Give the acting agent only the prompt and ordinary repository context.
Keep `Expected` and `Fail conditions` hidden until scoring.

Evaluate the first consequential action and the final state. Extra explanation
is acceptable. Record the client, model, Cairn revision, available continuation
and subagent capabilities, and whether the case passed. When a skill's trigger
or authority boundary changes, forward-test the affected cases with an
independent agent.

| Case | Boundary |
|------|----------|
| `01-ordinary-bug.md` | No Cairn ceremony for ordinary work |
| `02-explicit-session-log.md` | Explicit journal activation |
| `03-close-session.md` | Close versus append routing |
| `04-single-round.md` | Exactly one cycle |
| `05-loop-without-continuation.md` | Honest capability degradation |
| `06-draft-proposal-gate.md` | Autonomy never implies Draft authority |
| `07-accepted-proposal.md` | Accepted work may proceed within scope |
| `08-preference-without-consent.md` | No personal persistence by inference |
| `09-project-stance.md` | Shared stance routes to project profile |
| `10-nontrivial-review.md` | Evidence-backed independent review |
| `11-partial-proposal-completion.md` | Partial is not Implemented |
| `12-custom-strata-contract.md` | `.ep-kit` paths and optional keys are authoritative |
| `13-p3-proposal-promotion.md` | P3 crosses into Strata without duplicate design state |
| `14-accepted-ep-to-p1.md` | Accepted scope becomes reviewed bounded P1 work |
| `15-journal-architecture-escalation.md` | Journal detects and stops at architectural drift |
| `16-ep-conformance-review.md` | Green tests cannot override proposal conformance |
| `17-standalone-no-strata.md` | Cairn remains complete without Strata |
