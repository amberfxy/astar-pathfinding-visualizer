# Interactive A* Pathfinding Visualizer

> Portfolio fork of a team pathfinding project.  
> Upstream: [pstereoluna/5800-Astar-Visualizer](https://github.com/pstereoluna/5800-Astar-Visualizer)  
> Live demo: [GitHub Pages](https://pstereoluna.github.io/5800-Astar-Visualizer/)

Interactive side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted 20×20 grid.

The repository includes:

- a **browser version** (`index.html` + JavaScript in `src/`)
- a **local Pygame version** (`python3 -m pygame_app`)

## Team

| Member | Focus |
|---|---|
| **Jiaxin Jia** | 3-panel Pygame UI, terrain editing, interaction design |
| **Xiaoyuan Lu** | Generator-based Dijkstra / A\* search core (min-heap open set) |
| **Xinyuan Fan (Amber)** | Prototyping, interactive gameplay features, metrics instrumentation, performance comparison |

## My Contributions (Xinyuan Fan / Amber)

- Prototyped early interactive pathfinding flows and contributed gameplay features (wall-limited mode, predict-path cost comparison)
- Built structured experiment logging (`pygame_app/logger.py`) with per-run metrics: nodes expanded, path cost, path length, runtime, success/failure, and grid-state hashing
- Fixed runtime measurement in the search loop so logged / on-screen timing reflects actual algorithm work
- Added path visualization polish (neon pulse) and UI layout fixes for control usability
- Benchmarked Dijkstra vs A\* heuristics on shared weighted-grid inputs; A\* Manhattan cut node expansions by ~50% vs Dijkstra at the same optimal path cost

Git author **Amber** = Xinyuan Fan.

## Features

- Weighted-grid pathfinding with terrain costs (empty / grass / swamp / wall)
- Synchronized three-panel visualization of Dijkstra vs two A\* heuristics
- Run / pause / step controls and `f(n)` overlays
- Preset maps (maze, barrier, random) and interactive map editing
- Local CSV experiment logging + browser demo via GitHub Pages

## Requirements

- Python 3.10+
- pygame >= 2.1.0

## Setup

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Running

### Browser Custom Mode

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000/](http://localhost:8000/).

Published demo: [https://pstereoluna.github.io/5800-Astar-Visualizer/](https://pstereoluna.github.io/5800-Astar-Visualizer/)

### Local Pygame Version

```bash
python3 -m pygame_app
```

## Feature Summary

### Shared Across Both Interfaces

- Weighted 20×20 grid
- Three simultaneous algorithm panels: Dijkstra, A\* Manhattan, A\* Euclidean
- Terrain painting (Wall, Grass, Swamp), movable start/goal
- Preset maps: Maze, Barrier, Random
- Run / Pause / Step and speed controls
- `f(n)` overlays and on-screen comparison metrics

### Local Pygame Only

- CSV logging to `project_data/metrics_log.csv`
- Wall-limited mechanic (up to 5 wall cells)
- Predict-path cost feedback

## Metric Logging

Local Pygame runs append rows to `project_data/metrics_log.csv`:

| Column | Description |
|---|---|
| timestamp | ISO timestamp of the run |
| algorithm | Dijkstra / A\* Manhattan / A\* Euclidean |
| grid_hash | SHA256 fingerprint of grid state |
| nodes_expanded | Number of nodes expanded |
| path_cost | Total path cost |
| path_length | Number of cells in path |
| runtime_ms | Recorded runtime (environment-sensitive) |
| found | Whether a path was found |

## Project Structure

```text
index.html                 — Browser / GitHub Pages entry
game.html                  — Legacy redirect
pygame_app/main.py         — Local Pygame UI
pygame_app/algorithms.py   — Dijkstra / A* generators
pygame_app/grid.py         — Weighted grid + presets
pygame_app/logger.py       — CSV metrics logging
src/states/customState.js  — Browser three-panel mode
src/utils.js               — Browser MinHeap utilities
project_docs/              — Design notes and writeups
project_data/              — Local metrics logs
```

## License

See repository license (MIT, matching upstream where applicable).
