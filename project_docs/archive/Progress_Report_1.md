# CS 5800: Progress Report 1

**Team 4:** Jiaxin Jia, Xiaoyuan Lu, Xinyuan Fan
**Project Title:** An Interactive A* Pathfinding Puzzle Game

## 1. Executive Summary / Overview
The project is currently on track and we have successfully completed Phase 1 of our timeline. We have built a fully functional interactive A* Pathfinding Visualizer that runs three algorithms (Dijkstra, A* Manhattan, A* Euclidean) side-by-side on a customisable weighted grid. To enhance engagement, we integrated our first set of "puzzle game" mechanics: *Layer 1 (The Trap)*, where players have a limited number of walls to trick the A* heuristic, and *Layer 2 (The Swamp)*, where players can predict path costs before running the algorithms. We also implemented metric logging and dynamic visual effects. There are no major issues at this time, and we are prepared to transition into systematic data evaluation and advanced game modes.

## 2. Problem Statement
The central problem is to demonstrate how different admissible heuristics affect A* search efficiency (node expansions) while preserving path optimality in grids with varying terrain costs. 
*   **Inputs:** A 20x20 grid graph $G=(V, E)$. User inputs include start and goal coordinates, obstacle placements (walls with $cost = \infty$), and weighted terrain (grass with $cost = 2$, swamp with $cost = 5$). In the "Predict Path" mode, the input also includes a user-drawn sequence of nodes.
*   **Outputs:** The shortest path from start to goal, visualized step-by-step. The system outputs quantitative metrics for each algorithm: Nodes Expanded, Path Cost, Path Length, and Runtime (ms). For the prediction mode, it outputs the difference between predicted cost and actual algorithmic cost.
*   **Constraints:** The heuristics used must remain admissible. A* must process terrain edge weights accurately so that it correctly computes $g(n)$. The search frontier and $f(n)$ values must update visually without dropping frame rates, requiring a Generator-based step-by-step execution.

## 3. Algorithm Design
We are implementing **Dijkstra's Algorithm** and the **A* Search Algorithm**. Both utilize a greedy approach by always expanding the node with the lowest cost from a Priority Queue (Min-Heap). Dijkstra operates as a special case of A* where the heuristic $h(n) = 0$.

**Pseudocode (A* Search Generator):**
```text
function AStar_Generator(grid, start, goal, heuristic_func):
    open_set = Min-Heap()
    open_set.push( (heuristic_func(start), start) )
    g_score[start] = 0
    came_from = empty Map
    
    while open_set is not empty:
        current = open_set.pop_min()
        
        yield current_state  // Pauses execution for visualization
        
        if current == goal:
            return reconstruct_path(came_from, current)
            
        for neighbor in get_walkable_neighbors(current):
            tentative_g = g_score[current] + weight(current, neighbor)
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic_func(neighbor, goal)
                open_set.push( (f_score, neighbor) )
```

**Time & Space Complexity:**
*   **Time Complexity:** $O(|E| + |V| \log |V|)$ where $|V|$ is the number of grid cells and $|E|$ is the number of walkable edges. The Min-Heap allows for $O(\log |V|)$ extraction and insertion. In the worst-case (no heuristic / Dijkstra), we may explore all nodes.
*   **Space Complexity:** $O(|V|)$ since we must maintain the `g_score`, `came_from` pointers, and the Min-Heap, which at worst contains all vertices in the grid.

## 4. Work Completed
During the reporting period, we have successfully accomplished all Phase 1 deliverables and added interactive game layers:
*   **Algorithm Implementation (Xiaoyuan Lu):** Successfully implemented Dijkstra and A* using Python's `heapq` as a generator, allowing it to yield state frame-by-frame. Ensured algorithms correctly account for weighted edge costs. *(See attached Code Snippet 1 in Section 10).*
*   **UI & Interactive Game Layers (Jiaxin Jia):** Built the 3-panel UI using `pygame`. Created brushes for walls, grass, and swamp. Implemented *Layer 1: The Trap* (limiting wall placement to 5 blocks to teach players how to trap heuristics) and *Layer 2: The Swamp* (a "Predict Path" tool to compare human intuition against the AI).
*   **Visual Enhancements (Xinyuan Fan):** Added a dynamic sine-wave-based pulsing neon effect to the optimal path rendering. This prepares the visual style for our upcoming Layer 3/4 chasing mode and improves visual feedback.
*   **Metrics & Logging (Xinyuan Fan):** Implemented `logger.py` to automatically append run metrics (algorithm type, nodes expanded, path cost, runtime) to a `metrics_log.csv` file.

**Input Generated Close to Real Data:**
We generate maps structured as 2D arrays (`20x20` grid) with weighted terrains that simulate real-world traversal costs: 
- `Empty`: Cost 1 (Standard road)
- `Grass`: Cost 2 (Rough terrain)
- `Swamp`: Cost 5 (Difficult terrain)
- `Wall`: Cost $\infty$ (Obstacle)
*Example Random Input (seed=42):* A grid containing 25% walls, 10% swamps, and 18% grass scattered probabilistically, representing a realistic uneven landscape.

**Results Achieved (Quantitative Data):**
Based on our `metrics_log.csv`, running the three algorithms on a standard open grid with a vertical wall barrier yields clear efficiency differences:
- **Dijkstra** explored **272 nodes** to find the goal (Cost: 33.0).
- **A* Euclidean** explored **206 nodes** to find the goal (Cost: 33.0).
- **A* Manhattan** explored only **172 nodes** to find the goal (Cost: 33.0).
*Interpretation:* Manhattan distance dominates in a 4-way grid, reducing node expansion by ~36% compared to Dijkstra. However, in our "Layer 1: The Trap" mode, players successfully forced A* Manhattan to expand 208 nodes by placing a C-shaped wall, demonstrating its vulnerability to local optima.

**Initial Testing & Basic Test Cases:**
We created preset maps in `grid.py` to test edge cases:
1.  *Test Case 1 (Empty Grid):* Validates base optimality.
2.  *Test Case 2 (The Barrier):* A vertical wall splitting the map, forcing the algorithm to route around. Evaluates how heuristic values adjust to obstacles.
3.  *Test Case 3 (The Trap/Unreachable):* Surrounding the goal entirely with walls. The algorithm successfully halts and returns `found = False`, with Dijkstra expanding only 14 nodes before exhausting the open set. *(See attached Table 1 in Section 10 for detailed test data).*

## 5. Work in Progress
*   **Systematic Experimentation Pipeline (Xinyuan Fan - 30% complete):** We have the CSV logging working, but we need to write automated scripts that run the algorithms headless (without Pygame UI) across 100+ randomly generated seeds at different obstacle densities.
*   **Layer 3/4 Chase Mode Concept (Jiaxin Jia & Xiaoyuan Lu - 20% complete):** We are designing the logic where the goal node is a moving player, requiring the A* agent (the monster) to continuously recalculate its path on a neon grid.

## 6. Planned Work / Next Steps
In the next reporting period (Weeks 3-4), we plan to:
1.  **Data Analysis:** Run our headless experiments and generate comparative performance plots (e.g., Nodes Expanded vs. Obstacle Density) using `matplotlib` or `pandas`. (Target: April 3)
2.  **Advanced Game Mode:** Implement the Layer 4 Pacman-style chase mode using the neon visual effects recently added to the codebase. (Target: April 5)
3.  **Refinement:** Polish the on-screen $f(n)$ values visualization so they don't overlap on dense mazes, and ensure the UI scales cleanly.

## 7. Issues, Challenges & Risks
*   **Challenge - Generator State Management:** One issue we encountered was tracking the `f(n)` and `g(n)` values smoothly without slowing down Pygame's rendering thread. We resolved this by having the algorithm `yield` a highly optimized `AlgState` dataclass snapshot rather than recalculating UI colours on the fly.
*   **Risk - Heuristic Admissibility on Diagonals:** Currently, our grid is 4-way movement only. If we introduce 8-way (diagonal) movement later, we must be careful that our Manhattan heuristic does not overestimate cost, which would break A*'s guarantee of optimality. We will likely stick to 4-way to avoid this risk.

## 8. Schedule Status
We are **on time**, and slightly ahead of schedule regarding the interactive "game" elements (Predict Path and Tower Defense limits), which were originally stretched goals. The Phase 1 deliverables outlined in our proposal are complete.

## 9. Conclusion
The project is progressing excellently. The core algorithms function correctly, the visualizer is robust, and the game mechanics successfully translate abstract algorithm theory into engaging, testable user interactions. We are highly confident in meeting our final goals for Phase 2 data analysis and presentation. No immediate decisions are needed from stakeholders.

## 10. Attachments

### Table 1: Initial Test Case Results (Sample from metrics_log.csv)
| Test Case / Map Setup | Algorithm | Nodes Expanded | Path Cost | Found? | Runtime (ms) |
|---|---|---|---|---|---|
| **Test Case 1** (Empty Grid) | Dijkstra | 215 | 25.0 | True | ~2.50 |
| **Test Case 1** (Empty Grid) | A* Manhattan | 67 | 25.0 | True | ~0.85 |
| **Test Case 2** (Barrier Wall) | Dijkstra | 272 | 33.0 | True | ~3.15 |
| **Test Case 2** (Barrier Wall) | A* Manhattan | 172 | 33.0 | True | ~1.95 |
| **Test Case 3** (Surrounded/Trap) | Dijkstra | 14 | 0.0 | False | ~0.15 |
| **Test Case 3** (Surrounded/Trap) | A* Manhattan | 14 | 0.0 | False | ~0.15 |

### Code Snippet 1: A* Generator Implementation
```python
def _search_gen(grid: Grid, heuristic: Callable) -> Generator[AlgState, None, None]:
    start, goal = grid.start, grid.goal
    g, f = {start: 0.0}, {}
    came_from = {start: None}
    open_set, closed = {start}, set()
    counter = 0
    h0 = heuristic(start, goal)
    f[start] = h0
    heap = [(h0, counter, start)]

    state = AlgState(expanded=closed, open_set=open_set, current=None, f_vals=f, g_vals=g, path=[])

    while heap:
        _, _, pos = heapq.heappop(heap)
        if pos in closed: continue
        open_set.discard(pos)
        closed.add(pos)

        state.current = pos
        state.nodes_expanded = len(closed)
        yield state  # Yield for visual step-by-step update

        if pos == goal:
            state.path = _reconstruct(came_from, goal)
            state.path_cost, state.done, state.found = g[goal], True, True
            yield state
            return

        for nb in grid.neighbors(*pos):
            if nb in closed: continue
            tg = g[pos] + grid.get_cost(*nb)
            if tg < g.get(nb, float('inf')):
                g[nb] = tg
                came_from[nb] = pos
                hn = heuristic(nb, goal)
                f[nb] = tg + hn
                counter += 1
                heapq.heappush(heap, (tg + hn, counter, nb))
                open_set.add(nb)
```

### Code Snippet 2: Custom Grid Terrain Definitions
```python
TERRAIN_COST = {
    'empty': 1,
    'grass': 2,
    'swamp': 5,
    'wall':  float('inf'),
}

TERRAIN_COLOR = {
    'empty': (240, 240, 242),
    'grass': (120, 195,  75),
    'swamp': (130,  90,  40),
    'wall':  ( 38,  38,  48),
}
```

### GitHub Push History
*(🚨 TEAM: Please paste your screenshot of the Git history here. Explain below it that the screenshot demonstrates collaborative efforts where Jiaxin pushed UI changes, you pushed Layer 1/2 game modes, and Xinyuan pushed the recent dynamic neon path effects.)*
