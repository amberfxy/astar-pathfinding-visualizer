# CS 5800 Project Final Report

## Interactive A* Pathfinding Puzzle Game

**Team members:** Jiaxin Jia, Xiaoyuan Lu, Xinyuan Fan  
**Course:** CS 5800

## Abstract

This project implements a browser-based interactive visualizer for comparing Dijkstra, A* with Manhattan distance, and A* with Euclidean distance on the same weighted 20x20 grid. Users can paint walls and weighted terrain, reposition the start and goal, and watch all three algorithms run side by side. The main goal is to study how admissible heuristics affect search efficiency while preserving optimality on a 4-direction weighted grid. The system records nodes expanded, path cost, path length, runtime, and whether a path is found. In the benchmark already used on the project poster, which matches the current barrier preset, all three algorithms reached path cost 25.0 while A* Manhattan expanded 183 nodes, A* Euclidean expanded 233 nodes, and Dijkstra expanded 368 nodes. These results support the project’s main claim: admissible heuristics can preserve optimal-cost solutions while reducing search effort on the same input.

## Introduction

This project studies how heuristic choice affects the behavior of A* search in a weighted grid environment while preserving optimality. In many algorithms courses, students learn shortest-path methods through pseudocode and proofs, but it is much harder to build intuition for how the search frontier actually evolves from one step to the next. A* is a particularly useful case study because its correctness depends on a clear relationship between path cost and heuristic estimates, yet its practical efficiency can change significantly depending on the heuristic being used.

To make this behavior easier to observe, we built an interactive pathfinding visualizer with lightweight puzzle-game elements. The system allows a user to paint walls and weighted terrain, move the start and goal, and then run Dijkstra, A* with Manhattan distance, and A* with Euclidean distance on the same grid at the same time. This shared-input setting makes it possible to compare expansion behavior, path cost, and other metrics directly instead of relying only on static pseudocode examples. The project is implemented in Python/Pygame and delivered through a browser-based web build.

Our central question is: **How do different admissible heuristics affect A* search efficiency on a weighted 4-direction grid while preserving optimality?** In our implementation, efficiency is primarily measured by nodes expanded, while correctness is checked using path cost on the same terrain configuration.

We chose this topic because it connects core shortest-path concepts from class to a concrete visual system. The project also gave us a way to combine algorithm design, interactive visualization, and evidence-based comparison in one deliverable. Rather than presenting A* only as an abstract formula, we wanted to show how the search actually behaves under different heuristics and map configurations.

## Technical Discussion and Analysis

### Problem Setup

The environment is a 20x20 weighted grid. Each cell is treated as a vertex in a graph, and each walkable edge connects one cell to one of its four orthogonal neighbors. The cost of moving into a cell depends on its terrain type:

- `empty`: cost 1
- `grass`: cost 2
- `swamp`: cost 5
- `wall`: blocked

The user can place weighted terrain, reposition the start and goal, and choose from preset maps such as a maze, a barrier configuration, and a random map. The same edited grid is then used by all three search panels so that differences in performance come from the search strategy rather than from different inputs.

### Development Steps

We approached the project in a sequence of concrete implementation steps. First, we modeled the weighted grid and its terrain-dependent traversal costs. Second, we implemented a shared search framework that could run Dijkstra and multiple A* heuristic variants on the same input. Third, we added a side-by-side visualization so that the search process could be observed rather than only measured after termination. Fourth, we added interaction features such as terrain painting, preset maps, start/goal repositioning, and step-through controls. Finally, we logged run results to a CSV file so that representative runs could be compared outside the live demo.

This sequence matters because the final project is not only an algorithm implementation; it is also a comparison environment. The visualization and logging layers are therefore part of the methodology rather than just presentation details.

### Methodology and Implementation

The implementation compares three algorithms:

- Dijkstra
- A* with Manhattan distance
- A* with Euclidean distance

The search core is implemented as a unified generator-based framework. Dijkstra serves as the uninformed baseline and is implemented as A* with `h(n)=0`. Each search keeps a min-heap open set, a closed set, `g` values, `f` values, and predecessor pointers for path reconstruction. After each node expansion, the algorithm yields a state snapshot so the user interface can render the current frontier, expanded nodes, and score values step by step. This structure makes the comparison visual and synchronized across all three algorithms.

The generator design is important for the methodology because the goal of the project is not only to compute a shortest path, but also to make the search process observable. By yielding the intermediate state after each expansion, the visualizer can show how the heuristic changes the order in which nodes are explored. This is one of the main ways the system turns algorithm behavior into something easier to interpret.

Under the current 4-direction, nonnegative-cost grid model, both Manhattan distance and Euclidean distance are admissible heuristics. This lets the project compare efficiency differences while preserving optimality of path cost on the same input.

The interface is implemented in Pygame as a three-panel visualizer and packaged into a browser-usable web build. Each panel corresponds to one algorithm. Users can paint terrain directly on the grid, use preset maps, run all three algorithms simultaneously, pause, step through the search, and toggle `f(n)` overlays. The interface also includes two puzzle-style mechanics already present in the implementation: a wall-limited mode that allows up to five placed wall cells at a time and a path-prediction mode that compares a user’s predicted cost to the algorithm’s actual path cost.

### Inputs and Outputs

The system takes the following inputs:

- Grid terrain configuration
- Start and goal positions
- Preset map choice, if used
- Optional user prediction path

The system produces the following outputs for each algorithm:

- Expanded nodes
- Path cost
- Path length
- Runtime as recorded by the current implementation
- Whether a path was found
- A visual trace of open-set, closed-set, current-node, and final-path behavior

These results are also appended to `metrics_log.csv`, which makes it possible to compare runs after the demo finishes. In the final analysis, path cost is treated as the main correctness metric, while runtime is treated more cautiously because it is environment-sensitive.

### Pseudocode

The following pseudocode reflects the actual generator-based search structure used in the implementation:

```text
function SearchGenerator(grid, heuristic):
    start <- grid.start
    goal <- grid.goal

    g[start] <- 0
    f[start] <- heuristic(start, goal)
    came_from[start] <- NIL

    open_heap <- min-heap containing (f[start], 0, start)
    open_set <- {start}
    closed <- {}
    counter <- 0

    while open_heap is not empty:
        (_, _, current) <- pop_min(open_heap)

        if current is in closed:
            continue

        remove current from open_set
        add current to closed

        yield snapshot(closed, open_set, current, f, g)

        if current = goal:
            path <- reconstruct_path(came_from, goal)
            return final_snapshot(path, g[goal], found=True)

        for each neighbor in walkable_4_neighbors(current):
            if neighbor is in closed:
                continue

            tentative_g <- g[current] + cost_to_enter(neighbor)

            if tentative_g < g.get(neighbor, infinity):
                g[neighbor] <- tentative_g
                came_from[neighbor] <- current
                f[neighbor] <- tentative_g + heuristic(neighbor, goal)
                counter <- counter + 1
                push(open_heap, (f[neighbor], counter, neighbor))
                add neighbor to open_set

    return final_snapshot(path=[], found=False)
```

In this framework, Dijkstra is implemented as A* with a zero heuristic. Manhattan and Euclidean are both admissible under the current 4-direction, nonnegative-cost grid model, so the project compares their efficiency while preserving optimality of path cost.

### Time Complexity

The search uses a min-heap priority queue for the open set. Under the standard graph interpretation, the time complexity is approximately \(O(|E| + |V| \log |V|)\), with \(O(|V|)\) additional space for the score maps, predecessor structure, and heap contents. In the current project, the graph is a grid, so \(|V|\) is the number of cells and \(|E|\) is the number of walkable neighbor connections.

### Results and Testing

The current evaluation evidence comes from the poster benchmark, the logged CSV runs, the implemented test scenarios in the visualizer, and a final consistency check against the current codebase. We do **not** claim a fully automated large-scale experiment pipeline in this report because that is not part of the current evidence set.

The clearest benchmark already used in the project materials is the benchmark shown on the poster, which matches the current barrier preset configuration in the implementation. In that run:

- Dijkstra expanded 368 nodes
- A* Manhattan expanded 183 nodes
- A* Euclidean expanded 233 nodes
- All three recorded path cost 25.0
- All three recorded path length 26

This benchmark shows the intended comparison clearly: under the same weighted-grid input, both A* heuristics reached an optimal-cost solution while expanding fewer nodes than Dijkstra, and Manhattan expanded fewer nodes than Euclidean in this case.

The current materials also support additional functional scenarios and consistency checks:

- An empty-grid case used to validate basic behavior
- A barrier map that forces a detour
- A no-path case in which the goal is blocked and the algorithm terminates with `found = False`
- Repeated reruns of the barrier, maze, and random-seed maps to confirm stable node-expansion and path-cost values on the current implementation

For a weighted-grid project, path cost is the most important correctness metric. Path length can still be reported, but it should be treated as secondary because multiple optimal paths can have the same total cost while using different numbers of cells. For that reason, our interpretation of correctness focuses primarily on whether the compared algorithms reach the same optimal-cost solution on the same map. Runtime is recorded by the system, but this report does not use runtime as a headline result.

### Use of GenAI

Based on the current project materials, GenAI was used to support planning and writing rather than to directly produce the finished implementation. The proposal explicitly states that GenAI was used to refine user-interface ideas, experiment design, pseudocode structure, and report organization. The proposal text also records drafting assistance from GPT and summarization assistance from Gemini.

GenAI was most useful when we were refining the project from a broad idea into a more structured and presentable question. Instead of treating pathfinding only as a generic coding problem, we narrowed the project toward a specific comparison of admissible heuristics on the same weighted 4-direction grid. This refinement helped make the project more open-ended and more suitable for algorithmic analysis, because the final deliverable was not just a single path output but an environment for comparing search behavior and metrics.

A conservative description for the final submission is:

> We used GenAI primarily as a planning and writing assistant. It helped refine our project framing, clarify our experimental goals, improve pseudocode structure, and improve how we explained the methodology and deliverables. The final implementation, algorithm behavior, and project-specific deliverables were still based on our own code, poster, and analysis.

This report should be paired with the reconstructed GenAI appendix prepared for the submission set. That appendix is intentionally described as reconstructed from team recollection rather than presented as a raw exported chat log.

### How Our Solution Differs from Direct GenAI Solutions

This project is not simply a direct GenAI answer to a pathfinding question. A direct GenAI response could explain A* in words or produce a one-time solution for a single input, but our project implements a reusable interactive environment for comparing multiple search strategies on the same weighted grid. The user can construct inputs, observe step-by-step frontier changes in the web interface, and collect quantitative metrics such as path cost and nodes expanded.

The project is also tailored to a specific course goal: understanding heuristic behavior through direct comparison. Instead of asking an AI system to return a path, we created a system that exposes the search process itself. This makes the contribution different from a generic AI-generated answer because the project’s value is in the comparison environment, the visualization, and the structured algorithmic analysis.

We do **not** claim a formal survey of all existing online pathfinding tools in this report. A safer and more accurate claim is that our project provides a custom interactive comparison setting designed specifically for heuristic analysis in CS 5800.

### Limitations and Future Work

The current implementation has several limitations:

- The grid size is fixed at 20x20.
- Movement is limited to four directions.
- Only three search modes are implemented in the comparison view.
- The current evidence focuses on representative logged runs rather than a large automated experiment suite.
- The report currently relies on existing logged data rather than a newly generated clean experimental dataset.

These limitations suggest several directions for future work:

- Add a headless batch experiment pipeline across many seeds and obstacle densities
- Add more admissible heuristics for comparison
- Expand the visual analysis with cleaner plots and summary tables
- Generalize to additional movement models while rechecking heuristic admissibility
- Extend the game-like mechanics into more advanced interactive modes

### Collaboration

The proposal divided the work into three broad areas: interface and visualization, algorithm implementation, and evaluation/report organization. This division is consistent with the shape of the final project: the system required both algorithmic work and interface work, and the final deliverables also depended on metric collection and written analysis. Repository history also shows contributions under multiple author names that map to the final team roster.

For consistency in the final archived submission, the repository author names should be interpreted as follows:

- `Jiaxin Jia` corresponds to Jiaxin Jia
- `Amber` corresponds to Xinyuan Fan
- `algernon` corresponds to Xiaoyuan Lu
- `Xiaoyuan` also corresponds to Xiaoyuan Lu

## Conclusion

This project implemented an interactive A* pathfinding visualizer with puzzle-style features to study heuristic efficiency on a weighted 4-direction grid. By running Dijkstra, A* Manhattan, and A* Euclidean on the same user-defined map, the system makes differences in search behavior visible rather than purely theoretical. The current benchmark evidence supports the main claim of the project: admissible heuristics can preserve optimality while reducing search effort, and the choice of heuristic affects how efficiently the search reaches an optimal-cost solution.

The strongest contribution of the project is not only the final path returned by the algorithms, but the side-by-side environment for observing, comparing, and explaining their behavior. By combining a weighted-grid model, synchronized visualization, and logged metrics, the project turns a shortest-path topic from the course into a concrete tool for heuristic analysis. The final result is a project-specific comparison environment rather than a one-time pathfinding answer, which is why the project remains meaningful even in a setting where direct AI-generated solutions already exist.

## References

1. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics, 4*(2), 100-107.
2. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. Chapter 3: Solving Problems by Searching.
