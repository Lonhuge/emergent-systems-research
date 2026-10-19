#!/usr/bin/env bash
# Sandbox wrapper (see ../../PRINCIPLES.md §2): empty env, isolated python,
# 4 GB memory, 2 h CPU and wall clock, single-threaded math.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 4000000
ulimit -t 7200
exec env -i PATH=/usr/bin:/bin HOME=/nonexistent LANG=C.UTF-8 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 7200 python3 -I "$DIR/run.py" "$@"
