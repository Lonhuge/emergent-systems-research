#!/usr/bin/env bash
# Sandbox wrapper for fast notes (see ../../PRINCIPLES.md §2).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 4000000
ulimit -t 7200
exec env -i PATH=/usr/bin:/bin HOME=/nonexistent LANG=C.UTF-8 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 7200 python3 -I "$DIR/run_notes.py" "$@"
