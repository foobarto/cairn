#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/.tmp"
TEST_TMP="$(mktemp -d "$ROOT/.tmp/install-tests.XXXXXX")"
trap 'rm -rf "$TEST_TMP"' EXIT

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

expect_failure() {
    if "$@"; then
        fail "command unexpectedly succeeded: $*"
    fi
}

assert_empty() {
    local directory="$1"
    if [[ -n "$(ls -A "$directory")" ]]; then
        fail "expected no writes under $directory"
    fi
}

echo "default portable install"
mkdir -p "$TEST_TMP/default"
XDG_CONFIG_HOME="$TEST_TMP/xdg" "$ROOT/install.sh" --non-interactive "$TEST_TMP/default" >/dev/null
[[ -f "$TEST_TMP/default/AGENTS.md" ]] || fail "default AGENTS.md missing"
[[ ! -e "$TEST_TMP/xdg" ]] || fail "non-interactive default wrote a global profile"
grep -q '../../AGENTS.md' "$TEST_TMP/default/docs/sessions/README.md"
skill_files=("$TEST_TMP/default/.agents/skills"/*/SKILL.md)
[[ ${#skill_files[@]} -eq 8 ]] || fail "expected eight installed skills"
[[ -x "$TEST_TMP/default/.agents/skills/cairn-strata-interop/scripts/resolve_strata.py" ]] || fail "Strata resolver lost executable mode"
"$ROOT/scripts/validate_frontmatter.py" --root "$TEST_TMP/default" --skills-root .agents/skills --skills-only --strict >/dev/null
if command -v agentskills >/dev/null 2>&1; then
    for skill_path in "$TEST_TMP/default/.agents/skills"/*; do
        agentskills validate "$skill_path" >/dev/null
    done
fi

echo "idempotency and managed skill upgrade"
printf '%s\n' 'project-owned instructions' > "$TEST_TMP/default/AGENTS.md"
printf '%s\n' 'stale skill' > "$TEST_TMP/default/.agents/skills/cairn-session-log/SKILL.md"
"$ROOT/install.sh" --non-interactive --profile-scope 4 "$TEST_TMP/default" >/dev/null
grep -qx 'project-owned instructions' "$TEST_TMP/default/AGENTS.md"

echo "legacy skill directories migrate only during managed upgrade"
mkdir -p "$TEST_TMP/legacy/.agents/skills/session-log"
printf '%s\n' '---' 'name: cairn-session-log' '---' > "$TEST_TMP/legacy/.agents/skills/session-log/SKILL.md"
printf '%s\n' 'project-owned resource' > "$TEST_TMP/legacy/.agents/skills/session-log/project-notes.md"
"$ROOT/install.sh" --non-interactive --profile-scope 4 --upgrade-skills "$TEST_TMP/legacy" >/dev/null
[[ ! -e "$TEST_TMP/legacy/.agents/skills/session-log" ]] || fail "legacy skill directory remained after upgrade"
cmp -s "$ROOT/skills/cairn-session-log/SKILL.md" "$TEST_TMP/legacy/.agents/skills/cairn-session-log/SKILL.md"
grep -qx 'project-owned resource' "$TEST_TMP/legacy/.agents/skills/cairn-session-log/project-notes.md"
grep -qx 'stale skill' "$TEST_TMP/default/.agents/skills/cairn-session-log/SKILL.md"
"$ROOT/install.sh" --non-interactive --profile-scope 4 --upgrade-skills "$TEST_TMP/default" >/dev/null
cmp -s "$ROOT/skills/cairn-session-log/SKILL.md" "$TEST_TMP/default/.agents/skills/cairn-session-log/SKILL.md"
grep -qx 'project-owned instructions' "$TEST_TMP/default/AGENTS.md"

echo "legacy migration preserves unrelated third-party skills"
mkdir -p "$TEST_TMP/third-party/.agents/skills/session-log"
printf '%s\n' '---' 'name: session-log' '---' > "$TEST_TMP/third-party/.agents/skills/session-log/SKILL.md"
"$ROOT/install.sh" --non-interactive --profile-scope 4 --upgrade-skills "$TEST_TMP/third-party" >/dev/null
grep -qx 'name: session-log' "$TEST_TMP/third-party/.agents/skills/session-log/SKILL.md"
[[ -f "$TEST_TMP/third-party/.agents/skills/cairn-session-log/SKILL.md" ]] || fail "canonical Cairn skill was not installed beside third-party skill"

echo "legacy and canonical Cairn copies require manual reconciliation"
mkdir -p "$TEST_TMP/legacy-conflict/.agents/skills/session-log" "$TEST_TMP/legacy-conflict/.agents/skills/cairn-session-log"
printf '%s\n' '---' 'name: cairn-session-log' '---' > "$TEST_TMP/legacy-conflict/.agents/skills/session-log/SKILL.md"
printf '%s\n' '---' 'name: cairn-session-log' '---' > "$TEST_TMP/legacy-conflict/.agents/skills/cairn-session-log/SKILL.md"
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --upgrade-skills "$TEST_TMP/legacy-conflict" >/dev/null 2>&1
[[ ! -e "$TEST_TMP/legacy-conflict/AGENTS.md" ]] || fail "legacy conflict failed after partial installation"

echo "nested instructions and custom skills path"
mkdir -p "$TEST_TMP/custom"
"$ROOT/install.sh" --non-interactive --profile-scope 4 --agents-file .github/copilot-instructions.md --skill-dir .gemini/skills "$TEST_TMP/custom" >/dev/null
[[ -f "$TEST_TMP/custom/.github/copilot-instructions.md" ]] || fail "custom instructions file missing"
grep -q '../../.github/copilot-instructions.md' "$TEST_TMP/custom/docs/sessions/README.md"
[[ -f "$TEST_TMP/custom/.gemini/skills/cairn-session-log/SKILL.md" ]] || fail "custom skills path missing"

echo "skills opt-out"
mkdir -p "$TEST_TMP/no-skills"
"$ROOT/install.sh" --non-interactive --profile-scope 4 --no-skills "$TEST_TMP/no-skills" >/dev/null
[[ ! -e "$TEST_TMP/no-skills/.agents" ]] || fail "--no-skills created .agents"

echo "private local profile"
mkdir -p "$TEST_TMP/local-profile"
"$ROOT/install.sh" --non-interactive --profile-scope 2 "$TEST_TMP/local-profile" >/dev/null
[[ -f "$TEST_TMP/local-profile/.cairn/user-profile.md" ]] || fail "local profile missing"
grep -qx '/.cairn/' "$TEST_TMP/local-profile/.gitignore"
python3 -m json.tool "$TEST_TMP/local-profile/.cairn/config.json" >/dev/null
printf '%s\n' '{"custom":"preserve"}' > "$TEST_TMP/local-profile/.cairn/config.json"
"$ROOT/install.sh" --non-interactive --profile-scope 2 "$TEST_TMP/local-profile" >/dev/null
grep -qx '{"custom":"preserve"}' "$TEST_TMP/local-profile/.cairn/config.json"

echo "explicit global profile remains sandboxed in the test XDG root"
mkdir -p "$TEST_TMP/global-profile"
XDG_CONFIG_HOME="$TEST_TMP/explicit-xdg" "$ROOT/install.sh" --non-interactive --profile-scope 1 "$TEST_TMP/global-profile" >/dev/null
[[ -f "$TEST_TMP/explicit-xdg/cairn/user-profile.md" ]] || fail "global profile missing"

echo "dry run writes nothing"
mkdir -p "$TEST_TMP/dry-run"
XDG_CONFIG_HOME="$TEST_TMP/dry-xdg" "$ROOT/install.sh" --dry-run --non-interactive --profile-scope 1 "$TEST_TMP/dry-run" >/dev/null
assert_empty "$TEST_TMP/dry-run"
[[ ! -e "$TEST_TMP/dry-xdg" ]] || fail "dry run wrote global profile"

echo "invalid input fails before mutation"
for case_name in invalid-scope tracked-scope escaped-agents escaped-skills singular-agent incompatible-options; do
    mkdir -p "$TEST_TMP/$case_name"
done
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 9 "$TEST_TMP/invalid-scope" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 3 "$TEST_TMP/tracked-scope" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --agents-file ../escape.md "$TEST_TMP/escaped-agents" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --agents-file .agent/AGENTS.md "$TEST_TMP/escaped-agents" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --skill-dir ../skills "$TEST_TMP/escaped-skills" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --skill-dir .agent/skills "$TEST_TMP/singular-agent" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --no-skills --upgrade-skills "$TEST_TMP/incompatible-options" >/dev/null 2>&1
for case_name in invalid-scope tracked-scope escaped-agents escaped-skills singular-agent incompatible-options; do
    assert_empty "$TEST_TMP/$case_name"
done
expect_failure "$ROOT/install.sh" --agents-file >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --agents-file= >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --agents-file=docs/ --non-interactive "$TEST_TMP/escaped-agents" >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --skill-dir >/dev/null 2>&1
expect_failure "$ROOT/install.sh" --profile-scope >/dev/null 2>&1
expect_failure env -u HOME -u XDG_CONFIG_HOME "$ROOT/install.sh" --non-interactive --profile-scope 1 "$TEST_TMP/global-profile" >/dev/null 2>&1

echo "symlink escapes fail before external writes"
mkdir -p "$TEST_TMP/symlink-target" "$TEST_TMP/symlink-outside"
ln -s "$TEST_TMP/symlink-outside" "$TEST_TMP/symlink-target/docs"
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 "$TEST_TMP/symlink-target" >/dev/null 2>&1
assert_empty "$TEST_TMP/symlink-outside"
[[ ! -e "$TEST_TMP/symlink-target/AGENTS.md" ]] || fail "symlink preflight failed after a partial install"

echo "managed skill resource symlinks fail before mutation"
mkdir -p "$TEST_TMP/skill-symlink/.agents/skills/cairn-session-log" "$TEST_TMP/skill-symlink-outside"
printf '%s\n' 'outside sentinel' > "$TEST_TMP/skill-symlink-outside/resource.md"
ln -s "$TEST_TMP/skill-symlink-outside/resource.md" "$TEST_TMP/skill-symlink/.agents/skills/cairn-session-log/resource.md"
expect_failure "$ROOT/install.sh" --non-interactive --profile-scope 4 --upgrade-skills "$TEST_TMP/skill-symlink" >/dev/null 2>&1
grep -qx 'outside sentinel' "$TEST_TMP/skill-symlink-outside/resource.md"
[[ ! -e "$TEST_TMP/skill-symlink/AGENTS.md" ]] || fail "skill symlink preflight failed after partial installation"

echo "target paths with spaces"
mkdir -p "$TEST_TMP/project with spaces"
"$ROOT/install.sh" --non-interactive --profile-scope 4 "$TEST_TMP/project with spaces" >/dev/null
[[ -f "$TEST_TMP/project with spaces/AGENTS.md" ]] || fail "space-containing target failed"

echo "PASS"
