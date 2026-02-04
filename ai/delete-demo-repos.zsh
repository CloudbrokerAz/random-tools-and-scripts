#!/usr/bin/env zsh
#
# delete-demo-repos.zsh
# Deletes demo repositories locally and remotely
#
# Usage examples:
#   # Delete specific repos by name
#   ./delete-demo-repos.zsh ai-iac-consumer-demo01 ai-iac-consumer-demo02
#
#   # Delete a range using brace expansion
#   ./delete-demo-repos.zsh ai-iac-consumer-demo{01..05}
#
#   # Delete from a file (one repo name per line)
#   ./delete-demo-repos.zsh -f repos-to-delete.txt
#
#   # Dry run (show what would be deleted without doing it)
#   ./delete-demo-repos.zsh --dry-run ai-iac-consumer-demo01

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================
GITHUB_HOST="${GITHUB_HOST:-github.ibm.com}"
GITHUB_ACCOUNT="${GITHUB_ACCOUNT:-Aaron-Evans2}"
CLONE_BASE_PATH="${CLONE_BASE_PATH:-$HOME/Documents/repos}"
DRY_RUN=false
SKIP_CONFIRM=false
REPO_LIST=()

# =============================================================================
# USAGE
# =============================================================================
usage() {
    cat <<EOF
Usage: $0 [OPTIONS] REPO_NAME [REPO_NAME...]

Deletes demo repositories locally and on GitHub.

Options:
    -a, --account NAME      GitHub account/org (default: $GITHUB_ACCOUNT)
    -p, --path PATH         Local base path (default: $CLONE_BASE_PATH)
    -H, --host HOST         GitHub Enterprise host (default: $GITHUB_HOST)
    -f, --file FILE         Read repo names from file (one per line)
    -y, --yes               Skip confirmation prompt
    --dry-run               Show what would be deleted without doing it
    --help                  Show this help message

Examples:
    # Delete specific repos
    $0 ai-iac-consumer-demo01 ai-iac-consumer-demo02

    # Delete a range (zsh brace expansion)
    $0 ai-iac-consumer-demo{01..10}

    # Delete from file
    $0 -f repos-to-delete.txt

    # Dry run first
    $0 --dry-run ai-iac-consumer-demo{01..05}

    # Skip confirmation
    $0 -y ai-iac-consumer-demo01
EOF
    exit 0
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--account)
            GITHUB_ACCOUNT="$2"
            shift 2
            ;;
        -p|--path)
            CLONE_BASE_PATH="$2"
            shift 2
            ;;
        -H|--host)
            GITHUB_HOST="$2"
            shift 2
            ;;
        -f|--file)
            if [[ -f "$2" ]]; then
                while IFS= read -r line; do
                    [[ -n "$line" && ! "$line" =~ ^# ]] && REPO_LIST+=("$line")
                done < "$2"
            else
                echo "Error: File not found: $2"
                exit 1
            fi
            shift 2
            ;;
        -y|--yes)
            SKIP_CONFIRM=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            usage
            ;;
        -*)
            echo "Error: Unknown option $1"
            usage
            ;;
        *)
            REPO_LIST+=("$1")
            shift
            ;;
    esac
done

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
log_info() {
    echo "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo "\033[0;32m[OK]\033[0m $1"
}

log_error() {
    echo "\033[0;31m[ERROR]\033[0m $1" >&2
}

log_warn() {
    echo "\033[0;33m[WARN]\033[0m $1"
}

log_dry() {
    echo "\033[0;35m[DRY-RUN]\033[0m $1"
}

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
preflight_checks() {
    if [[ ${#REPO_LIST[@]} -eq 0 ]]; then
        log_error "No repositories specified"
        echo ""
        echo "Usage: $0 REPO_NAME [REPO_NAME...]"
        echo "       $0 -f repos-to-delete.txt"
        exit 1
    fi

    # Check gh CLI
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed."
        exit 1
    fi

    # Set GH_HOST for GitHub Enterprise
    export GH_HOST="$GITHUB_HOST"

    # Check authentication
    if ! gh auth status --hostname "$GITHUB_HOST" &> /dev/null; then
        log_error "Not authenticated to $GITHUB_HOST"
        echo "  Run: gh auth login --hostname $GITHUB_HOST"
        exit 1
    fi
}

# =============================================================================
# DELETE REPO
# =============================================================================
delete_repo() {
    local repo_name="$1"
    local repo_full="$GITHUB_ACCOUNT/$repo_name"
    local local_path="$CLONE_BASE_PATH/$repo_name"
    local remote_deleted=false
    local local_deleted=false

    log_info "Processing: $repo_name"

    # Check and delete remote repo
    if GH_HOST="$GITHUB_HOST" gh repo view "$repo_full" --json name &> /dev/null 2>&1; then
        if [[ "$DRY_RUN" == true ]]; then
            log_dry "  Would delete remote: $GITHUB_HOST/$repo_full"
        else
            log_info "  Deleting remote repo..."
            if GH_HOST="$GITHUB_HOST" gh repo delete "$repo_full" --yes; then
                log_success "  Deleted remote: $repo_full"
                remote_deleted=true
            else
                log_error "  Failed to delete remote: $repo_full"
            fi
        fi
    else
        log_warn "  Remote repo not found: $repo_full"
    fi

    # Check and delete local directory
    if [[ -d "$local_path" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            log_dry "  Would delete local: $local_path"
        else
            log_info "  Deleting local directory..."
            rm -rf "$local_path"
            log_success "  Deleted local: $local_path"
            local_deleted=true
        fi
    else
        log_warn "  Local directory not found: $local_path"
    fi

    echo ""
}

# =============================================================================
# MAIN
# =============================================================================
main() {
    echo ""
    echo "=============================================="
    echo "  Demo Repository Deleter"
    echo "=============================================="
    echo ""

    preflight_checks

    echo "Configuration:"
    echo "  GitHub Host: $GITHUB_HOST"
    echo "  Account:     $GITHUB_ACCOUNT"
    echo "  Local Path:  $CLONE_BASE_PATH"
    echo "  Dry Run:     $DRY_RUN"
    echo ""
    echo "Repositories to delete (${#REPO_LIST[@]}):"
    for repo in "${REPO_LIST[@]}"; do
        echo "  - $repo"
    done
    echo ""

    # Confirmation prompt
    if [[ "$DRY_RUN" == false && "$SKIP_CONFIRM" == false ]]; then
        echo "\033[0;31mWARNING: This will permanently delete the above repositories!\033[0m"
        echo -n "Type 'yes' to confirm: "
        read confirmation
        if [[ "$confirmation" != "yes" ]]; then
            echo "Aborted."
            exit 0
        fi
        echo ""
    fi

    # Process each repo
    local processed=0
    for repo_name in "${REPO_LIST[@]}"; do
        delete_repo "$repo_name"
        processed=$((processed + 1))
    done

    echo "=============================================="
    echo "  Summary"
    echo "=============================================="
    echo "  Processed: $processed repositories"
    if [[ "$DRY_RUN" == true ]]; then
        echo "  (Dry run - no changes made)"
    fi
    echo "=============================================="
}

main
