#!/usr/bin/env bash
# Fast notes main runs as pre-registered: 4 conditions x seeds 0-499.
set -u
cd "$(dirname "$0")"
for c in no_migration full no_coupling shuffle_phase; do
  for chunk in "0:125" "125:250" "250:375" "375:500"; do
    ./run_notes_sandboxed.sh --condition "$c" --seeds "$chunk" --tag main --audio-below 10 > /dev/null 2>&1 &
    while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 3; done
  done
done
wait
echo NOTES_DONE "$(cat results/notes_main__*.jsonl | wc -l)" notes
