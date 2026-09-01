---
name: cairn-strata-interop
description: Coordinate Cairn work artifacts with an optional Strata installation when .ep-kit exists, including P3 promotion, Accepted proposal decomposition, EP conformance review, and lifecycle reconciliation. Also use when an architectural P3 item reaches the proposal boundary without Strata, but only to offer the optional integration once.
metadata:
  version: "0.3.0"
---

# Cairn: Strata interoperability

Cairn manages the life of the work. Strata manages the life of the decision.
Use this skill only at the boundary between those systems; never copy Strata's
proposal schema, Decision Log, relationship graph, or lifecycle into Cairn.

## Detect the public contract

Strata is installed when a `.ep-kit` file is present in the project root or an
ancestor selected by the project's normal root-discovery rules. Read that file
before looking for proposals. It is a `key=value` configuration file; blank
lines and lines beginning with `#` are comments.

Resolve:

- `dir` — proposal directory relative to the config file; default `docs/eps`.
- `prefix` — proposal-number frontmatter field; default `ep`.
- `validator` — configured validator path relative to the config file, if any.
- `kit_version` — installed contract version, if present.

The bundled `scripts/resolve_strata.py` performs this read-only resolution and
emits JSON. Use it when executable resources are available. If the config is
missing, Cairn remains fully functional and this skill exits without creating
anything. If it is malformed or resolves outside its project root, stop and
report the configuration error; do not guess a proposal directory.

Read the installed proposal process document and Strata skills when present.
They override this interoperability summary if their lifecycle or schema is
newer. Do not import Strata code into Cairn or auto-install it.

## Ownership boundary

- Project stance and operating values: `docs/project-profile.md`.
- Architectural decision, alternatives, relationships, and history: Strata.
- Implementation-local decision or discovery: Cairn session journal.
- Current executable work: `docs/todo.md`.
- Changed behavior: code and tests.
- Shipped release summary: `CHANGELOG.md`.
- Proposal implementation state: Strata lifecycle metadata.

No fact gets two canonical homes. Journals and todo items cite a proposal; they
do not reproduce its design or Decision Log.

## Lifecycle authority

Autonomy levels grant operational latitude, never proposal authority:

- `Placeholder` or `Draft`: proposal/design work only; status does not authorize
  implementation.
- `Accepted`: implementation may proceed within Cairn's autonomy policy.
- `Partial`: remaining accepted implementation may proceed.
- `Implemented`: only maintenance or follow-up within the shipped contract;
  changed architectural scope needs a new proposal.
- `Superseded`: follow the replacement proposal before selecting work.
- `Withdrawn` or `Rejected`: do not treat as implementation authority.

If implementation would conflict with an Accepted or Partial proposal, stop at
the decision boundary. Never let L2, L3, or L4 override proposal status.
A project or user may separately grant a specific, scoped pre-acceptance
implementation override that explicitly acknowledges an unaccepted proposal.
Never infer one from task assignment, autonomy level, or the proposal's
existence; it does not change the proposal's status.

## Stable references

Use Strata's stable textual references: `EP-NNNN`, and Decision Log references
such as `EP-NNNN D3`. These remain canonical even when a project calls its
proposals RFCs, GEPs, or something else. The configured `prefix` names the
frontmatter key; it does not change the textual citation family.

Examples:

- `**Proposal:** EP-0017`
- `Implementation follows EP-0017 D3.`
- `Conflict with EP-0017 D6; paused at the proposal boundary.`

## Promote a P3 item to a proposal

When a P3 item crosses a public contract, persisted shape, trust boundary,
load-bearing invariant, or durable alternatives/rationale boundary:

1. Record the discovery concisely in the active Cairn journal.
2. If Strata is installed, invoke its current governance/authoring workflow.
   Do not invent a Cairn proposal format.
3. After the proposal exists, replace or check off the P3 design text with a
   compact stable reference such as `- [x] Provider contract design -> EP-0017`.
4. Do not create implementation tasks until proposal authority permits them.

If Strata is absent, leave the item in P3 or tell the user once, in the setup or
decision context, that a structured proposal system may be appropriate. Do not
nag, auto-install, or imply that Cairn is degraded.

## Materialize an Accepted proposal into Cairn work

For an Accepted or Partial proposal:

1. Read Goals, Non-goals, Design, Migration, Test Strategy, relevant open
   questions, and applicable Decision Log entries.
2. Stop if an unresolved question blocks safe decomposition.
3. Propose bounded P1 tasks that each fit one Cairn cycle and cite the proposal.
4. Let the user review the decomposition unless standing project authority
   explicitly permits todo maintenance from accepted specifications.
5. Add only approved tasks to `docs/todo.md`, for example:
   `- [ ] EP-0017: migrate provider lookup call sites`.

The todo decomposition may evolve as implementation evidence changes. Never
write implementation task tracking back into an Accepted proposal.

## Journal-to-proposal escalation test

An adopted decision may remain journal-only only when it is implementation-
local, reversible, preserves public behavior and persisted representation,
does not alter a trust boundary or load-bearing invariant, and does not
contradict an Accepted/Partial proposal.

Escalate when a discovery changes any of those boundaries, materially
constrains future implementations, or deserves durable alternatives/rationale:

1. Record the discovery and evidence in the Cairn journal without duplicating
   the architectural decision.
2. Stop implementation at that boundary.
3. Invoke or recommend Strata to extend or supersede the governing proposal.
4. Resume only when proposal authority permits it.

## Review and completion reconciliation

When a change cites an Accepted or Partial proposal, Review includes a separate
EP-conformance pass against its Goals, Non-goals, Design constraints, and
relevant Decision Log entries. Passing tests do not excuse a conflict.

At Ship or close-session, assess every proposal referenced during the session:

- Is its status still truthful?
- Did no meaningful slice, some accepted scope, or every goal and rollout
  obligation ship?
- Did implementation expose a contradiction or architectural discovery?
- Are todo items stale because a proposal was superseded, withdrawn, or
  rejected?

Recommend `Accepted` when no meaningful production slice shipped, `Partial`
when some scope shipped but obligations remain, and `Implemented` only when all
accepted goals and rollout obligations are satisfied. Add `implemented-in`
only when the relevant release is actually known.

Assessment is read-only by default. Change proposal status, history,
relationships, or `implemented-in` only with the project's explicit lifecycle
authority. After any authorized proposal mutation, invoke the configured Strata
validator (or Strata's documented resolver when `validator` is absent) and
record the exact result. Most sessions should conclude: `No proposal changes
required.`
