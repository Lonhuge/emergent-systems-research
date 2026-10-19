#!/usr/bin/env bash
# Viability calibration on seeds 100-102 (never used for results). Usage: ./calibrate.sh TAG
set -u
cd "$(dirname "$0")"
TAG="$1"
for c in full no_coupling shuffle_phase no_migration no_evolution; do
  for s in 100 101 102; do
    if [ "$s" = 100 ]; then AUD="0:4,26:30,56:60"; else AUD=""; fi
    ./run_sandboxed.sh --condition "$c" --seed "$s" --seconds 60 --tag "$TAG" --audio "$AUD" > /dev/null 2>&1 &
    while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 2; done
  done
done
wait
python3 -I calib_view.py "$TAG"
echo CALIBRATION_DONE
