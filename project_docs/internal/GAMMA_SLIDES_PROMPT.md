# Gamma Slides Prompt

Use this prompt with the current repository state in mind.

```text
Create a clean, academic slide deck in English for a 15-minute CS5800 final project presentation.

Audience: a university algorithms instructor and classmates.
Tone: rigorous, concise, evidence-based, and presentation-ready.
Important: do not invent any facts, experiments, user studies, tools, or deployment claims beyond what is listed below.

Project title:
Interactive A* Pathfinding Puzzle Game

Team members:
Jiaxin Jia, Xiaoyuan Lu, Xinyuan Fan

Central question:
How do different admissible heuristics affect A* search efficiency on a weighted 4-direction grid while preserving optimality?

Current repository structure:
- local Pygame implementation: `main.py`
- browser custom mode: `index.html` + `src/states/customState.js`

Project summary:
This project compares Dijkstra, A* Manhattan, and A* Euclidean on the same weighted 20x20 grid. The repository includes both a local Pygame version and a browser-facing custom mode. Users can paint terrain, move the start and goal, use preset maps, and watch the three algorithms run side by side. The browser entry is rooted at `index.html`, so it can be served directly by GitHub Pages as a static site.

Terrain costs:
- empty = 1
- grass = 2
- swamp = 5
- wall = blocked

Benchmark data to use:
- barrier preset benchmark
- Dijkstra: 368 nodes expanded
- A* Manhattan: 183 nodes expanded
- A* Euclidean: 233 nodes expanded
- all three had path cost 25.0
- all three had path length 26

Important benchmark note:
- do not call this benchmark random seed 42
- call it the poster benchmark or the barrier preset benchmark

Testing evidence:
- barrier detour case
- no-path case
- weighted-grid correctness checks
- fresh Python reruns confirmed the benchmark values
- inputs: terrain configuration, start/goal positions, preset choice, optional predicted path
- outputs: nodes expanded, path cost, path length, found/not found, runtime, and the visual search trace

Important wording:
- path cost is the primary correctness metric
- do not claim the algorithms always find the exact same path in every case
- do not claim a full automated experiment pipeline

Interface wording:
- the current repository includes both a local Pygame version and a browser-facing custom mode
- the browser-facing custom mode is launched from `index.html`
- do not say the browser mode writes to metrics_log.csv
- if mentioning logging, say the local Pygame version appends CSV metrics

GenAI wording:
- GenAI was used mainly for planning, framing, pseudocode/report organization, and writing support
- use cautious wording: reconstructed appendix based on team recollection

Slide constraints:
- 9 to 10 slides total
- no code screenshots
- no dense paragraphs
- one clear benchmark chart
- one concise slide on methodology
- one concise slide on limitations and future work

Recommended slide structure:
1. Title and question
2. What is A*?
3. Why heuristic choice matters
4. Problem setup
5. Methodology
6. System interface / demo overview
7. Benchmark results and testing
8. GenAI use and project contribution
9. Limitations and future work
10. Conclusion
```
