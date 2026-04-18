# Interactive A* Pathfinding Puzzle Game

Interactive side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted 20x20 grid.

The current repository contains two user-facing interfaces for the same comparison task:

- A **browser custom mode** launched from `index.html` and implemented with the web files in `src/`
- A **local Pygame version** launched from `python3 -m pygame_app`

Authors: Jiaxin Jia, Xiaoyuan Lu, Xinyuan Fan

## Requirements

- Python 3.10+
- pygame >= 2.1.0

## Setup

```bash
# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running

### Browser Custom Mode

```bash
# Run from the repository root
python3 -m http.server 8000
```

Then open:

- [http://localhost:8000/](http://localhost:8000/)

This mode uses browser-side JavaScript modules from `src/`, so a local static server is the safest way to run it.

`index.html` is also the repository's GitHub Pages entry point. The browser version is published at [https://pstereoluna.github.io/5800-Astar-Visualizer/](https://pstereoluna.github.io/5800-Astar-Visualizer/). The older `game.html` path is kept as a redirect to the same browser interface.

### Local Python Run

From the repository root:

```bash
python3 -m pygame_app
```

Or from inside `pygame_app/`:

```bash
python3 main.py
```

A 1380x858 window opens showing three algorithm panels side by side in the local Pygame version.

## Feature Summary

### Shared Across Both Interfaces

- Weighted 20x20 grid
- Three simultaneous algorithm panels:
  - Dijkstra
  - A* Manhattan
  - A* Euclidean
- Terrain painting with Wall, Grass, and Swamp
- Repositionable start and goal
- Preset maps: Maze, Barrier, Random
- Run / Pause / Step controls
- Speed controls
- `f(n)` overlays
- On-screen comparison metrics

### Local Pygame Version Only

- CSV logging to `project_data/metrics_log.csv`
- Wall-limited mechanic with up to 5 placed wall cells at a time
- Predict-path cost feedback in the panel footer

### Browser Custom Mode Notes

- The browser custom mode focuses on the core side-by-side comparison interface
- It is now structured so the root `index.html` can be served directly by GitHub Pages
- It displays metrics on screen but does **not** append runs to `project_data/metrics_log.csv`

## Local Pygame Demo Guide

### Map Editing
- **Brush toolbar (top row):** Select Wall, Empty, Grass (cost 2), Swamp (cost 5), Start, Goal, or Predict Path.
- **Left-click / drag** on any panel's grid to paint with the selected brush.
- **Right-click / drag** to erase (set cell to Empty).
- **Wall-limited mechanic:** The current implementation allows up to 5 placed wall cells at a time.
- **Predict Path mode:** Paint a predicted route to compare your predicted cost with the algorithm's path cost.
- **Preset maps:** Click Maze, Barrier, or Random for pre-built scenarios. Random generates a new layout each time.

### Running Algorithms
- Press **R** or click **Run** to start all three algorithms simultaneously.
- Press **Space** or click **Pause** to pause/resume animation.
- Press **Right arrow** or click **Step** to advance one expansion at a time.
- Adjust speed with the **Slow / Med / Fast / Max** buttons.

### Viewing Results
- Each panel shows expanded nodes (orange), open set (blue), current node (gold), and the optimal path (violet).
- Per-panel metrics appear below each grid: nodes expanded, path cost, path length, runtime.
- A comparison table appears at the bottom once all algorithms finish.
- Toggle **f(n) vals** to show/hide f-values on expanded cells.

### Other Controls
- **C** — Clear the entire grid.
- **H** — Toggle f(n) value overlay.
- **Q / Esc** — Quit.

## Metric Logging

In the **local Pygame version**, every completed run appends results to `project_data/metrics_log.csv`. Fields:

| Column | Description |
|---|---|
| timestamp | ISO timestamp of the run |
| algorithm | Dijkstra / A* Manhattan / A* Euclidean |
| grid_hash | SHA256 fingerprint of grid state |
| grid_rows, grid_cols | Grid dimensions |
| nodes_expanded | Number of nodes expanded |
| path_cost | Total path cost (0.0 if no path) |
| path_length | Number of cells in path (0 if no path) |
| runtime_ms | Runtime in milliseconds as recorded by the current search implementation; this value is environment-sensitive |
| found | Whether a path was found |

## Project Structure

```
index.html               — Root browser entry point for static hosting / GitHub Pages
game.html                — Legacy redirect to the root browser entry point
pygame_app/main.py       — Local Pygame UI, event loop, rendering
pygame_app/algorithms.py — Python Dijkstra and A* generators
pygame_app/grid.py       — Weighted grid model, terrain types, preset maps
pygame_app/constants.py  — Layout, colors, terrain costs, configuration
pygame_app/logger.py     — CSV metrics logging for the local version
src/states/customState.js — Browser-side three-panel custom mode
src/utils.js             — Shared browser-side utilities, including MinHeap
project_docs/            — Submission drafts, internal notes, and archive material
project_data/            — Local runtime outputs such as CSV metrics logs
requirements.txt         — Python dependencies
```
