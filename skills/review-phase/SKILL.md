---
name: cairn-review-phase
version: 0.2.0
description: Use during the Review phase of the six-phase checklist — detect available review tools in the project environment, propose a review plan, run quality + security passes (both mandatory), and summarise findings for the session journal. Triggers at natural review seams — after implementation, before commit; when the user asks "review this diff"; or automatically from autonomous-round / autonomous-loop step 7. Quality alone is not enough; security pass is always required even if the only tool available is a manual diff read.
---

# cairn: Review-phase skill

Drive the **Review** phase of the six-phase checklist: detect
available review tools, propose a plan, run quality + security
passes, summarise for the session journal.

## When to use this skill

- After implementation, before commit, in a normal dev cycle.
- Automatically from autonomous-round / autonomous-loop step 7.
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

| Category | Check                                  | Canonical tools                    |
|----------|----------------------------------------|------------------------------------|
| Codex review | `command -v codex`                 | `codex exec` second-opinion        |
| Claude plugins | Skill listing                    | `superpowers:code-reviewer`        |
| Security orchestrator | Plugin listing            | `security-kit`                     |
| SAST (static) | `command -v` + project fingerprint | `semgrep`, `bandit`, `gitleaks`  |
| Language-specific linter | Project fingerprint    | `mix credo`, `cargo clippy`, `ruff`, `golangci-lint`, `eslint` |
| Project gate | Scan for aliases                  | `mix precommit`, `just check`, `make review`, `pnpm run check` |

Record the detection pass in the session journal's review
subsection:

```markdown
**Review tools detected:**
- Codex CLI: ✓ (`codex exec` available)
- Security: semgrep ✓, security-kit ✓
- Language: mix credo, mix precommit
- Project gate: mix precommit
```

### 2. Propose a review plan

Short, concrete, tailored to what's available. Example:

```
Detected: codex, semgrep, mix precommit. Proposed review:

1. Self-review (always).
2. Quality: `mix precommit` + `codex exec` second opinion.
3. Security: `semgrep --config=auto` scoped to changed files +
   manual diff read against OWASP Top 10, secret handling,
   authz/authn boundaries.

Proceed? (Y / customize / skip <which>)
```

Interactive sessions: surface the plan, wait for Y.
Autonomous rounds: proceed unless the project profile says
otherwise.

### 3. Quality pass (ALWAYS mandatory)

Run the project's canonical gate (`mix precommit`, `pnpm run
check`, etc.) and at least one of:

- **Second-opinion reviewer.** `codex exec "review this diff"`
  or `superpowers:code-reviewer` sub-agent dispatch.
- **Self-review against the diff.** Manual read-through with
  the governing principles in mind — scope creep, unrelated
  changes, missing docstrings on public API, comments
  explaining *what* instead of *why*.

Record which option ran and the result in the journal.

### 4. Security pass (ALWAYS mandatory)

Never skip. If tools are absent, do a manual security pass.

**Tool-based path:**

- Run detected SAST tools scoped to changed files.
- If `security-kit` is installed, use its orchestrator skill.
- Summarise findings: severity distribution, any high/critical
  items that block the commit.

**Manual fallback (when no tool is available):**

Read the diff and explicitly consider:

- **OWASP Top 10** — injection, broken access control, crypto
  failures, auth weaknesses, misconfigurations, vulnerable
  dependencies, ID/auth failures, software/data integrity,
  logging/monitoring, SSRF.
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

### 5. Second opinion (optional for small changes)

For non-trivial changes (new modules, API contracts, security-
adjacent code): dispatch a second-opinion reviewer.

For small diffs: skip, note the skip in the journal.

Default rule: if the diff touches more than ~200 lines across
2+ files, require second opinion. Override via the project
profile ("Quality bar: always require second opinion" or
"small fixes only need self-review").

### 6. Record in the journal

The review subsection of today's session journal entry gets:

```markdown
**Review:**

- Tools detected: <list>.
- Quality: <tool(s)> — <result>.
- Security: <tool(s) OR "manual">. <summary of concerns>.
- Second opinion: <who/what> OR "skipped (trivial)".
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

The heavy lifting of actually running parallel tools in
isolation is the `review-runner` sub-agent's job if available;
this skill orchestrates + summarises for the main context.
