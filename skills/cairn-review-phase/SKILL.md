---
name: cairn-review-phase
description: Run Cairn's Review phase after a non-trivial implementation or when the user requests a full quality and security review. Detect available checks, review the actual diff, and report evidence and gaps; do not use for a read-only explanation with no review request.
metadata:
  version: "0.3.0"
---

# cairn: Review-phase skill

Drive the **Review** phase of the six-phase checklist: inspect the
actual change, run relevant project checks, perform quality and
security passes, check governing-proposal conformance when applicable, and
report evidence and remaining gaps.

## When to use this skill

- After a non-trivial implementation, before handoff or commit.
- From `cairn-autonomous-round` or `cairn-autonomous-loop` step 7.
- When the user asks "review this diff" or "what does the
  security posture look like for this change?"

## Do NOT use for

- Trivial changes (doc typos, whitespace): skip and note the
  skip in the journal.
- Code that hasn't been implemented yet — review is post-Build,
  pre-Ship, not a proposal review.

## The protocol

### 1. Detect available tools

Before proposing a plan, inventory what's reachable. Check:

| Category | Evidence to inspect | Examples |
|----------|---------------------|----------|
| Project gates | Repository instructions and scripts | `just check`, `make test`, language test/lint commands |
| Independent review | Available agent/client capability | subagent, peer-review command, separate review model |
| Static security | Installed tools and project config | `semgrep`, `bandit`, `gitleaks` |
| Dependency risk | Changed lockfiles/manifests | ecosystem audit command, maintainer review |

Record the detection pass in the session journal's review
subsection:

```markdown
**Review capabilities detected:**
- Project gates: `make test`, `ruff check`
- Independent reviewer: subagent available
- Security: `semgrep` configured
- Dependency audit: not applicable (no manifest changes)
```

### 2. Propose a review plan

Short, concrete, tailored to what's available. Example:

```
Detected: project tests, an independent reviewer, and semgrep.

1. Self-review (always).
2. Quality: project tests plus an independent review of the diff.
3. Security: configured static scan plus a trust-boundary review
   scoped to what changed.

Proceed? (Y / customize / skip <which>)
```

Ask before running a check only when it needs new authority, external
access, meaningful cost, or a state change. Otherwise proceed under the
user's review request and project instructions.

### 3. Quality pass (ALWAYS mandatory)

Run the project's canonical relevant gates and inspect the diff for:

- **Regressions and edge cases.** Check error paths, compatibility,
  public contracts, and missing tests.
- **Self-review against the diff.** Manual read-through with
  the governing principles in mind — scope creep, unrelated
  changes, missing docstrings on public API, comments
  explaining *what* instead of *why*.

For non-trivial changes, use an independent reviewer when the client
provides one. Record which checks ran and their results.

### 4. Security pass (ALWAYS mandatory)

Always consider security, but keep the depth proportional to the
change. If tools are absent or irrelevant, do a focused manual pass.

**Tool-based path:**

- Run detected SAST tools scoped to changed files.
- Summarise findings: severity distribution, any high/critical
  items that block the commit.

**Manual fallback (when no tool is available):**

Read the diff and explicitly consider the applicable boundaries:

- **Trust boundaries** — injection, access control, authentication,
  authorization, unsafe deserialization, path/command handling, and
  external input where relevant.
- **Secret handling** — no new secrets committed; env/config
  files carry placeholders only.
- **Authz/authn boundaries** — no privilege escalation paths;
  new endpoints have correct auth; role checks before
  side-effecting calls.
- **Input validation at system edges** — user input, network
  boundaries, file reads, external commands. Trust boundaries
  respected.
- **Dependency changes** — any new transitive dep worth
  flagging? License-compatible? Maintained?

Log the manual pass in the journal:

```markdown
**Security pass — manual (no tooling available):**

- OWASP Top 10 scan: no concerns (injection paths use existing
  Repo with typed params; no new auth surface).
- Secrets: clean — no credentials or tokens in diff.
- Authz: N/A (no new endpoints).
- Input validation: new `create_task/3` validates slug +
  title; inherits existing path-traversal guards from
  `TaskDefinition`.
- Deps: no changes.
```

### 5. Second opinion

For non-trivial changes (new modules, API contracts, security-
adjacent code): dispatch a second-opinion reviewer.

For small diffs: skip, note the skip in the journal.

Use project policy and consequence, not a line-count proxy, to decide.
Security boundaries, compatibility changes, persistent formats, and
multi-component behavior are non-trivial even when the diff is small.

### 6. EP conformance when applicable

If `.ep-kit` exists and the change cites an Accepted or Partial proposal, use
`cairn-strata-interop` to resolve the configured proposal directory. Compare
the implementation with its Goals, Non-goals, Design constraints, and relevant
Decision Log entries. Record stable references such as `EP-0017 D3`, not a
copy of the Decision Log. Any contradiction is a blocker that returns to
proposal governance even when normal tests pass.

If that sibling skill is unavailable, read `.ep-kit` directly as its public
`key=value` contract (`dir` defaults to `docs/eps`), then follow the installed
proposal process and run the same conformance comparison. Stop on malformed
configuration rather than guessing the proposal location.

### 7. Record in the journal

If an active Cairn session journal exists, its review subsection gets:

```markdown
**Review:**

- Tools detected: <list>.
- Quality: <tool(s)> — <result>.
- Security: <tool(s) OR "manual">. <summary of concerns>.
- Second opinion: <who/what> OR "skipped (trivial)".
- EP conformance: <reference + result> OR "not applicable".
- Blockers: <any>, OR "none".
```

If any blocker is found, the round pauses (autonomous) or the
user is asked to decide (interactive) — do NOT commit through
unresolved blockers.

## Integration

This skill is invoked from:

- `cairn-autonomous-round` / `cairn-autonomous-loop` step 7.
- The user's interactive "review this" request.
- The six-phase checklist's Review phase (manually).

When an independent-review capability exists, use it with a bounded
definition of done and verify its findings before adopting them. When it
does not, report that validation gap rather than inventing a reviewer.
