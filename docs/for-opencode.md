# Cairn on OpenCode

OpenCode discovers project Agent Skills under `.agents/skills/` and reads
`AGENTS.md`, so Cairn's defaults are the native portable path:

```bash
git clone https://github.com/foobarto/cairn ~/tools/cairn
cd /your/project
~/tools/cairn/install.sh
```

Confirm the installed `cairn-*` skills through the current OpenCode skill
interface. OpenCode's [Agent Skills documentation](https://opencode.ai/docs/skills)
also lists `.opencode/skills/` and supports configured sources; pass
`--skill-dir .opencode/skills` if the project prefers the client-specific
location.

Cairn's Claude `commands/` and `agents/` folders are optional adapters and are
not needed. The canonical skills use only capabilities they can verify. In
particular, loop continuation, subagents, review tooling, and memory all
degrade explicitly when unavailable.
