#!/usr/bin/env bash
# SIGIL — Claude Code skill installer.
# One-line install:
#   curl -fsSL https://raw.githubusercontent.com/tommy29tmar/SIGIL/main/integrations/claude-code/install.sh | bash
#
# What this does:
#   1. Installs the /sigil Claude Code skill.
#   2. Installs the SIGIL output-style (optional, only if output-styles dir exists or can be created).
#   3. Installs the sigil-ir Python package (provides the `sigil` CLI for local parse/rerender).
#
# Refuses to run if ~/.claude is not present (i.e. Claude Code not installed).

set -euo pipefail

CLAUDE_DIR="${HOME}/.claude"
REPO_URL="https://github.com/tommy29tmar/SIGIL.git"
RAW_URL="https://raw.githubusercontent.com/tommy29tmar/SIGIL/main"

if [ ! -d "$CLAUDE_DIR" ]; then
  echo "error: ~/.claude not found. Install Claude Code first."
  exit 1
fi

# Detect if running from a repo checkout (for local testing). Otherwise curl down.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
IS_LOCAL=0
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/skill/SKILL.md" ]; then
  IS_LOCAL=1
fi

fetch() {
  # fetch <relative_path> <dest>
  local rel="$1"
  local dest="$2"
  if [ "$IS_LOCAL" = "1" ]; then
    cp "$SCRIPT_DIR/$rel" "$dest"
  else
    curl -fsSL "$RAW_URL/integrations/claude-code/$rel" -o "$dest"
  fi
}

echo "==> Installing /sigil skill"
mkdir -p "$CLAUDE_DIR/skills/sigil"
fetch "skill/SKILL.md" "$CLAUDE_DIR/skills/sigil/SKILL.md"

echo "==> Installing SIGIL output-style"
mkdir -p "$CLAUDE_DIR/output-styles"
fetch "output-styles/sigil.md" "$CLAUDE_DIR/output-styles/sigil.md" || \
  echo "   (output-style install failed — skill alone is sufficient)"

echo "==> Installing sigil-ir Python package (optional)"
if command -v pipx >/dev/null 2>&1; then
  pipx install "git+${REPO_URL}" || pipx install --force "git+${REPO_URL}" || true
elif command -v pip >/dev/null 2>&1; then
  pip install --user "git+${REPO_URL}" || true
else
  echo "   (skipping — install pipx or pip to get the \`sigil\` CLI)"
fi

echo ""
echo "✓ SIGIL installed."
echo ""
echo "Use:"
echo "  /sigil <your question>              # one-shot, in any Claude Code session"
echo "  /output-style sigil                 # persistent, every response in SIGIL"
echo ""
echo "Toggle off with /output-style default."
