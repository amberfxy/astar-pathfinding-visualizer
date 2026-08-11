<div align="center">

# Interactive A* Pathfinding Visualizer

Side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted grid.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Browser-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Pygame](https://img.shields.io/badge/Pygame-Local%20UI-green)](https://www.pygame.org/)
[![Algorithms](https://img.shields.io/badge/Algorithms-A*%20%7C%20Dijkstra-0A66C2)](#features)
[![Demo](https://img.shields.io/badge/Live-GitHub%20Pages-222?logo=github)](https://pstereoluna.github.io/5800-Astar-Visualizer/)

**Team project** · Portfolio fork maintained by [@amberfxy](https://github.com/amberfxy) (**Amber Fan**)  
Upstream: [pstereoluna/5800-Astar-Visualizer](https://github.com/pstereoluna/5800-Astar-Visualizer) · [Live demo](https://pstereoluna.github.io/5800-Astar-Visualizer/)

</div>

---

Browser version (`index.html` + JavaScript) and local Pygame version (`python3 -m pygame_app`) on a weighted **20×20** grid.

## Team

| Member | Focus |
|--------|------|
| **Jiaxin Jia** | 3-panel Pygame UI, terrain editing, interaction design |
| **Xiaoyuan Lu** | Generator-based Dijkstra / A\* search core (min-heap open set) |
| **Amber Fan ([@amberfxy](https://github.com/amberfxy))** | Prototyping, interactive features, metrics logging, performance comparison |

## My contributions

- Prototyped interactive pathfinding flows and gameplay features (wall-limited mode, predict-path cost comparison)
- Built structured experiment logging (`pygame_app/logger.py`): nodes expanded, path cost, path length, runtime, success/failure, grid-state hashing
- Fixed runtime measurement so on-screen / logged timing reflects actual search work
- Path visualization polish and UI layout fixes
- Benchmarked Dijkstra vs A\* heuristics on shared weighted grids; **A\* Manhattan cut node expansions by ~50%** vs Dijkstra at the same optimal path cost

## Features

- Weighted-grid pathfinding with terrain costs (empty / grass / swamp / wall)
- Synchronized three-panel visualization: Dijkstra vs two A\* heuristics
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

### Browser

```bash
python3 -m http.server 8000
```

Open http://localhost:8000/  

Published demo: https://pstereoluna.github.io/5800-Astar-Visualizer/

### Local Pygame

```bash
python3 -m pygame_app
```

## Feature summary

### Shared (browser + Pygame)

- Weighted 20×20 grid
- Three algorithm panels: Dijkstra, A\* Manhattan, A\* Euclidean
- Terrain painting, movable start/goal, presets
- Run / Pause / Step, speed controls, `f(n)` overlays, on-screen metrics

### Pygame only

- CSV logging to `project_data/metrics_log.csv`
- Wall-limited mechanic (up to 5 wall cells)
- Predict-path cost feedback

## Metric logging

Local Pygame runs append to `project_data/metrics_log.csv`:

| Column | Description |
|--------|-------------|
| timestamp | ISO timestamp of the run |
| algorithm | Dijkstra / A\* Manhattan / A\* Euclidean |
| grid_hash | SHA256 fingerprint of grid state |
| nodes_expanded | Number of nodes expanded |
| path_cost | Total path cost |
| path_length | Number of cells in path |
| runtime_ms | Recorded runtime (environment-sensitive) |
| found | Whether a path was found |

## Project structure

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
