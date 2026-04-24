# cairn

> A cairn is a pile of stones travelers add to as they pass, marking
> the way for those behind them. This project is a kit for building
> that kind of trail through a software project — structured session
> journals, a rolling punch list, and an autonomous-round cadence
> that turns open-ended AI-agent collaboration into a legible
> sequence of waypoints.

**Status:** alpha. Used in production on one project (Glorbo); shape
is being extracted and generalized. API and layout may shift.

## What cairn is

A small bundle of **templates**, **skills**, **slash commands**, and
**sub-agent definitions** that codify a specific flavor of AI-agent
development workflow:

1. **Session journals** (`docs/sessions/<date>-<topic>.md`) — a
   detailed narrative log of each working session. Written as you
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
   commit, optionally re-schedule and pick up again.
5. **CLAUDE.md / AGENTS.md / GEMINI.md template** — project-level
   instructions that wire the above into whichever CLI you use.

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

- **Proposals with decision logs** — that's [ep-kit](../ep-kit/)'s
  job. cairn's templates reference ep-kit; the two are designed to
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
*what was decided and why*, but not *what was tried, what was
skipped, and what the agent had to guess at* during the session.
cairn's session journal is the layer between commit history and
proposal documents. It captures:

- What the user asked for, paraphrased.
- What the agent did without asking.
- Gates that were / weren't run and why.
- Yes/no questions parked for the user's review.
- A running trail of SHAs so the log and `git log` agree.

It's the part that *feels* most like working with a colleague who
keeps a notebook — not because they're overly formal, but because
shared context makes future sessions more productive.

## Quickstart (Claude Code)

```bash
# One-time: install cairn into your Claude Code plugin directory.
# (If you cloned this repo directly, add it as a plugin instead.)
mkdir -p ~/.claude/plugins/user/
cp -r /path/to/cairn ~/.claude/plugins/user/

# Per-project: scaffold the workflow into a project directory.
cd /your/project
/path/to/cairn/install.sh

# This creates:
#   docs/sessions/          (where session journals live)
#   docs/todo.md            (the rolling punch list)
#   CLAUDE.md               (or merges into an existing one)
```

Then inside Claude Code:

```
/cairn-init        Scaffold into the current project (same as install.sh)
/cairn-session     Open or append to today's session log
/cairn-round       One autonomous cycle, stop when done
/cairn-loop        Repeated cycles until a stop criterion is met
```

## Quickstart (other CLIs)

cairn's substance is plain markdown. Pointing any LLM-CLI at the
cairn templates — via `GEMINI.md`, `AGENTS.md`, or whatever your
tool calls its instructions file — gives you ~80% of the Claude
Code experience. See:

- [docs/for-claude-code.md](docs/for-claude-code.md)
- [docs/for-gemini-cli.md](docs/for-gemini-cli.md)
- [docs/for-codex-cli.md](docs/for-codex-cli.md)
- [docs/for-opencode.md](docs/for-opencode.md)

The slash commands and subagents are Claude-specific conveniences.
The templates, skills, and workflow docs are portable.

## Layout

```
cairn/
├── .claude-plugin/plugin.json    Claude Code plugin manifest
├── commands/                     Claude Code slash commands
│   ├── cairn-init.md             Scaffold into a project
│   ├── cairn-session.md          Open or append today's journal
│   ├── cairn-round.md            One autonomous cycle
│   └── cairn-loop.md             Repeating cycles
├── skills/                       Claude Code skills
│   ├── session-log/SKILL.md
│   ├── autonomous-round/SKILL.md
│   ├── autonomous-loop/SKILL.md
│   ├── review-phase/SKILL.md     Quality + security pass orchestrator
│   ├── build-user-profile/SKILL.md
│   ├── build-project-profile/SKILL.md
│   └── close-session/SKILL.md
├── agents/                       Claude Code sub-agents
│   ├── prior-session-digest.md   Compress recent journals → ~800 words
│   ├── autonomous-planner.md     Recommend next bounded task
│   └── review-runner.md          Run detected review tools in parallel
├── templates/                    CLI-agnostic project templates
│   ├── CLAUDE.md                 Copied into target projects
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
├── examples/                     Sample session logs etc.
├── CHANGELOG.md
├── LICENSE                       Apache-2.0
└── README.md                     This file
```

## Companion projects

- **[ep-kit](../ep-kit/)** — structured enhancement proposals with
  decision logs, bidirectional links, and a CI-friendly validator.
  cairn's `templates/CLAUDE.md` references ep-kit; install both
  together for the full workflow.

## License

Apache-2.0. Use it in any project.
