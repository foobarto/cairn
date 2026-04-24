#!/usr/bin/env bash
# cairn installer — scaffolds session journal dir, rolling punch list,
# workflow docs, and CLAUDE.md into a target project.
#
# Usage:
#   ./install.sh                   # install into CWD
#   ./install.sh /path/to/project  # install into that path
#
# Options:
#   --agents-file <name>   Rename CLAUDE.md to this on copy (GEMINI.md, AGENTS.md)
#   --dry-run              Print what would happen, don't touch files
#   --help                 Show this help
#
# The script never overwrites existing files; it reports "skipped" for
# each collision. For a clean re-run, delete the files you want
# refreshed before invoking.

set -euo pipefail

DRY_RUN=false
AGENTS_FILE="CLAUDE.md"
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
        --agents-file) AGENTS_FILE="$2"; shift 2 ;;
        --agents-file=*) AGENTS_FILE="${1#--agents-file=}"; shift ;;
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
    "$SCRIPT_DIR/templates/workflow/six-phase-checklist.md" \
    "$TARGET/docs/workflow/six-phase-checklist.md"
copy_if_missing \
    "$SCRIPT_DIR/templates/workflow/autonomous-round-protocol.md" \
    "$TARGET/docs/workflow/autonomous-round-protocol.md"

# 4. CLAUDE.md / AGENTS.md / GEMINI.md
echo ""
echo "Agent-instructions file ($AGENTS_FILE):"
copy_if_missing "$SCRIPT_DIR/templates/CLAUDE.md" "$TARGET/$AGENTS_FILE"

echo ""
echo "Done."
echo ""
echo "Next steps:"
echo "  1. Open $TARGET/$AGENTS_FILE and customise the"
echo "     'Project-specific notes' section at the bottom."
echo "  2. Open $TARGET/docs/todo.md and either start fresh or"
echo "     import your existing punch list."
echo "  3. On your first cairn session, create"
echo "     $TARGET/docs/sessions/\$(date +%F)-<topic>.md"
echo "     from templates/session-template.md."
echo ""
echo "Optional: also install ep-kit for structured proposals"
echo "(https://github.com/foobarto/ep-kit)."
