#!/usr/bin/env bash
# Amendment A: 5 conditions x seeds 10-14 x 600 s.
set -u
cd "$(dirname "$0")"
for s in 10 11 12 13 14; do
  for c in full no_evolution no_migration no_coupling shuffle_phase; do
    ./run_sandboxed.sh --condition "$c" --seed "$s" --seconds 600 --log-every 1.0 --tag long \
      --audio "0:4,296:300,596:600" > /dev/null 2>&1 &
    while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 5; done
  done
done
wait
echo LONG_DONE "$(ls results/long__*.json 2>/dev/null | wc -l)" runs
