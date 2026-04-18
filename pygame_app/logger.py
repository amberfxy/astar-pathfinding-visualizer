"""
CS5800 A* Pathfinding Visualizer — Metrics Logger

Appends one CSV row per algorithm run so experiment data can be analysed
in Phase 2 (pandas / matplotlib pipeline).
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .algorithms import AlgState
    from .grid import Grid

LOG_PATH = Path(__file__).resolve().parent.parent / 'project_data' / 'metrics_log.csv'

FIELDNAMES = [
    'timestamp', 'algorithm', 'grid_hash',
    'grid_rows', 'grid_cols',
    'nodes_expanded', 'path_cost', 'path_length',
    'runtime_ms', 'found',
]


def _grid_hash(grid: 'Grid') -> str:
    flat = ''.join(c for row in grid.cells for c in row)
    flat += f'|{grid.start}|{grid.goal}'
    return hashlib.sha256(flat.encode()).hexdigest()[:10]


def log_run(
    algo_names: list[str],
    states: list['AlgState | None'],
    grid: 'Grid',
) -> None:
    """Append one row per algorithm to the CSV log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ghash = _grid_hash(grid)
    ts    = datetime.datetime.now().isoformat(timespec='seconds')

    write_header = not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0

    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()

        for name, state in zip(algo_names, states):
            if state is None:
                continue
            writer.writerow({
                'timestamp':      ts,
                'algorithm':      name,
                'grid_hash':      ghash,
                'grid_rows':      grid.rows,
                'grid_cols':      grid.cols,
                'nodes_expanded': state.nodes_expanded,
                'path_cost':      f'{state.path_cost:.4f}' if state.found else '0.0000',
                'path_length':    len(state.path) if state.found else 0,
                'runtime_ms':     f'{state.runtime_ms:.6f}',
                'found':          state.found,
            })

    print(f'[Logger] Results appended → {LOG_PATH.resolve()}')
