# Cairn on Gemini CLI

Gemini CLI natively discovers Agent Skills from workspace `.agents/skills/`
and uses `GEMINI.md` for project context.

```bash
git clone https://github.com/foobarto/cairn ~/tools/cairn
cd /your/project
~/tools/cairn/install.sh --agents-file GEMINI.md
```

In Gemini CLI, trust the workspace if appropriate, then run `/skills list` to
confirm the `cairn-*` skills. Use `/skills reload` after upgrading installed
skills. These commands and discovery paths are documented in Gemini CLI's
[Agent Skills guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md).

Claude-specific slash commands and subagent definitions are not installed as
Gemini adapters. Invoke the canonical skills by relevant natural-language
requests or the client's skill controls. Remote/subagent, memory, and
continuation features are optional capabilities; Cairn tests for them rather
than assuming they exist.
