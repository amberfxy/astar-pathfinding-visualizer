# Interactive A* Pathfinding Visualizer

> Personal portfolio fork of a CS 5800 team project.  
> Upstream: [pstereoluna/5800-Astar-Visualizer](https://github.com/pstereoluna/5800-Astar-Visualizer)  
> Live demo: [GitHub Pages](https://pstereoluna.github.io/5800-Astar-Visualizer/)

Interactive side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted 20×20 grid.

The repository includes:

- a **browser version** (`index.html` + JavaScript in `src/`)
- a **local Pygame version** (`python3 -m pygame_app`)

## Team

| Member | Role |
|---|---|
| **Jiaxin Jia** | UI / interactive visualization (3-panel Pygame interface, terrain brushes, game layers) |
| **Xiaoyuan Lu** | Core search algorithms (generator-based Dijkstra / A\* with min-heap) |
| **Xinyuan Fan (Amber)** | Evaluation, metrics logging, visual polish, benchmarking & report support |

## My Contributions (Xinyuan Fan / Amber)

I focused on turning the visualizer into a **measurable comparison tool** and improving result presentation:

- **Metrics & logging** — implemented structured CSV logging (`pygame_app/logger.py`) for nodes expanded, path cost, path length, runtime, and success/failure, with grid-state hashing for reproducible runs
- **Benchmarking & analysis** — ran and interpreted side-by-side comparisons; representative results show A\* Manhattan reducing node expansions by about **50%** versus Dijkstra at equivalent optimal path cost
- **Visual polish** — contributed optimal-path neon pulse rendering and UI layout fixes (e.g. preset button positioning)
- **Runtime metric correctness** — fixed algorithm runtime calculation used in on-screen / logged metrics
- **Documentation & deliverables** — updated README / report materials and supported evaluation slides for the final presentation

Git commits under the author name **Amber** map to **Xinyuan Fan**.

## What We Built (Team)

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
project_docs/              — Course reports and notes
project_data/              — Local metrics logs
```

## License

See repository license (MIT, matching upstream where applicable).
