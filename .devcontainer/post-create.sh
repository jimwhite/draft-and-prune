#!/bin/bash
# Post-create setup script for the Draft-and-Prune devcontainer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_WORKSPACE_FOLDER="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE_FOLDER="${1:-${DEFAULT_WORKSPACE_FOLDER}}"

echo "=== Setting up Draft-and-Prune devcontainer ==="

# --- Python virtual environment ---
echo ""
echo "Setting up Python virtual environment..."
if [ ! -d "${WORKSPACE_FOLDER}/.venv" ]; then
    python3 -m venv "${WORKSPACE_FOLDER}/.venv"
    "${WORKSPACE_FOLDER}/.venv/bin/pip" install --upgrade pip
    "${WORKSPACE_FOLDER}/.venv/bin/pip" install -r "${WORKSPACE_FOLDER}/requirements.txt"
    "${WORKSPACE_FOLDER}/.venv/bin/pip" install 'jupyter-mcp-server>=0.15.0'
    # scitools-pyke uses deprecated 'imp' module removed in Python 3.12
    bash "${WORKSPACE_FOLDER}/patch_pyke.sh"
    echo "✓ Python venv created and requirements installed"
else
    echo "✓ Python venv already exists"
fi

# --- acl2-mcp ---
echo ""
echo "Setting up acl2-mcp..."
if ! "${WORKSPACE_FOLDER}/.venv/bin/python" -c "import acl2_mcp" 2>/dev/null; then
    echo "Installing acl2-mcp from GitHub..."
    "${WORKSPACE_FOLDER}/.venv/bin/pip" install "git+https://github.com/jimwhite/acl2-mcp.git"
    echo "✓ acl2-mcp installed"
else
    echo "✓ acl2-mcp already installed"
fi

# --- acl2-kg-mcp ---
echo ""
echo "Setting up acl2-kg-mcp..."
if ! "${WORKSPACE_FOLDER}/.venv/bin/python" -c "import acl2_kg_mcp" 2>/dev/null; then
    echo "Installing acl2-kg-mcp from GitHub..."
    "${WORKSPACE_FOLDER}/.venv/bin/pip" install "git+https://github.com/wiki3-ai/acl2-kg-mcp.git"
    echo "✓ acl2-kg-mcp installed"
else
    echo "✓ acl2-kg-mcp already installed"
fi

echo ""
echo "=== Setup complete! ==="
echo "  - Python venv: ${WORKSPACE_FOLDER}/.venv"
echo "  - acl2-mcp: ${WORKSPACE_FOLDER}/.venv/bin/acl2-mcp"
echo "  - acl2-kg-mcp: ${WORKSPACE_FOLDER}/.venv/bin/acl2-kg-mcp"
