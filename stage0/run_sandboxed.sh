#!/usr/bin/env bash
# Sandbox wrapper for stage 0 (see ../PRINCIPLES.md §2).
#  - empty environment: no proxy variables, no credentials, no PYTHON* settings
#  - python -I: isolated mode, ignores user site-packages and env
#  - ulimit: virtual memory 4 GB, CPU 2 h; timeout 2 h wall clock
#  - single-threaded BLAS so the limits are predictable
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 4000000
ulimit -t 7200
exec env -i PATH=/usr/bin:/bin HOME=/nonexistent LANG=C.UTF-8 \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 7200 python3 -I "$DIR/run_experiment.py" "$@"
