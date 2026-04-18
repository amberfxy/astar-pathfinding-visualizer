# CS5800 Final Presentation Outline

## Target length

- 15 minutes total presentation time

## Slide 1 - Title and Question

- Project title: `Interactive A* Pathfinding Puzzle Game`
- Team members
- Central question:
  - How do different admissible heuristics affect A* efficiency while preserving optimality on a weighted 4-direction grid?

## Slide 2 - Why This Problem Matters

- Students often understand shortest-path algorithms in theory before they understand their search behavior in practice.
- A* is a useful case because heuristic choice changes efficiency even when optimality is preserved.
- Our goal was to make those differences visible and measurable.

## Slide 3 - Problem Setup

- 20x20 weighted grid
- Inputs:
  - terrain configuration
  - start and goal positions
  - preset map choice
  - optional user-predicted path
- Terrain types:
  - empty = 1
  - grass = 2
  - swamp = 5
  - wall = blocked
- Same grid, same start, same goal for all three algorithms
- Output metrics:
  - nodes expanded
  - path cost
  - path length
  - runtime
  - found / not found

## Slide 4 - Methodology

- Compare:
  - Dijkstra
  - A* Manhattan
  - A* Euclidean
- Use a generator-based search implementation
- Yield state after each node expansion
- Visualize open set, closed set, current node, and final path side by side

## Slide 5 - System Demo / Interface

- Show the poster screenshot or a live demo
- Explain:
  - browser-facing custom mode launched from `index.html`
  - GitHub Pages can serve this root browser entry directly
  - local Pygame version launched from `python3 -m pygame_app`
  - terrain painting
  - moving start and goal
  - preset maps
  - run / pause / step
  - `f(n)` overlay
  - on-screen comparison metrics
  - note that CSV logging belongs to the local Pygame version and is written to `project_data/metrics_log.csv`

## Slide 6 - Results

- Use the poster benchmark, which matches the current barrier preset:
  - Dijkstra = 368 expanded nodes
  - A* Manhattan = 183 expanded nodes
  - A* Euclidean = 233 expanded nodes
  - same path cost = 25.0
- Key interpretation:
  - both admissible heuristics preserved optimal-cost results
  - Manhattan expanded fewer nodes than Euclidean in this sample
  - both expanded fewer nodes than Dijkstra

## Slide 7 - Additional Testing and What We Verified

- Barrier map: tests forced detours
- No-path case: tests correct termination with `found = False`
- Weighted terrain: tests whether algorithms account for traversal cost correctly
- Testing method:
  - we run all three algorithms on identical grids and compare path cost, nodes expanded, and termination behavior
- Important note:
  - for a weighted grid, `path cost` is the primary correctness metric

## Slide 8 - GenAI Use and Difference from Direct AI Solutions

- GenAI helped with planning and presentation/writing support
- It was used to refine framing, pseudocode structure, and explanation
- The final project is not just an AI-generated answer
- Our contribution is the implemented interactive comparison environment, including the browser-based visualization

## Slide 9 - Limitations and Future Work

- Fixed 20x20 grid
- 4-direction movement only
- Limited to three algorithms in the comparison
- No full large-scale automated experiment pipeline in the current submission
- Future work:
  - batch experiments
  - more heuristics
  - richer plots
  - additional game modes

## Slide 10 - Closing

- Restate the main answer:
  - heuristic choice changes search efficiency
  - admissible heuristics can reduce exploration while preserving optimal-cost solutions
- End with one sentence about what the visualizer contributes:
  - it turns A* from an abstract algorithm into a directly observable comparison tool

## Speaker Notes

- Do not turn the presentation into a code walkthrough.
- Mention that the submitted materials include both source code and standalone pseudocode.
- When discussing correctness, emphasize `path cost` over `path length`.
- If you mention the benchmark source, describe it as the `poster benchmark` or the `barrier preset benchmark`.
- If you mention repository structure, note that the current GitHub version contains both a browser custom mode and a local Pygame version.
- Avoid unsupported claims such as user-study evidence or a full survey of existing tools unless you can show them.
