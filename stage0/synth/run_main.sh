#!/usr/bin/env bash
# Main runs as pre-registered: 5 conditions x seeds 0-4 x 60 s, audio for every run.
set -u
cd "$(dirname "$0")"
for s in 0 1 2 3 4; do
  for c in full no_coupling shuffle_phase no_migration no_evolution; do
    ./run_sandboxed.sh --condition "$c" --seed "$s" --seconds 60 --tag main --audio "0:4,26:30,56:60" > /dev/null 2>&1 &
    while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 2; done
  done
done
wait
echo MAIN_DONE "$(ls results/main__*.json | wc -l)" runs
