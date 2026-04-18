"""
CS5800 A* Pathfinding Visualizer — Grid

Models the maze as a weighted graph G = (V, E) with non-negative edge
weights (CLRS Ch. 22).  Each cell is a vertex; edges connect 4-directional
neighbours.  Edge weight to enter cell (r, c) equals TERRAIN_COST[terrain].
"""
from __future__ import annotations

try:
    from .constants import GRID_N, TERRAIN_COST, TERRAIN_COLOR
except ImportError:
    from constants import GRID_N, TERRAIN_COST, TERRAIN_COLOR


class Grid:
    """
    20 × 20 weighted grid.

    cells[row][col] ∈ {'empty', 'grass', 'swamp', 'wall'}
    start / goal are (row, col) tuples stored separately so the terrain
    beneath them can still carry a cost.
    """

    def __init__(self, rows: int = GRID_N, cols: int = GRID_N) -> None:
        self.rows = rows
        self.cols = cols
        self.cells: list[list[str]] = [
            ['empty'] * cols for _ in range(rows)
        ]
        self.start: tuple[int, int] = (rows // 2, 2)
        self.goal:  tuple[int, int] = (rows // 2, cols - 3)

    # ── Cell access ────────────────────────────────────────────────────────

    def get_terrain(self, r: int, c: int) -> str:
        """Return terrain type of the given cell."""
        return self.cells[r][c]

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_cost(self, r: int, c: int) -> float:
        """Entering cost for cell (r, c); inf for walls."""
        return TERRAIN_COST[self.cells[r][c]]

    def walkable(self, r: int, c: int) -> bool:
        return self.cells[r][c] != 'wall'

    def base_color(self, r: int, c: int) -> tuple[int, int, int]:
        return TERRAIN_COLOR[self.cells[r][c]]

    # ── Editing ────────────────────────────────────────────────────────────

    def set_terrain(self, r: int, c: int, terrain: str) -> None:
        """Place terrain; protect start and goal from overwrite."""
        if not self.in_bounds(r, c):
            return
        if (r, c) in (self.start, self.goal):
            return
        self.cells[r][c] = terrain

    def move_start(self, r: int, c: int) -> None:
        if self.in_bounds(r, c) and (r, c) != self.goal:
            # Clear wall so start is never on a blocked cell
            if self.cells[r][c] == 'wall':
                self.cells[r][c] = 'empty'
            self.start = (r, c)

    def move_goal(self, r: int, c: int) -> None:
        if self.in_bounds(r, c) and (r, c) != self.start:
            # Clear wall so goal is never on a blocked cell
            if self.cells[r][c] == 'wall':
                self.cells[r][c] = 'empty'
            self.goal = (r, c)

    def clear(self) -> None:
        """Reset all terrain to empty; restore default start/goal."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c] = 'empty'
        self.start = (self.rows // 2, 2)
        self.goal  = (self.rows // 2, self.cols - 3)

    # ── Graph interface ────────────────────────────────────────────────────

    def neighbors(self, r: int, c: int) -> list[tuple[int, int]]:
        """4-connected walkable neighbours in-bounds."""
        result = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.walkable(nr, nc):
                result.append((nr, nc))
        return result

    def is_ready(self) -> bool:
        """True when start and goal are placed (they always are after clear)."""
        return self.start is not None and self.goal is not None

    # ── Preset maps ────────────────────────────────────────────────────────

    def load_barrier(self) -> None:
        """Vertical wall barrier forcing a detour — classic A* demo."""
        self.clear()
        mid_c = self.cols // 2
        for r in range(self.rows):
            if r != self.rows // 4 and r != 3 * self.rows // 4:
                self.cells[r][mid_c] = 'wall'

    def load_maze(self) -> None:
        """Hand-crafted maze with mixed terrain."""
        self.clear()
        walls = [
            # outer gaps removed; inner wall segments
            (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
            (2, 7), (3, 7), (4, 7),
            (6, 7), (7, 7), (8, 7), (9, 7),
            (4, 11), (5, 11), (6, 11), (7, 11), (8, 11),
            (2, 15), (3, 15), (4, 15),
            (10, 3), (11, 3), (12, 3),
            (12, 7), (13, 7), (14, 7),
            (10, 11), (10, 12), (10, 13),
            (14, 11), (15, 11), (16, 11),
            (12, 15), (13, 15), (14, 15), (15, 15),
        ]
        for r, c in walls:
            if (r, c) not in (self.start, self.goal):
                self.cells[r][c] = 'wall'
        # swamp patches
        for r, c in [(7, 4), (7, 5), (8, 4), (8, 5), (9, 4),
                     (3, 12), (3, 13), (4, 12), (4, 13)]:
            if (r, c) not in (self.start, self.goal):
                self.cells[r][c] = 'swamp'
        # grass patches
        for r, c in [(14, 4), (15, 4), (16, 4), (14, 5),
                     (5, 16), (6, 16), (5, 17), (6, 17)]:
            if (r, c) not in (self.start, self.goal):
                self.cells[r][c] = 'grass'

    def load_random(self, wall_prob: float = 0.25, seed: int | None = None) -> None:
        """Random obstacle field.  seed=None → truly random each time."""
        import random
        rng = random.Random(seed)
        self.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in (self.start, self.goal):
                    continue
                roll = rng.random()
                if roll < wall_prob:
                    self.cells[r][c] = 'wall'
                elif roll < wall_prob + 0.10:
                    self.cells[r][c] = 'swamp'
                elif roll < wall_prob + 0.18:
                    self.cells[r][c] = 'grass'
