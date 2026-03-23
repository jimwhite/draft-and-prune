#!/usr/bin/env bash
# patch_pyke.sh — Fix scitools-pyke for Python ≥ 3.12
#
# The `imp` module was removed in Python 3.12.  scitools-pyke 1.1.1 uses
# `imp.reload()` in two files.  This script replaces those calls with the
# modern `importlib.reload()`.
#
# Run after: pip install -r requirements.txt

set -euo pipefail

SITE_PACKAGES=$(python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")
PYKE_DIR="$SITE_PACKAGES/pyke"

if [ ! -d "$PYKE_DIR" ]; then
    echo "pyke not found at $PYKE_DIR — skipping patch"
    exit 0
fi

for f in "$PYKE_DIR/knowledge_engine.py" "$PYKE_DIR/target_pkg.py"; do
    if [ -f "$f" ] && grep -q "^import imp$" "$f"; then
        sed -i 's/^import imp$/import importlib/' "$f"
        sed -i 's/imp\.reload/importlib.reload/g' "$f"
        echo "Patched: $f"
    else
        echo "Already patched or not found: $f"
    fi
done

echo "pyke patch complete."
