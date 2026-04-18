# CS 5800 Project Final Report

## Interactive A* Pathfinding Puzzle Game

**Team members:** Jiaxin Jia, Xiaoyuan Lu, Xinyuan Fan  
**Course:** CS 5800

## Abstract

This project builds an interactive visualizer to compare Dijkstra, A* with Manhattan distance, and A* with Euclidean distance on the same weighted 20x20 grid. The repository includes both a local Pygame version in `pygame_app/` and a browser version that can be served directly from the repository root. Users can paint walls and weighted terrain, move the start and goal, and watch all three algorithms run side by side. The main goal is to study how admissible heuristics affect search efficiency while still preserving optimality on a 4-direction weighted grid. The local Pygame version records nodes expanded, path cost, path length, runtime, and whether a path was found in `project_data/metrics_log.csv`, while the browser version shows the same comparison metrics on screen. In a representative barrier benchmark, all three algorithms reached the same path cost of 25.0, but they explored the grid differently: A* Manhattan expanded 183 nodes, A* Euclidean expanded 233 nodes, and Dijkstra expanded 368 nodes. This result helps answer our main question: different admissible heuristic functions can lead to different search behavior and different efficiency, even when the final path cost is the same.

## Introduction

This project studies how heuristic choice affects A* search on a weighted grid while still preserving optimality. In many algorithms classes, students learn shortest-path algorithms through pseudocode and proofs, but it is harder to build intuition for how the search frontier actually grows step by step. A* is a useful case because its correctness depends on the relationship between path cost and heuristic estimates, while its efficiency can change a lot depending on which heuristic is used.

To make this behavior easier to see, we built an interactive pathfinding visualizer with light puzzle-game elements. The system lets a user paint walls and weighted terrain, move the start and goal, and then run Dijkstra, A* with Manhattan distance, and A* with Euclidean distance on the same grid at the same time. Because all three algorithms use the same input, we can compare expansion behavior, path cost, and other metrics directly instead of relying only on static pseudocode examples. The current repository includes both a local Pygame version and a browser version built around the same comparison idea.

Our central question is: **How do different admissible heuristics affect A* search efficiency on a weighted 4-direction grid while preserving optimality?** In our implementation, efficiency is primarily measured by nodes expanded, while correctness is checked using path cost on the same terrain configuration.

We chose this topic because it connects shortest-path ideas from class to something concrete and visible. It also gave us a way to combine algorithm design, visualization, and result comparison in one project. Instead of showing A* only as an abstract formula, we wanted to show how the search actually behaves under different heuristics and map setups.

## Technical Discussion and Analysis

### Problem Setup

The environment is a 20x20 weighted grid. Each cell is treated as a vertex in a graph, and each walkable edge connects one cell to one of its four orthogonal neighbors. The cost of moving into a cell depends on its terrain type:

- `empty`: cost 1
- `grass`: cost 2
- `swamp`: cost 5
- `wall`: blocked

The user can place weighted terrain, reposition the start and goal, and choose from preset maps such as a maze, a barrier configuration, and a random map. The same edited grid is then used by all three search panels so that differences in performance come from the search strategy rather than from different inputs.

### Development Steps

We built the project in a clear sequence. First, we modeled the weighted grid and its terrain costs. Second, we implemented a shared search framework that could run Dijkstra and multiple A* heuristics on the same input. Third, we added a side-by-side visualization so that the search process could be seen, not just measured at the end. Fourth, we added interaction features such as terrain painting, preset maps, start/goal movement, and step-through controls. Finally, we logged run results to a CSV file so that representative runs could be compared outside the live demo.

This sequence matters because the project is not only an algorithm implementation. It is also a comparison environment. Because of that, the visualization and logging layers are part of the methodology, not just interface details.

### Implementation Iterations

The project also went through several iterations that improved clarity, reproducibility, and usability.

**Iteration 1: Core weighted-grid search comparison.** We first implemented the weighted grid model, the terrain-cost system, and the shared generator-based search framework for Dijkstra, A* Manhattan, and A* Euclidean. The goal at this stage was to make sure all three algorithms could run on the same input and be compared fairly under the same movement model and cost definition.

**Iteration 2: Interactive comparison environment.** After the baseline search logic was working, we added the synchronized three-panel visualizer, terrain editing, preset maps, and run/pause/step controls. The goal here was to make the search process visible so that heuristic behavior could be understood visually instead of only through the final path.

**Iteration 3: Logging and browser access.** Finally, we added metric logging for the local Pygame version and prepared a browser version rooted at `index.html`. The goal here was to make runs easier to validate across sessions and to make the same comparison environment available both locally and in the browser.

### Methodology and Implementation

The implementation compares three algorithms:

- Dijkstra
- A* with Manhattan distance
- A* with Euclidean distance

The search core is implemented as one generator-based framework. Dijkstra is the uninformed baseline and is implemented as A* with `h(n)=0`. Each search keeps a min-heap open set, a closed set, `g` values, `f` values, and predecessor pointers for path reconstruction. After each node expansion, the algorithm yields a state snapshot so the interface can render the current frontier, expanded nodes, and score values step by step. This structure makes the comparison visual and synchronized across all three algorithms.

We use a generator-based design so the algorithm can return its current state after each node expansion instead of only returning the final path. This allows the visualizer to show how the search progresses step by step and makes it easier to compare how different heuristics change the search order.

Under the current 4-direction, nonnegative-cost grid model, both Manhattan distance and Euclidean distance are admissible heuristics. This lets us compare efficiency differences while still preserving optimal path cost on the same input.

The repository currently provides two interfaces for this comparison task. The local version is implemented in Pygame as a three-panel visualizer under `pygame_app/`. The browser version is launched from `index.html` and uses the JavaScript files in `src/`, especially `src/states/customState.js`, to reproduce the same three-panel comparison idea in the browser. This browser entry is static-hosting friendly and is designed for direct GitHub Pages hosting from the repository root. In both interfaces, each panel corresponds to one algorithm, and the user can paint terrain on the grid, use preset maps, run all three algorithms at the same time, pause, step through the search, and toggle `f(n)` overlays.

The local Pygame version also includes two extra features that are not fully carried over to the browser version. One is a wall-limited mode, which allows up to five placed wall cells at a time. The other is a path-prediction mode, in which the user can guess a path and compare its cost with the algorithm's actual path cost. The browser version keeps the main side-by-side comparison and on-screen metrics, but it does not match every local Pygame feature exactly.

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

In the local Pygame version, these results are also appended to `project_data/metrics_log.csv`, which makes it possible to compare runs after the demo finishes. In the browser version, the metrics are shown on screen but are not written to the CSV file. In our analysis, path cost is the main correctness metric, while runtime is treated more cautiously because it depends on the environment.

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

### Libraries and External Functions Used

The project uses a small number of external libraries and standard-library functions that are directly tied to the implementation goals:

| Library / function | Reference | Where used | Goal of using it |
|---|---|---|---|
| `pygame.display.set_mode`, `pygame.draw.rect`, `pygame.event.get` | [6] | Local Pygame interface in `pygame_app/main.py` | These Pygame functions are used to create the local interactive window, draw the grid and controls, and process mouse/keyboard input in real time. |
| `heapq.heappush`, `heapq.heappop` | [3] | Search logic in `pygame_app/algorithms.py` | These standard-library priority-queue functions support efficient extraction of the next node with minimum `f(n)` or path cost. They are central to the Dijkstra and A* implementations. |
| `csv.DictWriter` | [4] | Logging in `pygame_app/logger.py` | This function writes one structured metrics row per algorithm run, which makes it easier to analyze benchmark output outside the live interface. |
| `hashlib.sha256` | [5] | Logging in `pygame_app/logger.py` | This function creates a compact fingerprint of the grid state so that logged benchmark rows can be tied back to the exact tested input. |
| `performance.now()` | [7] | Browser custom mode in `src/states/customState.js` | This browser-side timing function is used to record local runtime values during the JavaScript-based interface. |

The project also uses standard mathematical and drawing utilities such as `math.sin` for the path pulse effect and the HTML Canvas 2D drawing API inside the browser interface. We list only the main functions above because they are the most directly relevant to the project methodology, logging, and interaction design.

### Results and Testing

The current evaluation evidence comes from representative benchmark runs in the local Pygame version, the logged CSV output, the test scenarios built into the visualizer, and a final consistency check against the current codebase. We do **not** claim a large fully automated experiment pipeline in this report because that is not part of the current evidence set.

A representative barrier benchmark gives the clearest comparison and matches the current barrier preset in the implementation. In that run:

- Dijkstra expanded 368 nodes
- A* Manhattan expanded 183 nodes
- A* Euclidean expanded 233 nodes
- All three recorded path cost 25.0
- All three recorded path length 26

This benchmark shows the comparison clearly: on the same weighted-grid input, both A* heuristics reached an optimal-cost solution while expanding fewer nodes than Dijkstra, and Manhattan expanded fewer nodes than Euclidean in this case.

The current materials also support additional functional scenarios and consistency checks:

- An empty-grid case used to validate basic behavior
- A barrier map that forces a detour
- A no-path case in which the goal is blocked and the algorithm terminates with `found = False`
- Repeated reruns of the barrier, maze, and random-seed maps to confirm stable node-expansion and path-cost values on the current implementation

The main test scenarios can be summarized more explicitly as inputs and outputs:

| Test scenario | Input | Observed output | Why it matters |
|---|---|---|---|
| Empty grid | 20x20 grid with no blocking walls and the same start/goal given to all three algorithms | All algorithms find a path and provide a clean baseline for expansion behavior | Confirms the implementation works in the simplest reachable case |
| Barrier preset | Weighted grid with a forced detour using the current barrier preset | Dijkstra 368 expansions, A* Manhattan 183, A* Euclidean 233, with common path cost 25.0 | Serves as the clearest comparative benchmark for efficiency under the same input |
| No-path case | Goal region manually blocked so no legal path exists | All algorithms terminate with `found = False` rather than looping or returning a false solution | Confirms correct failure behavior |
| Random seed 42 | Current random map generated from the implementation's seeded configuration | Common path cost 34.0 with 201, 110, and 147 expansions, while path length differs for A* Euclidean | Shows why path cost is a stronger correctness metric than path length on weighted terrain |

Fresh reruns against the current Python implementation confirm that the barrier preset still produces the same benchmark values. They also confirm that the current maze preset produces path cost 21.0 with node expansions 274, 53, and 64 for Dijkstra, A* Manhattan, and A* Euclidean. For the current random map with seed 42, the rerun values are 201, 110, and 147 expanded nodes with common path cost 34.0, while path length differs for A* Euclidean. This is another reason to treat path cost, not path length, as the main correctness metric on a weighted grid.

For a weighted-grid project, path cost is the most important correctness metric. Path length can still be reported, but it is secondary because multiple optimal paths can have the same total cost while using different numbers of cells. For that reason, we focus mainly on whether the compared algorithms reach the same optimal-cost solution on the same map. Runtime is recorded by the system, but this report does not use runtime as a main result.

### Use of GenAI

Based on the current project materials, GenAI was used mainly for planning and writing support rather than to directly produce the final implementation. The proposal states that GenAI was used to refine interface ideas, experiment design, pseudocode structure, and report organization. The proposal text also records drafting help from GPT and summarization help from Gemini.

GenAI was most useful when we were narrowing the project from a broad idea into a more focused question. Instead of treating pathfinding only as a general coding problem, we shaped the project into a comparison of admissible heuristics on the same weighted 4-direction grid. This made the project more open-ended and more suitable for algorithmic analysis, because the final deliverable was not just a single path output but an environment for comparing search behavior and metrics.

A conservative description for the final submission is:

> We used GenAI primarily as a planning and writing assistant. It helped refine our project framing, clarify our experimental goals, improve pseudocode structure, and improve how we explained the methodology and deliverables. The final implementation, algorithm behavior, and project-specific deliverables were still based on our own code and analysis.

This report should be paired with the reconstructed GenAI appendix prepared for the submission set. That appendix is described as reconstructed from team recollection rather than presented as a raw exported chat log.

### How Our Solution Differs from Direct GenAI Solutions

This project is not simply a direct GenAI answer to a pathfinding question. A direct GenAI response could explain A* in words or produce a one-time solution for a single input, but our project builds a reusable interactive environment for comparing multiple search strategies on the same weighted grid. The user can create inputs, observe step-by-step frontier changes in the web interface, and collect quantitative metrics such as path cost and nodes expanded.

The project is also built around a specific course goal: understanding heuristic behavior through direct comparison. Instead of asking an AI system to return a path, we created a system that shows the search process itself. This makes the project different from a generic AI-generated answer because its value is in the comparison environment, the visualization, and the algorithmic analysis.

We do **not** claim a formal survey of all existing online pathfinding tools in this report. A safer and more accurate claim is that our project provides a custom interactive comparison setting designed specifically for heuristic analysis in CS 5800.

### Limitations and Future Work

The current implementation has several limitations:

- The grid size is fixed at 20x20.
- Movement is limited to four directions.
- Only three search modes are implemented in the comparison view.
- The current evidence focuses on representative logged runs rather than a large automated experiment suite.
- The report currently relies on existing logged data rather than a newly generated clean experimental dataset.
- Feature parity between the browser custom mode and the local Pygame version is not complete.

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

This project implemented an interactive A* pathfinding visualizer with puzzle-style features to study heuristic efficiency on a weighted 4-direction grid. On the weighted 4-direction grid used in this project, the tested admissible heuristics preserved optimal path cost, and Manhattan was the most efficient heuristic among the ones we evaluated. By running Dijkstra, A* Manhattan, and A* Euclidean on the same user-defined map, the system makes differences in search behavior visible instead of leaving them as theory. The current benchmark evidence answers the project’s central question by showing that different admissible heuristic functions can produce different expansion behavior and different levels of efficiency even when they still reach an optimal-cost solution.

The strongest contribution of the project is not only the final path returned by the algorithms, but the side-by-side environment for observing, comparing, and explaining their behavior. By combining a weighted-grid model, synchronized visualization, and logged metrics, the project turns a shortest-path topic from class into a concrete tool for heuristic analysis. The final result is a project-specific comparison environment rather than a one-time pathfinding answer, which is why the project still has value even when direct AI-generated solutions already exist.

### Individual Reflections

**Jiaxin Jia.** This project was valuable because it showed me how much interface design affects whether an algorithm is actually understandable to other people. I learned that building an interactive visualization is not just a cosmetic add-on; it changes how clearly a technical idea can be communicated. I think this experience will still be useful in future Northeastern courses and in any future work where I need to explain technical systems to users or teammates.

**Xiaoyuan Lu.** The most useful part of this project for me was turning shortest-path theory into a working implementation that could be tested and compared across multiple heuristics. I learned more about how admissibility, path cost, and priority-queue behavior interact in practice, especially once the algorithm is placed in a weighted environment instead of a simple textbook example. This project will be useful to me in later courses and in future software work that requires translating theory into reliable implementations.

**Xinyuan Fan.** This project helped me practice the evaluation side of algorithmic work, not just the implementation side. I learned how to think more carefully about benchmarks, logging, result interpretation, and how to present evidence in a way that is both concise and defensible. I think that skill will carry over to later coursework and to future projects where I need to justify design choices with actual data rather than only intuition.

## References

1. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics, 4*(2), 100-107.
2. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. Chapter 3: Solving Problems by Searching.
3. Python Software Foundation. (n.d.). *heapq — Heap queue algorithm*. Python 3 documentation. https://docs.python.org/3/library/heapq.html
4. Python Software Foundation. (n.d.). *csv — CSV file reading and writing*. Python 3 documentation. https://docs.python.org/3/library/csv.html
5. Python Software Foundation. (n.d.). *hashlib — Secure hashes and message digests*. Python 3 documentation. https://docs.python.org/3/library/hashlib.html
6. pygame community. (n.d.). *pygame documentation*. https://www.pygame.org/docs/
7. MDN Web Docs. (n.d.). *Performance.now()* https://developer.mozilla.org/en-US/docs/Web/API/Performance/now

## Appendix A — Submitted Source Code Map

For the submitted ZIP file, the most relevant source files are:

- `index.html`: root browser entry point used by the GitHub Pages version
- `game.html`: legacy redirect entry for the browser interface
- `src/states/customState.js`: browser-side comparison interface and JavaScript search-state visualization
- `src/utils.js`: browser-side support utilities, including the heap implementation used by the web interface
- `pygame_app/main.py`: local Pygame interface, interaction handling, rendering, and control flow
- `pygame_app/algorithms.py`: Python search generators for Dijkstra, A* Manhattan, and A* Euclidean
- `pygame_app/grid.py`: weighted grid model, terrain configuration, and preset maps
- `pygame_app/constants.py`: local layout, color, and configuration constants
- `pygame_app/logger.py`: CSV logging for local benchmark output
- `README.md`: instructions for running the browser and local versions

In the final submitted ZIP file, these files together form the relevant computer program for the project. In the final PDF export, the appendix can either include the full listing of the most important files above or include representative code listings together with this file map, depending on the instructor's preferred report length.

## Appendix B — Representative Source Code Excerpts

The full source code is submitted separately in the ZIP file. The excerpts below are included only to make the appendix more concrete by showing representative parts of the implemented program.

**Excerpt 1: generator-based search loop (`pygame_app/algorithms.py`)**

```python
while heap:
    _, _, pos = heapq.heappop(heap)

    if pos in closed:
        open_set.discard(pos)
        continue

    open_set.discard(pos)
    closed.add(pos)
    state.current = pos
    state.nodes_expanded = len(closed)
    yield state

    if pos == goal:
        state.path = _reconstruct(came_from, goal)
        state.path_cost = g[goal]
        state.done = True
        state.found = True
        yield state
        return
```

This excerpt shows the generator-based design used to support synchronized visualization. The algorithm does not only compute a final path; it yields intermediate states so the interface can render the frontier and expanded nodes step by step.

**Excerpt 2: CSV metric logging (`pygame_app/logger.py`)**

```python
with open(LOG_PATH, 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    if write_header:
        writer.writeheader()

    for name, state in zip(algo_names, states):
        if state is None:
            continue
        writer.writerow({
            'timestamp': ts,
            'algorithm': name,
            'grid_hash': ghash,
            'nodes_expanded': state.nodes_expanded,
            'path_cost': f'{state.path_cost:.4f}' if state.found else '0.0000',
            'runtime_ms': f'{state.runtime_ms:.6f}',
            'found': state.found,
        })
```

This excerpt shows how the local Pygame version records structured benchmark output for later comparison. Logging is part of the methodology because it preserves result evidence outside the live demo.

**Excerpt 3: browser-side priority queue (`src/utils.js`)**

```javascript
export class MinHeap {
    constructor() { this._h = []; }

    push(item) {
        this._h.push(item);
        this._up(this._h.length - 1);
    }

    pop() {
        if (this._h.length === 0) return undefined;
        const top = this._h[0];
        const last = this._h.pop();
        if (this._h.length > 0) { this._h[0] = last; this._down(0); }
        return top;
    }
}
```

This excerpt shows that the browser version includes its own supporting data structure for the search process rather than only mirroring the Python implementation superficially. It helps maintain the same comparison idea in the GitHub Pages-facing interface.
