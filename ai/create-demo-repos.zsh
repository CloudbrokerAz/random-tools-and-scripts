#!/usr/bin/env zsh
#
# create-demo-repos.zsh
# Creates demo repositories from a template with all branches
#
# Variables (via CLI args or env vars):                                   
#   - -a, --account - Target GitHub account (default: Aaron-Evans2)
#   - -n, --name - Base repo name (default: ai-iac-consumer-demo)           
#   - -c, --count - Number of repos to create (default: 1)
#   - -p, --path - Local clone path (default: ~/Documents/repos)
#   - -h, --host - GitHub Enterprise host (default: github.ibm.com)
#   - -v, --visibility - public/private (default: public)

#   Usage examples:
#   # Create 1 repo (ai-iac-consumer-demo01)
#   ./scripts/create-demo-repos.zsh

#   # Create 5 repos (ai-iac-consumer-demo01 through demo05)
#   ./scripts/create-demo-repos.zsh -c 5

#   # Create 10 repos with custom name
#   ./scripts/create-demo-repos.zsh -c 10 -n workshop-lab

#   # Full custom example
#   ./scripts/create-demo-repos.zsh -a MyOrg -c 3 -n my-project -p ~/code

#   Pre-flight checks:
#   - Verifies gh CLI is installed
#   - Checks authentication via GH_ENTERPRISE_TOKEN env var or existing gh
#   auth
#   - Confirms template repo exists
#   - Creates clone directory if needed

#   Authentication: Set GH_ENTERPRISE_TOKEN before running, or run gh auth
#   login -h github.ibm.com first.

set -e  # Exit on first error

# =============================================================================
# CONFIGURATION - Modify these defaults as needed
# =============================================================================
GITHUB_HOST="${GITHUB_HOST:-github.ibm.com}"
GITHUB_ACCOUNT="${GITHUB_ACCOUNT:-Aaron-Evans2}"
TEMPLATE_ORG="${TEMPLATE_ORG:-AdvArch}"
TEMPLATE_REPO="${TEMPLATE_REPO:-ai-iac-consumer-template}"
REPO_BASE_NAME="${REPO_BASE_NAME:-ai-iac-consumer-demo}"
CLONE_BASE_PATH="${CLONE_BASE_PATH:-$HOME/Documents/repos}"
REPO_COUNT="${REPO_COUNT:-1}"
REPO_VISIBILITY="${REPO_VISIBILITY:-public}"

# =============================================================================
# USAGE
# =============================================================================
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Creates demo repositories from the template repo with all branches.

Options:
    -a, --account NAME      GitHub account/org for new repos (default: $GITHUB_ACCOUNT)
    -n, --name BASE_NAME    Base name for repos (default: $REPO_BASE_NAME)
    -c, --count NUMBER      Number of repos to create (default: $REPO_COUNT)
    -p, --path PATH         Local path to clone repos (default: $CLONE_BASE_PATH)
    -h, --host HOST         GitHub Enterprise host (default: $GITHUB_HOST)
    -t, --template ORG/REPO Template repo (default: $TEMPLATE_ORG/$TEMPLATE_REPO)
    -v, --visibility TYPE   Repo visibility: public/private (default: $REPO_VISIBILITY)
    --help                  Show this help message

Environment Variables:
    GH_ENTERPRISE_TOKEN     GitHub Enterprise token for authentication
    GITHUB_HOST             GitHub Enterprise host
    GITHUB_ACCOUNT          Target account for new repos

Examples:
    # Create 1 repo with defaults
    $0

    # Create 5 repos
    $0 -c 5

    # Create 3 repos with custom name
    $0 -c 3 -n my-demo-project

    # Create repos in a different account
    $0 -a MyOrg -c 2
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
        -n|--name)
            REPO_BASE_NAME="$2"
            shift 2
            ;;
        -c|--count)
            REPO_COUNT="$2"
            shift 2
            ;;
        -p|--path)
            CLONE_BASE_PATH="$2"
            shift 2
            ;;
        -h|--host)
            GITHUB_HOST="$2"
            shift 2
            ;;
        -t|--template)
            TEMPLATE_ORG="${2%%/*}"
            TEMPLATE_REPO="${2##*/}"
            shift 2
            ;;
        -v|--visibility)
            REPO_VISIBILITY="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
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

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
preflight_checks() {
    log_info "Running pre-flight checks..."

    # Check gh CLI is installed
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed."
        echo "  Install with: brew install gh"
        exit 1
    fi
    log_success "GitHub CLI found: $(gh --version | head -1)"

    # Set GH_HOST for all gh commands (GitHub Enterprise)
    export GH_HOST="$GITHUB_HOST"

    # Check for GH_ENTERPRISE_TOKEN
    if [[ -z "$GH_ENTERPRISE_TOKEN" ]]; then
        log_warn "GH_ENTERPRISE_TOKEN not set. Checking existing auth..."

        # Check if already authenticated to the host
        if ! gh auth status --hostname "$GITHUB_HOST" &> /dev/null; then
            log_error "Not authenticated to $GITHUB_HOST"
            echo ""
            echo "  Option 1: Set environment variable"
            echo "    export GH_ENTERPRISE_TOKEN='your-token-here'"
            echo ""
            echo "  Option 2: Login interactively"
            echo "    gh auth login --hostname $GITHUB_HOST"
            echo ""
            exit 1
        fi
    fi
    log_success "Authenticated to $GITHUB_HOST"

    # Verify template repo exists (GH_HOST is set, so no need for --hostname)
    if ! GH_HOST="$GITHUB_HOST" gh repo view "$TEMPLATE_ORG/$TEMPLATE_REPO" --json name &> /dev/null; then
        log_error "Template repo not found: $TEMPLATE_ORG/$TEMPLATE_REPO"
        exit 1
    fi
    log_success "Template repo exists: $TEMPLATE_ORG/$TEMPLATE_REPO"

    # Check clone base path exists
    if [[ ! -d "$CLONE_BASE_PATH" ]]; then
        log_info "Creating clone directory: $CLONE_BASE_PATH"
        mkdir -p "$CLONE_BASE_PATH"
    fi
    log_success "Clone path ready: $CLONE_BASE_PATH"

    echo ""
}

# =============================================================================
# REPO CREATION
# =============================================================================
create_repo() {
    local repo_name="$1"
    local repo_full="$GITHUB_ACCOUNT/$repo_name"
    local local_path="$CLONE_BASE_PATH/$repo_name"
    local template_url="https://$GITHUB_HOST/$TEMPLATE_ORG/$TEMPLATE_REPO.git"
    local new_repo_url="https://$GITHUB_HOST/$repo_full.git"

    log_info "Creating repo: $repo_full"

    # Check if repo already exists on remote (GH_HOST env var handles the host)
    if GH_HOST="$GITHUB_HOST" gh repo view "$repo_full" --json name &> /dev/null 2>&1; then
        log_warn "Repo already exists on $GITHUB_HOST: $repo_full - skipping"
        return 1
    fi

    # Check if local directory exists
    if [[ -d "$local_path" ]]; then
        log_warn "Local directory already exists: $local_path - skipping"
        return 1
    fi

    # Create the new empty repo
    log_info "  Creating empty repo on $GITHUB_HOST..."
    GH_HOST="$GITHUB_HOST" gh repo create "$repo_full" \
        --"$REPO_VISIBILITY" \
        --description "Demo repo created from $TEMPLATE_ORG/$TEMPLATE_REPO template"

    # Clone template with all branches to local
    log_info "  Cloning template repo with all branches..."
    git clone "$template_url" "$local_path"
    cd "$local_path"

    # Fetch all remote branches and create local tracking branches
    log_info "  Setting up all branches from template..."
    for branch in $(git branch -r | grep -v '\->' | grep -v 'HEAD' | sed 's/origin\///'); do
        if [[ "$branch" != "main" && "$branch" != "master" ]]; then
            git branch --track "$branch" "origin/$branch" 2>/dev/null || true
        fi
    done

    # Update remote to point to new repo
    log_info "  Updating remote origin to new repo..."
    git remote set-url origin "$new_repo_url"

    # Push all branches and tags to new repo
    log_info "  Pushing all branches and tags..."
    git push --all origin
    git push --tags origin

    log_success "Created and cloned: $repo_full -> $local_path"
    echo ""
}

# =============================================================================
# MAIN
# =============================================================================
main() {
    echo ""
    echo "=============================================="
    echo "  Demo Repository Creator"
    echo "=============================================="
    echo ""
    echo "Configuration:"
    echo "  Template:    $TEMPLATE_ORG/$TEMPLATE_REPO"
    echo "  Target:      $GITHUB_ACCOUNT"
    echo "  Base name:   $REPO_BASE_NAME"
    echo "  Count:       $REPO_COUNT"
    echo "  Clone path:  $CLONE_BASE_PATH"
    echo "  Visibility:  $REPO_VISIBILITY"
    echo ""

    preflight_checks

    local created=0
    local skipped=0

    for i in $(seq -w 1 "$REPO_COUNT"); do
        # Format number with leading zeros (01, 02, ... 10, 11, etc.)
        local padded=$(printf "%02d" "$i")
        local repo_name="${REPO_BASE_NAME}${padded}"

        if create_repo "$repo_name"; then
            created=$((created + 1))
        else
            skipped=$((skipped + 1))
        fi
    done

    echo "=============================================="
    echo "  Summary"
    echo "=============================================="
    echo "  Created: $created"
    echo "  Skipped: $skipped"
    echo "=============================================="
}

main
