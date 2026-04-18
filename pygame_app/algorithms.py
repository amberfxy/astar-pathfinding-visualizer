"""
CS5800 A* Pathfinding Visualizer — Search Algorithms

Implements Dijkstra and A* as Python generators so the caller can consume
one node-expansion at a time for step-by-step animation.

Data structure: Min-Heap (heapq) for the Open Set → O(log V) extraction.
Reference: CLRS Ch. 6 (Binary Heaps), Ch. 24 (Dijkstra / Shortest Paths).

Admissibility:
  h_manhattan(n) = |Δrow| + |Δcol|  ≤ true cost (min edge cost = 1) ✓
  h_euclidean(n) = √(Δrow²+Δcol²)  ≤ manhattan ≤ true cost          ✓
  h_zero(n)      = 0                 → degrades A* to Dijkstra        ✓
"""
from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field
from typing import Callable, Generator

try:
    from .grid import Grid
except ImportError:
    from grid import Grid


# ── Heuristics ─────────────────────────────────────────────────────────────

def h_zero(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    return 0.0


def h_manhattan(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    return float(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))


def h_euclidean(pos: tuple[int, int], goal: tuple[int, int]) -> float:
    return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5


# ── Search state (yielded each step) ───────────────────────────────────────

@dataclass
class AlgState:
    """
    Snapshot yielded after each node expansion.
    All sets/dicts are references to the internal algorithm state,
    valid until the next generator advance.
    """
    expanded:       set[tuple[int, int]]            # closed set
    open_set:       set[tuple[int, int]]            # current frontier
    current:        tuple[int, int] | None          # just expanded
    f_vals:         dict[tuple[int, int], float]    # f(n) for seen nodes
    g_vals:         dict[tuple[int, int], float]    # g(n) for seen nodes
    path:           list[tuple[int, int]]           # empty until found
    nodes_expanded: int  = 0
    path_cost:      float = 0.0
    runtime_ms:     float = 0.0
    done:           bool  = False
    found:          bool  = False


# ── Path reconstruction ─────────────────────────────────────────────────────

def _reconstruct(came_from: dict, goal: tuple) -> list[tuple]:
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur)
    return path[::-1]


# ── Core generator ──────────────────────────────────────────────────────────

def _search_gen(
    grid: Grid,
    heuristic: Callable[[tuple, tuple], float],
) -> Generator[AlgState, None, None]:
    """
    Unified A* / Dijkstra generator.

    Yields one AlgState per node expansion.  Final yield has done=True.
    Uses lazy deletion: stale heap entries are skipped on pop, so the
    heap may contain duplicates but each (row,col) is expanded at most once.
    """
    start, goal = grid.start, grid.goal
    t0 = time.perf_counter()

    # ── Initialise ─────────────────────────────────────────────────────────
    g: dict[tuple, float]    = {start: 0.0}
    f: dict[tuple, float]    = {}
    came_from: dict[tuple, tuple | None] = {start: None}

    open_set: set[tuple]  = {start}
    closed:   set[tuple]  = set()

    counter = 0
    h0 = heuristic(start, goal)
    f[start] = h0
    heap: list = [(h0, counter, start)]

    state = AlgState(
        expanded=closed,
        open_set=open_set,
        current=None,
        f_vals=f,
        g_vals=g,
        path=[],
    )

    accumulated_time = 0.0

    # ── Main loop ──────────────────────────────────────────────────────────
    while heap:
        t0 = time.perf_counter()
        _, _, pos = heapq.heappop(heap)

        if pos in closed:
            accumulated_time += time.perf_counter() - t0
            open_set.discard(pos)
            continue

        open_set.discard(pos)
        closed.add(pos)

        state.current        = pos
        state.nodes_expanded = len(closed)
        accumulated_time += time.perf_counter() - t0
        
        yield state          # ← one step of animation
        
        t0 = time.perf_counter()

        # ── Goal reached ───────────────────────────────────────────────────
        if pos == goal:
            state.path       = _reconstruct(came_from, goal)
            state.path_cost  = g[goal]
            accumulated_time += time.perf_counter() - t0
            state.runtime_ms = accumulated_time * 1000
            state.done       = True
            state.found      = True
            yield state
            return

        # ── Relax neighbours ───────────────────────────────────────────────
        for nb in grid.neighbors(*pos):
            if nb in closed:
                continue
            tg = g[pos] + grid.get_cost(*nb)
            if tg < g.get(nb, float('inf')):
                g[nb]         = tg
                came_from[nb] = pos
                hn            = heuristic(nb, goal)
                f[nb]         = tg + hn
                counter      += 1
                heapq.heappush(heap, (tg + hn, counter, nb))
                open_set.add(nb)
                
        accumulated_time += time.perf_counter() - t0

    # ── No path ────────────────────────────────────────────────────────────
    state.current        = None
    state.runtime_ms     = accumulated_time * 1000
    state.nodes_expanded = len(closed)
    state.done           = True
    state.found          = False
    yield state


# ── Public API ─────────────────────────────────────────────────────────────

def dijkstra_gen(grid: Grid) -> Generator[AlgState, None, None]:
    """Dijkstra = A* with zero heuristic (explores uniformly by cost)."""
    return _search_gen(grid, h_zero)


def astar_manhattan_gen(grid: Grid) -> Generator[AlgState, None, None]:
    """A* with admissible Manhattan distance heuristic."""
    return _search_gen(grid, h_manhattan)


def astar_euclidean_gen(grid: Grid) -> Generator[AlgState, None, None]:
    """A* with admissible Euclidean distance heuristic."""
    return _search_gen(grid, h_euclidean)
