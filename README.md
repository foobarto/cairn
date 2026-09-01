# cairn

> A cairn is a pile of stones travelers add to as they pass, marking
> the way for those behind them. This project is a kit for building
> that kind of trail through a software project — structured session
> journals, a rolling punch list, and an autonomous-round cadence
> that turns open-ended AI-agent collaboration into a legible
> sequence of waypoints.

**Status:** `0.3.x` stabilization. Used in production on one project (Glorbo).
This is planned as the final pre-1.0 release line: barring compatibility issues
discovered during 0.3.x, the next release line will be 1.0.

The 0.3.x series establishes the candidate public surface—canonical skill
names, installer flags and non-overwrite behavior, project artifact paths, and
plugin coordinates. It may still make narrowly scoped compatibility fixes;
1.0 will mark that surface as stable.

## What cairn is

A portable bundle of **Agent Skills**, templates, workflow documents, and
optional client adapters that codifies a specific flavor of AI-agent
development workflow:

1. **Session journals** (`docs/sessions/<date>-<topic>.md`) — a
   concise project-facing record of each working session. Written as you
   go, not retroactively. Per-task entries have standard sub-
   sections (*What shipped*, *Design calls I made without you*,
   *Gates*, *Skipped / not done*), honest about shortcuts, with
   concrete SHAs and yes/no questions parked at the end for the
   user's later review.
2. **Rolling punch list** (`docs/todo.md`) — P0/P1/P2/P3 tiers +
   a running "Shipped this cycle" log. Noticed-but-not-yet-shipped
   items that don't warrant a full proposal.
3. **Six-phase feature checklist** — Spec → Plan → Build → Test →
   Review → Ship. Ship means *the code shipped AND every doc that
   should reflect the change has been updated in the same session*.
4. **Autonomous-round cadence** — when you need to run the agent
   unattended for a while: pick one bounded task from the punch
   list, log the decisions taken without asking, gate with tests,
   commit when authorized, and continue only through a capability the
   current client actually exposes.
5. **Portable agent-instructions template** — installed as `AGENTS.md` by
   default, or as the filename expected by a selected client.

## Governing principles (backbone)

cairn's four governing principles — adapted from
[Karpathy's guidelines](https://karpathy.bearblog.dev/dev/) — are
the backbone that every artefact is shaped around:

1. **Think before coding.** Surface assumptions and tradeoffs.
2. **Simplicity first.** Minimum that solves the problem.
3. **Surgical changes.** Touch only what you must.
4. **Goal-driven execution.** Define success concretely; loop
   until verified.

These override the shapes: if a template, skill, or command
conflicts with a principle, the principle wins. Full text at
[templates/workflow/governing-principles.md](templates/workflow/governing-principles.md).

## What cairn does NOT include

- **Proposals with decision logs** — that's [Strata](https://github.com/foobarto/strata)'s
  job. Cairn and Strata are designed to
  work together.
- **Test framework, build tool, or language opinions** — cairn is
  language-agnostic. It's about *how you work*, not *what you
  build*.
- **A knowledge-graph tool** — cairn's templates mention one as a
  hook point, but providing the tool is out of scope (Glorbo uses
  [graphify](https://github.com/foobarto/graphify); others can
  substitute anything).

## Why the shape

Chat contexts rot. Commit messages are too short. GEPs/ADRs record
*what was decided and why*, but not implementation evidence, scope changes,
validation gaps, and unresolved handoff questions from the session.
cairn's session journal is the layer between commit history and
proposal documents. It captures:

- What the user asked for, paraphrased.
- What the agent did without asking.
- Gates that were / weren't run and why.
- Yes/no questions parked for the user's review.
- A running trail of SHAs so the log and `git log` agree.

It is a professional operational record, not a transcript or private notebook:
future contributors get the context they need without exploratory deliberation,
personal information, host details, or unrelated methodology.

## Quickstart (Agent Skills clients)

Clone Cairn and scaffold a project:

```bash
git clone https://github.com/foobarto/cairn ~/tools/cairn
cd /your/project
~/tools/cairn/install.sh
```

The installer writes portable skills under `.agents/skills/`, an `AGENTS.md`
entry point, and the workflow files under `docs/`. Existing files are skipped.
Use `--agents-file CLAUDE.md`, `--agents-file GEMINI.md`, or another safe
project-relative path when a client expects a different entry point. Use `--no-skills` when
skills are supplied by a plugin or another managed source, and
`--upgrade-skills` to refresh only Cairn-owned skill files.

Versions before 0.3 used nonconforming skill directory names without the
`cairn-` prefix. Run `--upgrade-skills` once to migrate those known directories
in place and refresh Cairn-owned files; unrelated files inside them are
preserved. Migration first verifies the old skill's Cairn frontmatter. If both
old and new Cairn directories exist, the installer stops before writing and
requires manual reconciliation.

`.agents/skills/` is the documented cross-client discovery convention, not a
requirement of the [Agent Skills specification](https://agentskills.io/specification).
Confirm discovery in the selected client; Gemini CLI and OpenCode document the
alias directly, while other clients may require their native skill or plugin
installation route.

## Codex plugin

For native Codex marketplace installation:

```bash
codex plugin marketplace add foobarto/cairn
codex plugin add cairn@cairn
```

The plugin exposes the same canonical `skills/` packages. Use the shell
installer when you also want the workflow documents and `AGENTS.md`; pass
`--no-skills` if the plugin already supplies the skills.

## Claude Code plugin

**One-time: install the plugin.** cairn ships as a self-contained
plugin marketplace, so installation is two slash commands run
inside Claude Code:

```
/plugin marketplace add foobarto/cairn
/plugin install cairn@cairn
```

(Developing against a local clone instead? Launch Claude Code with
`claude --plugin-dir /path/to/cairn`. Copying the repo into
`~/.claude/plugins/` by hand does **not** work — Claude Code only
discovers plugins through a marketplace or `--plugin-dir`.)

**Per-project:** run `/cairn-init` from inside the project. It is the
Claude-specific interactive adapter and can merge Cairn sections into an
existing `CLAUDE.md`. The shell installer is the portable, non-overwriting
path and intentionally has different merge behavior.

If the plugin already supplies skills but you prefer the shell scaffolder, use
`install.sh --agents-file CLAUDE.md --no-skills` to avoid a stale project-local
copy shadowing the plugin.

Then inside Claude Code:

```
/cairn-init        Claude-specific interactive scaffolding/merge
/cairn-session     Open or append to today's session log
/cairn-round       One autonomous cycle, stop when done
/cairn-loop        Repeated cycles until a stop criterion is met
```

## Client adapters

Cairn's canonical skills and workflow are client-neutral. The adapter docs
cover native discovery, instruction filenames, and capability gaps:

- [docs/for-claude-code.md](docs/for-claude-code.md)
- [docs/for-gemini-cli.md](docs/for-gemini-cli.md)
- [docs/for-codex-cli.md](docs/for-codex-cli.md)
- [docs/for-opencode.md](docs/for-opencode.md)

Claude commands and subagent definitions are optional adapters. Canonical
behavior lives in `skills/` and `templates/workflow/`.

## Optional companion: Strata

Cairn manages the life of the work; [Strata](https://github.com/foobarto/strata)
manages the life of architectural decisions. Cairn is complete without it and
never installs it automatically. When `.ep-kit` exists, Cairn reads that public
config instead of assuming `docs/eps/`, uses the installed lifecycle as
authoritative, promotes architectural P3 items into Strata, materializes
approved proposal scope as bounded P1 work, checks EP conformance during
Review, and reconciles referenced proposal state during Ship/close.

Proposal design, alternatives, Decision Logs, relationships, and lifecycle
stay canonical in Strata. Cairn journals and todo items use stable references;
they do not duplicate that material.

Strata was named EP Kit through version 1.2.0; the rename ships in Strata 1.3.0.
Its compatibility protocol keeps the `.ep-kit` configuration filename,
`kit_version` key, `EP-NNNN` citations, and installed `ep-kit*` skill names.
The former `foobarto/ep-kit` repository URL redirects to `foobarto/strata`.

## Layout

```
cairn/
├── .agents/plugins/
│   └── marketplace.json          Codex marketplace catalogue
├── .claude-plugin/
│   ├── plugin.json               Claude Code plugin manifest
│   └── marketplace.json          Single-plugin marketplace catalog
├── .codex-plugin/
│   └── plugin.json               Codex plugin manifest
├── .github/workflows/lint.yml    CI: spec, tests, manifests, typing, shellcheck
├── commands/                     Claude Code slash commands
│   ├── cairn-init.md             Scaffold into a project
│   ├── cairn-session.md          Open or append today's journal
│   ├── cairn-round.md            One autonomous cycle
│   └── cairn-loop.md             Repeating cycles
├── skills/                       Canonical Agent Skills
│   ├── cairn-session-log/SKILL.md
│   ├── cairn-autonomous-round/SKILL.md
│   ├── cairn-autonomous-loop/SKILL.md
│   ├── cairn-review-phase/SKILL.md
│   ├── cairn-strata-interop/SKILL.md
│   ├── cairn-build-user-profile/SKILL.md
│   ├── cairn-build-project-profile/SKILL.md
│   └── cairn-close-session/SKILL.md
├── agents/                       Claude Code sub-agents
│   ├── prior-session-digest.md   Compress recent journals → ~800 words
│   ├── autonomous-planner.md     Recommend next bounded task
│   └── review-runner.md          Run detected review tools in parallel
├── templates/                    CLI-agnostic project templates
│   ├── agent-instructions.md     Copied under the selected client filename
│   ├── session-template.md
│   ├── todo.md
│   ├── user-profile.md           Global user profile (synthesis)
│   ├── project-profile.md        Per-project stances (declarative)
│   └── workflow/
│       ├── governing-principles.md
│       ├── six-phase-checklist.md
│       └── autonomous-protocol.md    (covers round + loop)
├── docs/
│   ├── workflow.md               The full picture
│   ├── for-claude-code.md        CLI adapter: Claude Code
│   ├── for-gemini-cli.md         CLI adapter: Gemini CLI
│   ├── for-codex-cli.md          CLI adapter: Codex CLI
│   └── for-opencode.md           CLI adapter: opencode
├── install.sh                    Per-project scaffolder
├── tests/                        Typed validator + installer regression tests
├── evals/                        Harness-neutral behavioral scenarios
├── scripts/
│   └── validate_frontmatter.py   Frontmatter linter (run in CI)
├── examples/                     Sample session logs etc.
├── CHANGELOG.md
├── CONTRIBUTING.md               How to add skills/commands/agents
├── LICENSE-MIT, LICENSE-APACHE   Dual-licensed: MIT OR Apache-2.0
└── README.md                     This file
```

## Development

Cairn's validator and installer are runtime code. CI checks canonical and
installed skills, typed Python, plugin metadata, installer behavior, and shell
portability. Install development dependencies, then run:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_frontmatter.py --strict
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install.sh
python3 -m mypy
shellcheck --severity=warning install.sh tests/test_install.sh
```

## License

Licensed under either of

- Apache License, Version 2.0
  ([LICENSE-APACHE](LICENSE-APACHE) or
  <http://www.apache.org/licenses/LICENSE-2.0>)
- MIT license
  ([LICENSE-MIT](LICENSE-MIT) or
  <http://opensource.org/licenses/MIT>)

at your option. Use it in any project.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms
or conditions.
