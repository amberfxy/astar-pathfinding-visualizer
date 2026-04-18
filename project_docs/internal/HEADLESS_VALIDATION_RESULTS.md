# Headless Validation Results

This file records fresh validation results against the current Python implementation in the GitHub repository.

## Scope

- Validation target: local Python implementation (`main.py`, `algorithms.py`, `grid.py`)
- Purpose: confirm benchmark values used in the report and slides
- Validation date: 2026-04-18
- Note: the browser custom mode was not used for this reproducibility check

## Verified Presets

### Barrier preset

- Dijkstra: nodes `368`, path cost `25.0`, path length `26`, found `True`
- A* Manhattan: nodes `183`, path cost `25.0`, path length `26`, found `True`
- A* Euclidean: nodes `233`, path cost `25.0`, path length `26`, found `True`

### Maze preset

- Dijkstra: nodes `274`, path cost `21.0`, path length `22`, found `True`
- A* Manhattan: nodes `53`, path cost `21.0`, path length `22`, found `True`
- A* Euclidean: nodes `64`, path cost `21.0`, path length `22`, found `True`

### Random map with seed 42

- Dijkstra: nodes `201`, path cost `34.0`, path length `24`, found `True`
- A* Manhattan: nodes `110`, path cost `34.0`, path length `24`, found `True`
- A* Euclidean: nodes `147`, path cost `34.0`, path length `28`, found `True`

## Interpretation

- The poster benchmark values are still reproducible in the current Python codebase.
- Those poster values correspond to the current `barrier` preset, not the current `random seed 42` map.
- On the weighted grid, `path cost` remains the main correctness metric.
- `path length` can differ across algorithms even when path cost matches.
- These reruns support the report wording that uses the barrier benchmark as the main published comparison and treats seed 42 as a separate checked scenario.

## Runtime Note

- Runtime remains environment-sensitive.
- Runtime should not be used as the headline comparison metric in the final write-up.
