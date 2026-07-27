#!/usr/bin/env bash
# SAF — install the git hooks by pointing core.hooksPath at the versioned folder.
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "not a git repo" >&2; exit 1; }
cd "$ROOT"

git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true

echo "SAF: core.hooksPath -> .githooks (commit-msg + pre-commit active)"
