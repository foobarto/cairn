# Contributing

Thanks for considering a contribution. cairn is a Claude Code **plugin** —
a bundle of templates, skills, slash commands, and sub-agent definitions
that codify a workflow (see [README.md](./README.md) for the shape and
[`docs/workflow.md`](docs/workflow.md) for the full picture). There's no
runtime code; the substance is plain Markdown plus a shell scaffolder.

Report vulnerabilities through the repository Security tab or the
[account-wide security policy](https://github.com/foobarto/.github/blob/main/SECURITY.md),
not a public issue. Participation is subject to the account-wide
[Code of Conduct](https://github.com/foobarto/.github/blob/main/CODE_OF_CONDUCT.md).

## The governing principles apply to changes too

cairn's four [governing principles](templates/workflow/governing-principles.md)
— think before coding, simplicity first, surgical changes, goal-driven
execution — are the backbone the artefacts are shaped around. They're also
how to judge a contribution: keep changes minimal and surgical, preserve the
existing terse doc voice, and make sure every artefact that *should* reflect
a change is updated in the same PR (the six-phase checklist's "Ship" bar).

## Where things live

| Artefact            | Path                  | Frontmatter |
|---------------------|-----------------------|-------------|
| Skills              | `skills/<name>/SKILL.md` | required: `name` (slug), `description`; optional: `version` |
| Slash commands      | `commands/<name>.md`     | required: `description`; optional: `allowed-tools` (name = filename) |
| Sub-agents          | `agents/<name>.md`       | required: `name` (slug), `description`; optional: `tools` |
| Project templates   | `templates/`             | — copied into target projects by `install.sh` |
| Workflow docs       | `templates/workflow/`    | — the protocol substance |
| CLI adapter docs     | `docs/for-*.md`          | — per-CLI porting notes |
| Plugin manifests    | `.claude-plugin/`        | `plugin.json`, `marketplace.json` |

## Editing skills, commands, and agents

The `description` is load-bearing: Claude Code matches against it to decide
whether to invoke a skill/agent, so **lead with "when to use" phrasing**, not
"what this does." Rules the frontmatter lint
([`scripts/validate_frontmatter.py`](scripts/validate_frontmatter.py))
enforces:

- **Skills & agents** require `name` and `description`. `name` must be a valid
  slug (`[a-z][a-z0-9-]*`). Skill names are conventionally `cairn-`prefixed
  (`cairn-session-log`); agent names are bare (`review-runner`).
- **Commands** require only `description` — the command name is the filename,
  so `commands/cairn-round.md` is invoked as `/cairn-round`.
- `description` should be ≥ 30 chars and < 1024 (Claude Code truncates the
  tail). Outside that range is a warning, not a failure.
- `allowed-tools` is optional and cairn's skills deliberately omit it (the
  workflow skills need broad access); commands pin a tool list where it helps.

## Adding a new artefact

- **Skill:** create `skills/<name>/SKILL.md` with the frontmatter above. If it
  scaffolds files into a project, also teach `install.sh` (and the
  `/cairn-init` command) to copy any new template.
- **Command:** create `commands/<name>.md`. Keep it a thin entry point that
  delegates to a skill where there's shared substance.
- **Agent:** create `agents/<name>.md`. Agents should be read-mostly and
  return a structured summary so they keep the main agent's context clean.
- **Template:** add it under `templates/`, then wire it into `install.sh`
  (`copy_if_missing`) and document it in the README layout + the `/cairn-init`
  table so the script and the docs agree.

## Plugin manifests

`plugin.json` is the plugin manifest; `marketplace.json` is the single-plugin
marketplace catalog that makes `/plugin marketplace add foobarto/cairn` work.
Both must stay valid JSON (CI checks this — a broken manifest breaks the whole
plugin). `commands/`, `skills/`, and `agents/` are auto-discovered by
directory convention, so adding a file there needs no manifest change. There's
no `version` in `plugin.json` on purpose: git-hosted installs version by commit
SHA, and releases are tracked in `CHANGELOG.md`.

## Checks

Run the same checks CI runs ([`.github/workflows/lint.yml`](.github/workflows/lint.yml))
before opening a PR:

```sh
python3 scripts/validate_frontmatter.py            # skill/command/agent frontmatter
python3 -m json.tool .claude-plugin/plugin.json > /dev/null      # manifest valid?
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null # manifest valid?
shellcheck --severity=warning install.sh           # shell lint (matches CI)
```

`validate_frontmatter.py` needs PyYAML (`pip install pyyaml`).

## Pull requests

`main` is protected by a repository ruleset: changes that touch
`.github/workflows/` require a PR rather than a direct push. When in doubt,
open a PR — CI runs on it and gates the merge.

## Commit style & releases

- Prefix commits with a short type: `feat:`, `fix:`, `docs:`, `ci:`,
  `chore:`, `refactor:`. Keep the subject under 70 chars; put context in
  the body.
- Record notable changes in [`CHANGELOG.md`](./CHANGELOG.md)
  ([Keep a Changelog](https://keepachangelog.com/) format,
  [SemVer](https://semver.org/) versions). Cut a release by finalising the
  version's `CHANGELOG.md` entry and stamping its date; tag `main` with the
  `vX.Y.Z` string if you want a pinned install version (otherwise git-hosted
  installs track the commit SHA).

## License

By contributing you agree your work is dual-licensed under MIT OR Apache-2.0,
matching the project (see the Contribution note in [README.md](./README.md)).
