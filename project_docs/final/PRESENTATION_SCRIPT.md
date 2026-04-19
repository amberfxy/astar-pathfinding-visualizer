# CS5800 Presentation Script

This script is written as a more natural, student-style speaking version of the presentation. It is intended for practice, not for word-for-word memorization.

## Timing and Division

- `Jiaxin Jia` — Slides 1 to 4, about 4.5 minutes
- `Xiaoyuan Lu` — Slides 5 to 6, about 4.5 minutes
- `Xinyuan Fan` — Slides 7 to 11, about 5.5 minutes

## Jiaxin Jia

### Slide 1 — Title

“Hi everyone, we’re Group 4, and our project is called *Interactive A* Pathfinding Puzzle Game*.

The main question we wanted to study is: how do different admissible heuristics affect A* search efficiency on a weighted four-direction grid, while still preserving optimality?

Our team members are Jiaxin Jia, Xiaoyuan Lu, and Xinyuan Fan. In this talk, we’ll first introduce the problem and the algorithm background, then explain our comparison setup, and finally show the results, testing, and conclusions.”

### Slide 2 — What Is A* Search?

“Before getting into our comparison, I want to briefly explain what A* is.

A* is a shortest-path algorithm that chooses which node to explore next by combining two kinds of information.

The first is `g(n)`, which is the actual cost from the start to the current node.

The second is `h(n)`, which is the heuristic, meaning an estimate of the remaining cost to the goal.

Then A* adds them together as `f(n) = g(n) + h(n)`, and uses that value to guide the search.

A useful reference point is that Dijkstra’s algorithm is basically the special case where the heuristic is zero, so it stays optimal but doesn’t get any goal-directed guidance.

As a concrete example, imagine we’re standing at a node three cells away from the goal. `g(n)` might be 7, meaning we’ve already paid 7 units of cost to get here. `h(n)` would be our estimate for the remaining 3 cells. A* always picks the node with the smallest `f(n)` to expand next, which is what gives it goal-directed behavior that Dijkstra lacks.”

### Slide 3 — Why Heuristic Choice Matters

“So why does the heuristic matter?

Dijkstra is optimal, but it explores pretty broadly in all directions. A* is usually more efficient, but that depends a lot on the heuristic you choose.

That leads to the main questions behind our project.

Do admissible heuristics still preserve optimality on a weighted grid?

Which heuristic expands fewer nodes on the same input?

And can we make those differences visible in a way that people can actually observe, instead of only reading about them in pseudocode?

Being able to *see* that difference, not just read about it, is really what motivated us to build an interactive visualizer instead of just writing a report.”

### Slide 4 — Problem Setup

“To study that, we used a controlled weighted-grid setup.

All three algorithms run on the exact same 20-by-20 grid, with four-direction movement only.

The terrain costs are fixed: empty cells cost 1, grass costs 2, swamp costs 5, and walls are blocked.

Because this is a weighted grid, path cost is the main correctness metric. Step count is still useful, but it’s secondary.

The inputs to the system include the terrain layout, the start and goal positions, the preset map choice, and an optional predicted path from the user.

The outputs include nodes expanded, path cost, path length, runtime, whether a path was found, and of course the visual search trace itself.”

### Handoff

“Now that we’ve introduced the problem setup, Xiaoyuan will explain the methodology and the system itself.”

## Xiaoyuan Lu

### Slide 5 — Methodology

“Our methodology compares three algorithms on the same weighted grid.

The first is Dijkstra, which we use as the uninformed baseline.

The second is A* with Manhattan distance.

And the third is A* with Euclidean distance.

Under our current four-direction weighted-grid model, both Manhattan and Euclidean are admissible, so they should still preserve optimal path cost.

What we really want to compare is efficiency, especially how many nodes they expand before reaching the solution.

Implementation-wise, our search is generator-based, which means each algorithm yields its state after every node expansion.

That lets us visualize the open set, the closed set, the current node, and the final path step by step, side by side.”

### Slide 6 — System Interface & Demo Overview

“The project currently has two interfaces for the same comparison task.

The browser version is an HTML and JavaScript interface that we publish through GitHub Pages.

The local version is a Pygame interface that we use for local execution and CSV-based validation.

Across both versions, users can paint weighted terrain and walls, move the start and goal, choose preset maps like maze, barrier, and random, and run all three algorithms side by side with run, pause, and step controls.

Users can also turn on `f(n)` overlays to inspect the search state more closely.

The local Pygame version includes a few extra features, like CSV logging, a wall-limited gameplay mode, and more detailed prediction feedback.

So overall, the project is not just computing one path. It’s giving users a full environment for comparing search behavior interactively.”

### Handoff

“With the method and system in place, Xinyuan will now go over the benchmark results, testing, and final conclusions.”

## Xinyuan Fan

### Slide 7 — Benchmark Results

“Our main benchmark is the barrier preset, which is also the benchmark shown on the poster.

On this map, all three algorithms reached the same optimal path cost of 25.0.

At the same time, their search effort was very different.

Dijkstra expanded 368 nodes, A* Manhattan expanded 183 nodes, and A* Euclidean expanded 233 nodes.

So compared with Dijkstra, Manhattan reduced node expansion by 50 percent, and Euclidean reduced it by 37 percent.

You might wonder why Manhattan beats Euclidean here, given that both are admissible. The reason is pretty intuitive once you think about movement. On a four-direction grid, you can only step along the axes, so the true remaining cost is always at least the Manhattan distance. Euclidean is the straight-line estimate, which is always smaller than or equal to Manhattan — so it’s a *looser* lower bound. A looser heuristic gives weaker guidance, and the search starts looking more like Dijkstra. Manhattan is tighter, so it prunes more aggressively. That theoretical story is exactly what the numbers show: 183 expansions versus 233.

This is the clearest answer to our main question: admissible heuristics preserved optimal path cost, but the choice of heuristic clearly changed efficiency.”

### Slide 8 — Additional Testing Scenarios

“We also tested several other scenarios besides the main benchmark.

On an empty grid, we checked baseline behavior without obstacles.

On the barrier map, we tested whether the algorithms could handle a forced detour.

And in the no-path case, we surrounded the goal and confirmed that all algorithms correctly terminated with `found = false`.

More generally, we tested all three algorithms on identical grids under open-grid, barrier, no-path, and weighted-terrain conditions, and then compared path cost, nodes expanded, and termination behavior.

For weighted grids, path cost is the most important correctness metric.”

### Slide 9 — GenAI Use & Project Contribution

“We also want to be clear about how GenAI was used.

GenAI mainly helped with planning, framing the problem, organizing pseudocode, and improving report and presentation wording.

It was not used as a substitute for the final implementation.

What makes the project original is that a direct AI answer would normally just return one path or one explanation.

Our project instead provides an interactive comparison environment, side-by-side visualization, and project-specific benchmark analysis on user-controlled maps.”

### Slide 10 — Limitations & Future Work

“There are a few clear limitations in the current version.

The grid is fixed at 20 by 20, movement is limited to four directions, and the comparison only includes three algorithms.

Also, while we do have representative benchmark and testing evidence, we do not claim to have a full large-scale automated experiment pipeline in this final submission.

To be upfront: the numbers we reported come from one representative run per scenario, not an averaged sweep across many seeds. Scaling this into a proper statistical study is one of our main future directions.

For future work, we’d like to support larger and variable grid sizes, add eight-direction movement, include more heuristics, and build a more systematic benchmarking pipeline.”

### Slide 11 — Conclusion

“To conclude, on our weighted four-direction grid, admissible heuristics preserved optimal path cost, and Manhattan was the most efficient heuristic among the ones we tested.

More specifically, both A* heuristics reduced search effort compared with Dijkstra, while still reaching the same optimal-cost result in our benchmark.

Beyond the numbers, the main contribution of the project is the interactive visualizer itself. It makes heuristic behavior observable and comparable, which helps turn an abstract shortest-path topic into something much more concrete.

Thank you.”

## Short Transition Lines

- `Jiaxin → Xiaoyuan`
  - “Now that we’ve introduced the problem setup, Xiaoyuan will explain the methodology and the system itself.”

- `Xiaoyuan → Xinyuan`
  - “With the method and system in place, Xinyuan will now go over the benchmark results, testing, and final conclusions.”

## Delivery Notes

- Do not try to memorize every word exactly. Use the script as a practice guide.
- Make sure Slide 7 is numerically stable in speech: `368`, `183`, `233`, and `25.0`.
- On Slide 8, explicitly say that `path cost` is the primary correctness metric for weighted grids.
- Keep Slide 9 short and matter-of-fact.
- End Slide 11 cleanly; do not introduce new information during the final sentence.
