# Consistency Audit

This note checks the current GitHub version of the repository against the main project documents and the implemented code.

## Overall Verdict

- The project is still centered on the same algorithmic comparison:
  - Dijkstra
  - A* Manhattan
  - A* Euclidean
- The current GitHub repository now contains **two user-facing interfaces**:
  - a local Pygame version in `main.py`
  - a browser custom mode rooted at `index.html` and implemented with `src/`
- The main documentation risk is that some older wording still assumes a packaged `build/web` deployment or treats the browser mode and local Pygame mode as perfectly identical.

## What Is Consistent

- The weighted 20x20, 4-direction comparison problem is still the central project.
- Terrain costs remain:
  - `empty = 1`
  - `grass = 2`
  - `swamp = 5`
  - `wall = blocked`
- The Python implementation still supports:
  - side-by-side visualization
  - terrain painting
  - preset maps
  - on-screen metrics
  - CSV logging
- The browser custom mode still supports:
  - side-by-side visualization
  - terrain painting
  - preset maps
  - on-screen metrics
  - direct static hosting from the repository root

## Important Interface Differences

- The **local Pygame version**:
  - runs from `main.py`
  - writes `metrics_log.csv`
  - includes a 5-wall limit
  - includes predict-path cost feedback
- The **browser custom mode**:
  - runs from `index.html`
  - uses `src/states/customState.js`
  - displays metrics on screen
  - does **not** append CSV logs
  - does **not** appear to implement the 5-wall limit

## Current Wording Risks

- `README.md` previously referenced `build/web`, which is not part of the current GitHub version.
- Any document that still describes `game.html` as the main browser entry is now outdated; `game.html` is only a legacy redirect.
- Any document that says the browser version appends to `metrics_log.csv` is too strong.
- Any document that implies all local Pygame features exist unchanged in the browser custom mode is too strong.

## Benchmark Accuracy

The benchmark values used on the poster still match the current Python implementation for the `barrier` preset:

- Dijkstra: `368`
- A* Manhattan: `183`
- A* Euclidean: `233`
- Path cost: `25.0`
- Path length: `26`

These values were rechecked against the current codebase.

## Safe Wording for Current Docs

- `The current repository includes both a local Pygame version and a browser-facing custom mode.`
- `The browser-facing custom mode is rooted at index.html so it can be published directly through GitHub Pages.`
- `The local Pygame version appends CSV logs; the browser custom mode displays metrics on screen.`
- `The poster benchmark matches the current barrier preset in the Python implementation.`
- `Path cost is the primary correctness metric on the weighted grid.`

## Remaining Low-Risk Mismatches

- Some source comments still describe the project using older wording.
- These are naming mismatches, not algorithmic mismatches.
