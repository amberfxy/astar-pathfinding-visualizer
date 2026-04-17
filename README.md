# Interactive A* Pathfinding Puzzle Game

Browser-based interactive side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted 20x20 grid. The project is implemented in Python/Pygame and includes a packaged web build.

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

### Browser-Based Web Build

```bash
open build/web/index.html
```

The repository includes a packaged web version in `build/web/`.

### Local Python Run

```bash
python main.py
```

A 1380x858 window opens showing three algorithm panels side by side in the local Pygame version.

## How to Use (Demo Guide)

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

Every completed run appends results to `metrics_log.csv` in the working directory. Fields:

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
main.py          — Pygame UI, event loop, rendering
algorithms.py    — Dijkstra and A* generators (min-heap priority queue)
grid.py          — Weighted grid model, terrain types, preset maps
constants.py     — Layout, colors, terrain costs, configuration
logger.py        — CSV metrics logging
requirements.txt — Python dependencies
```
