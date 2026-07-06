#!/usr/bin/env bash
# Creates (or reuses) an isolated virtualenv with `pypdf`, outside the repo,
# so extracting text from downloaded exam PDFs never touches system/project
# Python packages. Safe to run repeatedly - it's a no-op if the venv already
# has pypdf installed.
set -euo pipefail

VENV_DIR="${EXAM_HIERARCHY_SYNC_VENV:-$HOME/.cache/exam-hierarchy-sync/venv}"

if [ ! -x "$VENV_DIR/bin/python3" ]; then
    python3 -m venv "$VENV_DIR"
fi

if ! "$VENV_DIR/bin/python3" -c "import pypdf" 2>/dev/null; then
    "$VENV_DIR/bin/pip" install --quiet pypdf
fi

echo "$VENV_DIR/bin/python3"
