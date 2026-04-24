#!/usr/bin/env bash
# cairn installer — scaffolds session journal dir, rolling punch list,
# workflow docs, CLAUDE.md, and optional user + project profiles into
# a target project.
#
# Usage:
#   ./install.sh                   # install into CWD
#   ./install.sh /path/to/project  # install into that path
#
# Options:
#   --agents-file <name>   Rename CLAUDE.md to this on copy (GEMINI.md, AGENTS.md)
#   --profile-scope <N>    User-profile location: 1=global (default) | 2=local-gitignored | 3=local-tracked | 4=skip
#   --non-interactive      Don't prompt for profile scope; use --profile-scope value (or 1)
#   --dry-run              Print what would happen, don't touch files
#   --help                 Show this help
#
# The script never overwrites existing files; it reports "skipped" for
# each collision. For a clean re-run, delete the files you want
# refreshed before invoking.

set -euo pipefail

DRY_RUN=false
NON_INTERACTIVE=false
AGENTS_FILE="CLAUDE.md"
PROFILE_SCOPE=""
TARGET=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
    sed -n '3,/^$/s/^# \?//p' "$0"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h) usage ;;
        --dry-run) DRY_RUN=true; shift ;;
        --non-interactive) NON_INTERACTIVE=true; shift ;;
        --agents-file) AGENTS_FILE="$2"; shift 2 ;;
        --agents-file=*) AGENTS_FILE="${1#--agents-file=}"; shift ;;
        --profile-scope) PROFILE_SCOPE="$2"; shift 2 ;;
        --profile-scope=*) PROFILE_SCOPE="${1#--profile-scope=}"; shift ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *)
            if [[ -z "$TARGET" ]]; then
                TARGET="$1"
            else
                echo "Error: multiple positional arguments" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ -z "$TARGET" ]]; then
    TARGET="$(pwd)"
fi

if [[ ! -d "$TARGET" ]]; then
    echo "Error: target directory does not exist: $TARGET" >&2
    exit 1
fi

run() {
    if $DRY_RUN; then
        echo "[dry-run] $*"
    else
        "$@"
    fi
}

copy_if_missing() {
    local src="$1"
    local dst="$2"

    if [[ -e "$dst" ]]; then
        echo "  · $dst (exists, skipped)"
        return 0
    fi

    local dst_dir
    dst_dir="$(dirname "$dst")"
    run mkdir -p "$dst_dir"
    run cp "$src" "$dst"
    echo "  ✓ $dst"
}

mkdir_if_missing() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        echo "  · $dir/ (exists, skipped)"
        return 0
    fi
    run mkdir -p "$dir"
    echo "  ✓ $dir/"
}

echo "cairn installer"
echo "==============="
echo ""
echo "Source:         $SCRIPT_DIR"
echo "Target:         $TARGET"
echo "Agents file:    $AGENTS_FILE"
if $DRY_RUN; then
    echo "Mode:           dry-run"
fi
echo ""

# 1. docs/sessions/
echo "Session journal directory:"
mkdir_if_missing "$TARGET/docs/sessions"

if [[ ! -e "$TARGET/docs/sessions/README.md" ]] && ! $DRY_RUN; then
    cat > "$TARGET/docs/sessions/README.md" <<'EOF'
# Session journals

Per-session runtime logs, written as you go (not retroactively).
Filename convention: `YYYY-MM-DD-<topic-slug>.md`.

See [../workflow/](../workflow/) for the cairn protocol docs and
[../../CLAUDE.md](../../CLAUDE.md) (or AGENTS.md / GEMINI.md) for
the project's session rhythm.
EOF
    echo "  ✓ $TARGET/docs/sessions/README.md"
elif [[ -e "$TARGET/docs/sessions/README.md" ]]; then
    echo "  · $TARGET/docs/sessions/README.md (exists, skipped)"
fi

# 2. docs/todo.md
echo ""
echo "Rolling punch list:"
copy_if_missing "$SCRIPT_DIR/templates/todo.md" "$TARGET/docs/todo.md"

# 3. docs/workflow/
echo ""
echo "Workflow docs:"
copy_if_missing \
    "$SCRIPT_DIR/templates/workflow/governing-principles.md" \
    "$TARGET/docs/workflow/governing-principles.md"
copy_if_missing \
    "$SCRIPT_DIR/templates/workflow/six-phase-checklist.md" \
    "$TARGET/docs/workflow/six-phase-checklist.md"
copy_if_missing \
    "$SCRIPT_DIR/templates/workflow/autonomous-protocol.md" \
    "$TARGET/docs/workflow/autonomous-protocol.md"

# 4. docs/project-profile.md
echo ""
echo "Project profile:"
copy_if_missing "$SCRIPT_DIR/templates/project-profile.md" "$TARGET/docs/project-profile.md"

# 5. CLAUDE.md / AGENTS.md / GEMINI.md
echo ""
echo "Agent-instructions file ($AGENTS_FILE):"
copy_if_missing "$SCRIPT_DIR/templates/CLAUDE.md" "$TARGET/$AGENTS_FILE"

# 6. User profile — interactive prompt (or --profile-scope)
echo ""
echo "User profile location:"

if [[ -z "$PROFILE_SCOPE" ]] && ! $NON_INTERACTIVE; then
    cat <<'PROMPT'

  [1] Global (recommended) — ~/.config/cairn/user-profile.md
      One profile across all your cairn projects. Private to you.
  [2] Project-local, gitignored — .cairn/user-profile.md
      Per-project, not shared with collaborators.
  [3] Project-local, tracked — docs/user-profiles/<handle>.md
      Per-project, shared with collaborators (handle = git user).
  [4] Skip — no profile feature.

PROMPT
    read -r -p "Pick [1/2/3/4] (default: 1): " PROFILE_SCOPE
    PROFILE_SCOPE="${PROFILE_SCOPE:-1}"
fi
PROFILE_SCOPE="${PROFILE_SCOPE:-1}"

case "$PROFILE_SCOPE" in
    1)
        USER_PROFILE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/cairn"
        USER_PROFILE_PATH="$USER_PROFILE_DIR/user-profile.md"
        mkdir_if_missing "$USER_PROFILE_DIR"
        copy_if_missing "$SCRIPT_DIR/templates/user-profile.md" "$USER_PROFILE_PATH"
        echo "  → Global profile. No per-project config needed."
        ;;
    2)
        USER_PROFILE_PATH="$TARGET/.cairn/user-profile.md"
        mkdir_if_missing "$TARGET/.cairn"
        copy_if_missing "$SCRIPT_DIR/templates/user-profile.md" "$USER_PROFILE_PATH"
        if ! $DRY_RUN; then
            if [[ -f "$TARGET/.gitignore" ]] && ! grep -qE '^/?\.cairn/' "$TARGET/.gitignore"; then
                echo "/.cairn/" >> "$TARGET/.gitignore"
                echo "  ✓ Added /.cairn/ to $TARGET/.gitignore"
            elif [[ ! -f "$TARGET/.gitignore" ]]; then
                echo "/.cairn/" > "$TARGET/.gitignore"
                echo "  ✓ Created $TARGET/.gitignore with /.cairn/ entry"
            fi
            cat > "$TARGET/.cairn/config.json" <<EOF
{
  "user_profile_path": ".cairn/user-profile.md"
}
EOF
            echo "  ✓ $TARGET/.cairn/config.json"
        fi
        ;;
    3)
        HANDLE="$(git -C "$TARGET" config user.name 2>/dev/null || echo "${USER:-contributor}" )"
        HANDLE="$(echo "$HANDLE" | tr '[:upper:] ' '[:lower:]-')"
        USER_PROFILE_PATH="$TARGET/docs/user-profiles/${HANDLE}.md"
        copy_if_missing "$SCRIPT_DIR/templates/user-profile.md" "$USER_PROFILE_PATH"
        if ! $DRY_RUN; then
            mkdir -p "$TARGET/.cairn"
            cat > "$TARGET/.cairn/config.json" <<EOF
{
  "user_profile_path": "docs/user-profiles/${HANDLE}.md"
}
EOF
            echo "  ✓ $TARGET/.cairn/config.json"
        fi
        ;;
    4)
        echo "  · Skipped (no user profile created)."
        ;;
    *)
        echo "  ! Unknown profile scope '$PROFILE_SCOPE' — skipping." >&2
        ;;
esac

echo ""
echo "Done."
echo ""
echo "Next steps:"
echo "  1. Open $TARGET/$AGENTS_FILE and customise the"
echo "     'Project-specific notes' section at the bottom."
echo "  2. Open $TARGET/docs/project-profile.md and fill in the"
echo "     project's stances (risk tolerance, security posture,"
echo "     quality bar, contribution norms)."
echo "  3. Open $TARGET/docs/todo.md and either start fresh or"
echo "     import your existing punch list."
if [[ "$PROFILE_SCOPE" != "4" ]]; then
    echo "  4. The user profile stub is at:"
    echo "     ${USER_PROFILE_PATH:-<profile-path>}"
    echo "     Let cairn build it up across sessions — don't pre-fill."
fi
echo ""
echo "Optional: also install ep-kit for structured proposals"
echo "(https://github.com/foobarto/ep-kit)."
