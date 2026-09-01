# Contributing

Thanks for considering a contribution. Cairn is a portable Agent Skills
workflow with native Codex and Claude Code plugin adapters, templates,
commands, and optional
sub-agent definitions (see [README.md](./README.md) for the shape and
[`docs/workflow.md`](docs/workflow.md) for the full picture). There's no
application service; the small shell/Python utilities scaffold and validate
the Markdown workflow artifacts.

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
| Skills              | `skills/<name>/SKILL.md` | Agent Skills spec; directory must equal `name` |
| Slash commands      | `commands/<name>.md`     | required: `description`; optional: `allowed-tools` (name = filename) |
| Sub-agents          | `agents/<name>.md`       | required: `name` (slug), `description`; optional: `tools` |
| Project templates   | `templates/`             | — copied into target projects by `install.sh` |
| Workflow docs       | `templates/workflow/`    | — the protocol substance |
| CLI adapter docs     | `docs/for-*.md`          | — per-CLI porting notes |
| Plugin manifests    | `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Client manifests and marketplaces |

## Editing skills, commands, and agents

The `description` is load-bearing: clients use it to decide whether to activate
a skill, so describe both what it does and when it applies. Rules the
frontmatter lint
([`scripts/validate_frontmatter.py`](scripts/validate_frontmatter.py))
enforces:

- **Skills** follow the [Agent Skills specification](https://agentskills.io/specification):
  `name` and `description` are required; names match
  `^[a-z0-9]+(-[a-z0-9]+)*$`, are at most 64 characters, and equal the parent
  directory. Put Cairn's version string under `metadata.version`, not a
  top-level `version` field.
- **Agents** require `name` and `description`; agent names are lowercase slugs.
- **Commands** require only `description` — the command name is the filename,
  so `commands/cairn-round.md` is invoked as `/cairn-round`.
- Skill descriptions must be non-empty and at most 1024 characters. Cairn
  warns below 30 characters because such triggers are usually ambiguous.
- `allowed-tools` is optional and cairn's skills deliberately omit it (the
  workflow skills need broad access); commands pin a tool list where it helps.

## Adding a new artefact

- **Skill:** create `skills/<name>/SKILL.md` with the frontmatter above. The
  installer discovers canonical skill directories automatically. Keep the
  package self-contained: do not link back to repository-only paths that will
  disappear under `.agents/skills/`.
- **Command:** create `commands/<name>.md`. Keep it a thin entry point that
  delegates to a skill where there's shared substance.
- **Agent:** create `agents/<name>.md`. Agents should be read-mostly and
  return a structured summary so they keep the main agent's context clean.
- **Template:** add it under `templates/`, then wire it into `install.sh`
  (`copy_if_missing`) and document it in the README layout + the `/cairn-init`
  table so the script and the docs agree.

## Plugin manifests

Claude uses `.claude-plugin/plugin.json` plus its marketplace and auto-discovers
`commands/`, `skills/`, and `agents/`. Codex uses
`.codex-plugin/plugin.json`, whose `skills` path points at the same canonical
packages, plus `.agents/plugins/marketplace.json`.

In the repository Codex marketplace, `source.url: "./"` deliberately resolves
to the installed marketplace checkout root. This preserves the selected
marketplace ref; do not replace it with a separate default-branch fetch without
an explicit distribution change. All manifests must stay valid JSON and the
development versions must remain aligned with the next changelog entry.

## Checks

Run the same checks CI runs ([`.github/workflows/lint.yml`](.github/workflows/lint.yml))
before opening a PR:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_frontmatter.py --strict
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install.sh
python3 -m mypy
shellcheck --severity=warning install.sh tests/test_install.sh
```

Behavioral activation boundaries live under `evals/`; follow its README when
changing descriptions, autonomy, proposal gates, or persistence authority.

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
- Treat 0.3.x as the final planned pre-1.0 stabilization line. Compatibility
  findings may receive another 0.3.x release; otherwise the next release line
  is 1.0, which freezes the documented skill names, installer surface,
  artifact paths, and plugin coordinates.

## License

By contributing you agree your work is dual-licensed under both MIT and
Apache-2.0; recipients may choose either license. See the Contribution note in
[README.md](./README.md).
