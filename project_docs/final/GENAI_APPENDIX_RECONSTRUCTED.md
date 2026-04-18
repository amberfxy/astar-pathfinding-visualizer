# Reconstructed GenAI Use Appendix

## Reconstructed GenAI Use Appendix — CS 5800 Project

**CS 5800 Project — Interactive A* Pathfinding Puzzle Game**  
**Team Members:**  
Jiaxin Jia · Xiaoyuan Lu · Xinyuan Fan

## Important Note

This appendix is a reconstructed summary based on team recollection and surviving project materials. It is not a verbatim export of a single chat history and should not be described as one. The team used multiple GenAI tools across different devices and apps, so the original raw prompt record was not preserved in one place. To keep the submission honest, the entries below are written as representative reconstructed prompts and usage notes.

## Short Report Statement

Use the following wording in the report if needed:

> We used GenAI mainly as a planning and writing support tool rather than as a substitute for the final implementation. Because the team used multiple GenAI tools across different devices and did not preserve one unified exported prompt log, the appendix includes a reconstructed summary of representative prompts based on team recollection and the surviving project materials. The final implementation, visualization, and project-specific analysis were still based on our own code, poster, and report writing.

## Reconstructed Prompt Record

### Prompt 1: Narrowing the Project Topic

1. **Goal:** Refine a broad pathfinding idea into a topic that is more specific, algorithmic, and suitable for CS 5800.
2. **Reconstructed prompt:**  
   We want to do a final project related to A* pathfinding. Help us narrow the topic into something more specific and analytical, not just a generic game or coding demo. We want it to connect to algorithms, heuristics, and measurable performance.
3. **How the response helped:** It helped shift the project away from a generic pathfinding demo and toward a focused comparison of admissible heuristics on the same weighted grid.
4. **What we kept or changed ourselves:** We kept the idea of comparing heuristic efficiency while preserving correctness. We fixed the environment to a weighted 4-direction grid ourselves and selected Dijkstra, A* Manhattan, and A* Euclidean as the concrete comparison modes. Generic game ideas or feature lists that were not aligned with the final implementation were not used.

### Prompt 2: Refining Methodology and Evaluation

1. **Goal:** Clarify what metrics and comparison setup would make the project analytically meaningful.
2. **Reconstructed prompt:**  
   For an interactive A* visualizer, what are good ways to compare heuristics in a rigorous way? We want metrics and experiment ideas that are simple enough for a class project but still meaningful.
3. **How the response helped:** It highlighted metrics such as nodes expanded, runtime, and path cost, and suggested running all algorithms on the same grid for fair comparison.
4. **What we kept or changed ourselves:** We kept the same-input principle and the idea of logging quantitative metrics. We decided ourselves that path cost would be the main correctness metric on a weighted grid, and we scoped the evidence to representative scenarios plus CSV logging rather than claiming a full large-scale experiment pipeline.

### Prompt 3: Structuring Pseudocode and Report Writing

1. **Goal:** Improve how the project is explained in the final deliverables.
2. **Reconstructed prompt:**  
   Help us organize pseudocode and a final report for an A* visualizer project. We need to explain the algorithm clearly, describe the methodology, and avoid turning the report into just a code walkthrough.
3. **How the response helped:** It helped us organize the report around problem setup, methodology, results, and limitations, and suggested presenting pseudocode at the algorithm level rather than copying source code.
4. **What we kept or changed ourselves:** We kept the high-level structure and the algorithm-level pseudocode style. The actual wording was rewritten against our own implementation, poster, and metrics log so that the report matched what the system actually does instead of using boilerplate text.

### Prompt 4: Generator-Based Search Framework

1. **Goal:** Decide how to structure the search so that intermediate states could be visualized, not just the final path.
2. **Reconstructed prompt:**  
   We want a visualizer that shows the A* frontier step by step. Should the search function just return the final path, or is there a cleaner way to expose the intermediate state after each node expansion without coupling the algorithm to the renderer?
3. **How the response helped:** It suggested a generator-based design in which the search yields a state snapshot after each expansion, keeping the algorithm and the renderer loosely coupled.
4. **What we kept or changed ourselves:** We adopted the generator structure and kept the snapshot model (closed set, open set, current node, f, g). The exact snapshot contents, the closed-set check before yielding, and how Dijkstra is unified as A* with h(n)=0 were decided and implemented by us based on the needs of the three-panel comparison.

### Prompt 5: Three-Panel Synchronized Rendering in Pygame

1. **Goal:** Work out how to run three algorithms side by side and keep their visual frames in step.
2. **Reconstructed prompt:**  
   In Pygame, what is a reasonable way to render three panels that each show a different search algorithm on the same grid, and advance them together one step at a time? We want the user to be able to pause and step through as well.
3. **How the response helped:** It outlined a pattern where each panel holds its own generator and the main loop advances all three per frame, with event handling driving run, pause, and step controls.
4. **What we kept or changed ourselves:** We kept the one-generator-per-panel pattern and the per-frame advance idea. Layout, panel sizing, the button-driven control scheme, and the f(n) overlay toggle were designed and written ourselves to fit the actual interface.

### Prompt 6: Browser MinHeap and customState Structure

1. **Goal:** Translate the Python search structure into the browser while keeping the same comparison idea.
2. **Reconstructed prompt:**  
   We are porting the three-panel comparison to a static browser page. JavaScript does not have heapq. What is the minimum priority-queue implementation we need, and how should a state object be organized so that the same search loop can be driven by render frames in the browser?
3. **How the response helped:** It suggested a small MinHeap class with push, pop, and sift-up/down helpers, and recommended keeping search state (heap, closed, g, f, came_from) in one object that the UI can advance per tick.
4. **What we kept or changed ourselves:** We kept the minimal MinHeap shape in src/utils.js and the single-state-object pattern in customState.js. The actual comparison panels, DOM structure, canvas rendering, and how metrics are displayed on screen were written and tuned by us.

### Prompt 7: CSV Logging Schema

1. **Goal:** Decide what to log per run so that benchmark results could be compared reliably after the demo.
2. **Reconstructed prompt:**  
   We want to log each algorithm run to a CSV file. What fields are worth including so that runs on the same map are comparable later, and is there a lightweight way to tie a log row back to the exact grid that was tested?
3. **How the response helped:** It suggested including timestamp, algorithm name, nodes expanded, path cost, runtime, and a found flag, and recommended hashing the grid state to pin each row to its input.
4. **What we kept or changed ourselves:** We kept this field list and the idea of a grid fingerprint. We chose hashlib.sha256 over the input grid bytes ourselves, set the exact FIELDNAMES and numeric formatting (path_cost at 4 decimals, runtime_ms at 6), and used csv.DictWriter with a header-on-first-write pattern so the log stays append-only across sessions.

### Prompt 8: Designing the No-Path and Edge-Case Tests

1. **Goal:** Make sure the implementation behaves correctly when no solution exists or the input is degenerate.
2. **Reconstructed prompt:**  
   What edge cases should an A* and Dijkstra implementation be tested against besides a normal reachable case? We specifically want to be sure that an unreachable goal terminates cleanly and does not silently return a wrong path.
3. **How the response helped:** It listed cases such as goal fully walled off, start equals goal, empty grid, and start or goal inside an obstacle, and emphasized checking the termination condition when the open set empties.
4. **What we kept or changed ourselves:** We kept the no-path case and the empty-grid baseline, and added the barrier preset and a seeded random map ourselves because they were the scenarios most relevant to the heuristic comparison. We verified the found = False behavior on our own grids rather than using any suggested template.

### Prompt 9: Explaining Why Manhattan Beats Euclidean on This Grid

1. **Goal:** Interpret the observed result that A* Manhattan expanded fewer nodes than A* Euclidean on the barrier preset.
2. **Reconstructed prompt:**  
   On a 4-direction weighted grid, both Manhattan and Euclidean distance are admissible, but our runs show Manhattan expanding fewer nodes than Euclidean. Is this expected, and what is the intuition we should use when explaining it in the report?
3. **How the response helped:** It explained that on a 4-direction grid with unit-ish orthogonal moves, Manhattan matches the grid's geometry more tightly and therefore gives a heuristic value closer to the true remaining cost, while Euclidean consistently under-estimates, leading A* to expand more nodes to prove optimality.
4. **What we kept or changed ourselves:** We kept the "closer-to-true-cost" intuition and used it in the report. The concrete numbers (368 / 183 / 233 expansions with common path cost 25.0) come from our own runs, and we were careful in the report to frame this as a representative benchmark rather than a universal claim about the two heuristics.

## How GenAI Helped Make the Topic More Open-Ended

Our initial topic was closer to a broad pathfinding or game-demo idea. Through iterative prompting, we refined it into a more specific question about how admissible heuristics affect A* efficiency on the same weighted 4-direction grid. This made the project more open-ended and more appropriate for algorithmic analysis, because the final work was no longer just “implement A*,” but “design a comparison environment, choose meaningful metrics, and interpret heuristic behavior under the same input conditions.” The final contribution therefore required implementation, visualization design, metric logging, and project-specific analysis beyond what a direct AI answer would provide.
