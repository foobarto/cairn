#!/usr/bin/env bash
# Cairn installer — scaffold portable workflow docs and Agent Skills.
#
# Usage:
#   ./install.sh [options] [target-project]
#
# Options:
#   --agents-file <path>   Project-relative instructions path (default: AGENTS.md)
#   --skill-dir <path>     Project-relative skills root (default: .agents/skills)
#   --no-skills            Do not install project-local Agent Skills
#   --upgrade-skills       Migrate legacy names and refresh Cairn-owned skill files
#   --profile-scope <N>    1=global-private | 2=local-gitignored | 4=skip
#   --non-interactive      Do not prompt; profile defaults to skip
#   --dry-run              Print actions without writing
#   --help                 Show this help

set -euo pipefail

DRY_RUN=false
NON_INTERACTIVE=false
INSTALL_SKILLS=true
UPGRADE_SKILLS=false
AGENTS_FILE="AGENTS.md"
SKILL_DIR=".agents/skills"
PROFILE_SCOPE=""
TARGET=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
    sed -n '2,/^$/s/^# \?//p' "$0"
    exit 0
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

require_value() {
    local option="$1"
    local count="$2"
    local value="${3:-}"
    if [[ "$count" -lt 2 || -z "$value" || "$value" == -* ]]; then
        fail "$option requires a value"
    fi
}

is_safe_relative_path() {
    local value="$1"
    local component
    local -a components=()
    [[ -n "$value" && "$value" != /* && "$value" != */ && "$value" != *//* ]] || return 1
    IFS='/' read -r -a components <<< "$value"
    for component in "${components[@]}"; do
        [[ -n "$component" && "$component" != "." && "$component" != ".." ]] || return 1
        [[ "$component" =~ ^[A-Za-z0-9._-]+$ ]] || return 1
    done
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            usage
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --non-interactive)
            NON_INTERACTIVE=true
            shift
            ;;
        --no-skills)
            INSTALL_SKILLS=false
            shift
            ;;
        --upgrade-skills)
            UPGRADE_SKILLS=true
            shift
            ;;
        --agents-file)
            require_value "$1" "$#" "${2:-}"
            AGENTS_FILE="$2"
            shift 2
            ;;
        --agents-file=*)
            AGENTS_FILE="${1#--agents-file=}"
            [[ -n "$AGENTS_FILE" ]] || fail "--agents-file requires a value"
            shift
            ;;
        --skill-dir)
            require_value "$1" "$#" "${2:-}"
            SKILL_DIR="$2"
            shift 2
            ;;
        --skill-dir=*)
            SKILL_DIR="${1#--skill-dir=}"
            [[ -n "$SKILL_DIR" ]] || fail "--skill-dir requires a value"
            shift
            ;;
        --profile-scope)
            require_value "$1" "$#" "${2:-}"
            PROFILE_SCOPE="$2"
            shift 2
            ;;
        --profile-scope=*)
            PROFILE_SCOPE="${1#--profile-scope=}"
            [[ -n "$PROFILE_SCOPE" ]] || fail "--profile-scope requires a value"
            shift
            ;;
        -*)
            fail "unknown option: $1"
            ;;
        *)
            [[ -z "$TARGET" ]] || fail "multiple target projects supplied"
            TARGET="$1"
            shift
            ;;
    esac
done

is_safe_relative_path "$AGENTS_FILE" || fail "--agents-file must be a safe project-relative path"
if [[ "$AGENTS_FILE" == ".agent" || "$AGENTS_FILE" == .agent/* ]]; then
    fail "singular .agent is not a customization root; use .agents"
fi
if $INSTALL_SKILLS; then
    is_safe_relative_path "$SKILL_DIR" || fail "--skill-dir must be a safe project-relative path"
    if [[ "$SKILL_DIR" == ".agent" || "$SKILL_DIR" == .agent/* ]]; then
        fail "singular .agent is not a skill discovery root; use .agents/skills"
    fi
fi
if [[ -n "$PROFILE_SCOPE" && ! "$PROFILE_SCOPE" =~ ^(1|2|4)$ ]]; then
    fail "--profile-scope must be 1, 2, or 4; tracked personal profiles are not supported"
fi
if ! $INSTALL_SKILLS && $UPGRADE_SKILLS; then
    fail "--upgrade-skills cannot be combined with --no-skills"
fi

TARGET="${TARGET:-$(pwd)}"
[[ -d "$TARGET" ]] || fail "target directory does not exist: $TARGET"
TARGET="$(cd "$TARGET" && pwd -P)"
[[ "$TARGET" != "/" ]] || fail "refusing to use the filesystem root as a target"

ensure_project_parent() {
    local destination="$1"
    local parent resolved_parent
    parent="$(dirname "$destination")"
    while [[ ! -e "$parent" && ! -L "$parent" ]]; do
        [[ "$parent" != "/" ]] || fail "cannot resolve parent for $destination"
        parent="$(dirname "$parent")"
    done
    [[ -d "$parent" ]] || fail "destination parent is not a directory: $parent"
    resolved_parent="$(cd "$parent" && pwd -P)"
    case "$resolved_parent/" in
        "$TARGET/"*) ;;
        *) fail "destination escapes target through a symlink: $destination" ;;
    esac
}

reject_symlinks_in_tree() {
    local tree="$1"
    local first_link=""

    [[ ! -L "$tree" ]] || fail "refusing to manage a symlinked skill directory: $tree"
    if [[ -d "$tree" ]]; then
        first_link="$(find "$tree" -type l -print -quit)"
        [[ -z "$first_link" ]] || fail "refusing to copy through a symlink in a managed skill: $first_link"
    fi
}

is_legacy_cairn_skill() {
    local legacy_name="$1"
    local legacy_path="$2"
    local skill_file="$legacy_path/SKILL.md"

    [[ -d "$legacy_path" && ! -L "$legacy_path" ]] || return 1
    [[ -f "$skill_file" && ! -L "$skill_file" ]] || return 1
    sed -n '2,/^---$/p' "$skill_file" | grep -qx "name: cairn-$legacy_name"
}

if [[ -z "$PROFILE_SCOPE" ]] && ! $NON_INTERACTIVE; then
    cat <<'PROMPT'

Where should Cairn keep your personal user profile?

  [1] Global private — ~/.config/cairn/user-profile.md
  [2] Project-local, gitignored — .cairn/user-profile.md
  [4] Skip — no personal profile

Tracked personal profiles are intentionally unsupported. Pick [1/2/4]
(default: 1):
PROMPT
    read -r PROFILE_SCOPE
    PROFILE_SCOPE="${PROFILE_SCOPE:-1}"
    [[ "$PROFILE_SCOPE" =~ ^(1|2|4)$ ]] || fail "profile choice must be 1, 2, or 4"
fi
if [[ -z "$PROFILE_SCOPE" ]]; then
    PROFILE_SCOPE="4"
fi

if [[ "$PROFILE_SCOPE" == "1" ]]; then
    if [[ -n "${XDG_CONFIG_HOME:-}" ]]; then
        PROFILE_BASE="$XDG_CONFIG_HOME"
    else
        [[ -n "${HOME:-}" ]] || fail "HOME or XDG_CONFIG_HOME is required for a global profile"
        PROFILE_BASE="$HOME/.config"
    fi
    [[ "$PROFILE_BASE" == /* ]] || fail "profile base must be an absolute path"
    USER_PROFILE_PATH="$PROFILE_BASE/cairn/user-profile.md"
elif [[ "$PROFILE_SCOPE" == "2" ]]; then
    USER_PROFILE_PATH="$TARGET/.cairn/user-profile.md"
else
    USER_PROFILE_PATH=""
fi

# Resolve every project-owned destination before the first write. This catches
# existing directory symlinks that would otherwise redirect a lexically safe
# path outside the selected target.
for destination in \
    "$TARGET/docs/sessions/README.md" \
    "$TARGET/docs/todo.md" \
    "$TARGET/docs/project-profile.md" \
    "$TARGET/docs/workflow/governing-principles.md" \
    "$TARGET/docs/workflow/six-phase-checklist.md" \
    "$TARGET/docs/workflow/autonomous-protocol.md" \
    "$TARGET/$AGENTS_FILE"
do
    ensure_project_parent "$destination"
done
if $INSTALL_SKILLS; then
    for skill_dir in "$SCRIPT_DIR"/skills/*; do
        [[ -f "$skill_dir/SKILL.md" ]] || continue
        ensure_project_parent "$TARGET/$SKILL_DIR/$(basename "$skill_dir")/SKILL.md"
        if [[ -e "$TARGET/$SKILL_DIR/$(basename "$skill_dir")" || -L "$TARGET/$SKILL_DIR/$(basename "$skill_dir")" ]]; then
            reject_symlinks_in_tree "$TARGET/$SKILL_DIR/$(basename "$skill_dir")"
        fi
    done

    for legacy_name in autonomous-loop autonomous-round build-project-profile build-user-profile close-session review-phase session-log; do
        legacy_path="$TARGET/$SKILL_DIR/$legacy_name"
        current_path="$TARGET/$SKILL_DIR/cairn-$legacy_name"
        if is_legacy_cairn_skill "$legacy_name" "$legacy_path"; then
            reject_symlinks_in_tree "$legacy_path"
            if [[ -e "$current_path" || -L "$current_path" ]]; then
                fail "both legacy Cairn skill $legacy_path and current skill $current_path exist; reconcile them before installing"
            fi
        fi
    done
fi
if [[ "$PROFILE_SCOPE" == "2" ]]; then
    ensure_project_parent "$TARGET/.cairn/user-profile.md"
    ensure_project_parent "$TARGET/.cairn/config.json"
    ensure_project_parent "$TARGET/.gitignore"
    [[ ! -L "$TARGET/.gitignore" ]] || fail "refusing to append through a .gitignore symlink"
fi

run() {
    if $DRY_RUN; then
        printf '[dry-run]'
        printf ' %q' "$@"
        printf '\n'
    else
        "$@"
    fi
}

copy_if_missing() {
    local source="$1"
    local destination="$2"
    if [[ -e "$destination" || -L "$destination" ]]; then
        echo "  · $destination (exists, skipped)"
        return
    fi
    run mkdir -p "$(dirname "$destination")"
    run cp "$source" "$destination"
    echo "  ✓ $destination"
}

write_sessions_readme() {
    local destination="$TARGET/docs/sessions/README.md"
    if [[ -e "$destination" || -L "$destination" ]]; then
        echo "  · $destination (exists, skipped)"
        return
    fi
    if $DRY_RUN; then
        echo "[dry-run] write $destination"
    else
        mkdir -p "$(dirname "$destination")"
        {
            echo "# Session journals"
            echo
            echo "Per-session runtime logs, written as work proceeds."
            echo 'Filename convention: `YYYY-MM-DD-<topic-slug>.md`.'
            echo
            echo "See [../workflow/](../workflow/) for the Cairn protocol and"
            echo "[../../$AGENTS_FILE](../../$AGENTS_FILE) for project instructions."
        } > "$destination"
    fi
    echo "  ✓ $destination"
}

install_skill() {
    local source_dir="$1"
    local skill_name destination
    skill_name="$(basename "$source_dir")"
    destination="$TARGET/$SKILL_DIR/$skill_name"

    if [[ -e "$destination" || -L "$destination" ]]; then
        reject_symlinks_in_tree "$destination"
    fi

    if [[ ( -e "$destination/SKILL.md" || -L "$destination/SKILL.md" ) && "$UPGRADE_SKILLS" == false ]]; then
        echo "  · $destination/ (exists, skipped)"
        return
    fi
    run mkdir -p "$destination"
    run cp -R "$source_dir/." "$destination/"
    if $UPGRADE_SKILLS; then
        echo "  ↻ $destination/"
    else
        echo "  ✓ $destination/"
    fi
}

migrate_legacy_skills() {
    local legacy_name legacy_path current_path
    for legacy_name in autonomous-loop autonomous-round build-project-profile build-user-profile close-session review-phase session-log; do
        legacy_path="$TARGET/$SKILL_DIR/$legacy_name"
        current_path="$TARGET/$SKILL_DIR/cairn-$legacy_name"
        if [[ ! -e "$legacy_path" && ! -L "$legacy_path" ]]; then
            continue
        fi
        if ! is_legacy_cairn_skill "$legacy_name" "$legacy_path"; then
            continue
        elif ! $UPGRADE_SKILLS; then
            echo "  ! $legacy_path/ (legacy name; rerun with --upgrade-skills to migrate)"
        else
            run mv "$legacy_path" "$current_path"
            echo "  ↻ $legacy_path/ → $current_path/"
        fi
    done
}

echo "Cairn installer"
echo "==============="
echo "Target:          $TARGET"
echo "Instructions:    $AGENTS_FILE"
if $INSTALL_SKILLS; then
    echo "Skills root:     $SKILL_DIR"
else
    echo "Skills:          disabled"
fi
echo "Profile scope:   $PROFILE_SCOPE"
if $DRY_RUN; then
    echo "Mode:            dry-run"
fi
echo

echo "Session journal directory:"
run mkdir -p "$TARGET/docs/sessions"
write_sessions_readme

echo "Workflow and project files:"
copy_if_missing "$SCRIPT_DIR/templates/todo.md" "$TARGET/docs/todo.md"
copy_if_missing "$SCRIPT_DIR/templates/project-profile.md" "$TARGET/docs/project-profile.md"
copy_if_missing "$SCRIPT_DIR/templates/workflow/governing-principles.md" "$TARGET/docs/workflow/governing-principles.md"
copy_if_missing "$SCRIPT_DIR/templates/workflow/six-phase-checklist.md" "$TARGET/docs/workflow/six-phase-checklist.md"
copy_if_missing "$SCRIPT_DIR/templates/workflow/autonomous-protocol.md" "$TARGET/docs/workflow/autonomous-protocol.md"
copy_if_missing "$SCRIPT_DIR/templates/agent-instructions.md" "$TARGET/$AGENTS_FILE"

if $INSTALL_SKILLS; then
    echo "Portable Agent Skills:"
    migrate_legacy_skills
    for skill_dir in "$SCRIPT_DIR"/skills/*; do
        [[ -f "$skill_dir/SKILL.md" ]] || continue
        install_skill "$skill_dir"
    done
fi

echo "Personal profile:"
case "$PROFILE_SCOPE" in
    1)
        copy_if_missing "$SCRIPT_DIR/templates/user-profile.md" "$USER_PROFILE_PATH"
        ;;
    2)
        copy_if_missing "$SCRIPT_DIR/templates/user-profile.md" "$USER_PROFILE_PATH"
        if [[ -f "$TARGET/.gitignore" ]] && grep -qE '^/?\.cairn/$' "$TARGET/.gitignore"; then
            echo "  · $TARGET/.gitignore (already ignores .cairn/)"
        elif $DRY_RUN; then
            echo "[dry-run] add /.cairn/ to $TARGET/.gitignore"
        else
            printf '%s\n' '/.cairn/' >> "$TARGET/.gitignore"
            echo "  ✓ $TARGET/.gitignore (added /.cairn/)"
        fi
        copy_if_missing /dev/stdin "$TARGET/.cairn/config.json" <<'EOF'
{"user_profile_path":".cairn/user-profile.md"}
EOF
        ;;
    4)
        echo "  · skipped"
        ;;
esac

echo
echo "Done. Customize $TARGET/$AGENTS_FILE and $TARGET/docs/project-profile.md."
if $INSTALL_SKILLS; then
    echo "Agent Skills clients can discover Cairn under $TARGET/$SKILL_DIR/."
fi
