# CS5800 A* Pathfinding Visualizer — Phase 1

Interactive side-by-side comparison of **Dijkstra**, **A\* (Manhattan)**, and **A\* (Euclidean)** on a weighted 20x20 grid.

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

```bash
python main.py
```

A 1380x820 window opens showing three algorithm panels side by side.

## How to Use (Demo Guide)

### Map Editing
- **Brush toolbar (top row):** Select Wall, Empty, Grass (cost 2), Swamp (cost 5), Start, Goal, or **Predict Path**.
- **Left-click / drag** on any panel's grid to paint with the selected brush.
- **Right-click / drag** to erase (set cell to Empty, or erase predicted path).
- **Preset maps:** Click Maze, Barrier, or Random for pre-built scenarios. Random generates a new layout each time.

### Gameplay Modes (New Features)
- **Layer 1: The Trap (Tower Defense)**: When using the **Wall** brush, you are limited to placing a maximum of **5 walls**. Use these limited walls to create traps and observe how A* Manhattan falls for local optima compared to Dijkstra.
- **Layer 2: The Swamp (Predict Path)**: Use the hot pink **Predict Path** brush to draw what you think will be the shortest path considering the terrain costs (Grass = 2, Swamp = 5). After drawing your path, click **Run** and check the comparison table at the bottom to see if your `Predict Cost` matches the actual `Path cost`!

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
| runtime_ms | Wall-clock runtime in milliseconds |
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
