# Reconstructed GenAI Use Appendix

## Important Note

This appendix is a **reconstructed summary** based on team recollection and surviving project materials. It is **not** a verbatim export of a single chat history and should not be described as one. The team used multiple GenAI tools across different devices and apps, so the original raw prompt record was not preserved in one place. To keep the submission honest, the entries below are written as representative reconstructed prompts and usage notes.

## Short Report Statement

Use the following wording in the report if needed:

> We used GenAI mainly as a planning and writing support tool rather than as a substitute for the final implementation. Because the team used multiple GenAI tools across different devices and did not preserve one unified exported prompt log, the appendix includes a reconstructed summary of representative prompts based on team recollection and the surviving project materials. The final implementation, visualization, and project-specific analysis were still based on our own code, poster, and report writing.

## Reconstructed Prompt Record

### Prompt 1: Narrowing the Project Topic

- `Goal:` Refine a broad pathfinding idea into a topic that is more specific, algorithmic, and suitable for CS 5800.
- `Reconstructed prompt:`  
  `We want to do a final project related to A* pathfinding. Help us narrow the topic into something more specific and analytical, not just a generic game or coding demo. We want it to connect to algorithms, heuristics, and measurable performance.`
- `How the response helped:` It helped shift the project away from a generic pathfinding demo and toward a focused comparison of admissible heuristics.
- `What we kept:` The idea of comparing heuristic efficiency while preserving correctness.
- `What we changed ourselves:` We fixed the environment to a weighted 4-direction grid and selected Dijkstra, A* Manhattan, and A* Euclidean as the concrete comparison modes.
- `What we did not directly copy:` Any generic game ideas or broad feature lists that were not aligned with the final implementation.

### Prompt 2: Refining Methodology and Evaluation

- `Goal:` Clarify what metrics and comparison setup would make the project analytically meaningful.
- `Reconstructed prompt:`  
  `For an interactive A* visualizer, what are good ways to compare heuristics in a rigorous way? We want metrics and experiment ideas that are simple enough for a class project but still meaningful.`
- `How the response helped:` It highlighted metrics such as nodes expanded, runtime, and path cost, and suggested comparing algorithms on the same grid.
- `What we kept:` Using the same input grid for all algorithms and logging quantitative metrics.
- `What we changed ourselves:` We treated path cost as the main correctness metric for a weighted grid and used the implemented CSV logging plus representative scenarios instead of claiming a full large-scale experiment pipeline.
- `What we did not directly copy:` Any suggestions requiring external datasets, advanced plotting pipelines, or features that were not implemented.

### Prompt 3: Structuring Pseudocode and Report Writing

- `Goal:` Improve how the project is explained in the final deliverables.
- `Reconstructed prompt:`  
  `Help us organize pseudocode and a final report for an A* visualizer project. We need to explain the algorithm clearly, describe the methodology, and avoid turning the report into just a code walkthrough.`
- `How the response helped:` It helped organize the report around problem, methodology, results, and limitations, and suggested presenting pseudocode at the algorithm level instead of copying source code.
- `What we kept:` The emphasis on methodology, pseudocode, and explanation of deliverables.
- `What we changed ourselves:` We based the final wording on the actual implementation, poster, and metrics log rather than using generic text directly.
- `What we did not directly copy:` Boilerplate explanations that did not match the actual system or overclaimed the evaluation.

## How GenAI Helped Make the Topic More Open-Ended

Our initial topic was closer to a broad pathfinding or game-demo idea. Through iterative prompting, we refined it into a more specific question about how admissible heuristics affect A* efficiency on the same weighted 4-direction grid. This made the project more open-ended and more appropriate for algorithmic analysis, because the final work was no longer just “implement A*,” but “design a comparison environment, choose meaningful metrics, and interpret heuristic behavior under the same input conditions.” The final contribution therefore required implementation, visualization design, metric logging, and project-specific analysis beyond what a direct AI answer would provide.

## Final Honesty Check

- Do not describe this appendix as a raw chat export.
- Do not create fake screenshots and present them as original evidence.
- If the instructor asks, describe this as a reconstructed prompt record based on team recollection.
- If any teammate can still recover real prompt screenshots, those can be added later as a stronger appendix.
