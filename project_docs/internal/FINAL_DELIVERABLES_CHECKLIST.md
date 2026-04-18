# Final Deliverables Checklist

This checklist is based on the current GitHub version of the repository.

## Directly Usable

- `Code`
  - local Pygame version in `main.py`
  - browser custom mode in `index.html` and `src/`
- `Report draft`
  - `project_docs/final/FINAL_REPORT_DRAFT.md`
- `Pseudocode`
  - `project_docs/final/PSEUDOCODE.md`
- `Presentation outline`
  - `project_docs/final/PRESENTATION_OUTLINE.md`
- `GenAI appendix (reconstructed)`
  - `project_docs/final/GENAI_APPENDIX_RECONSTRUCTED.md`
- `GitHub Pages-ready browser entry`
  - `index.html` can serve as the repository root entry for static deployment

## Still Missing or External

- Final exported report PDF
- Final slide deck file for submission
- Any official GenAI screenshots, if the team can still recover them
- The final public GitHub Pages URL after Pages is enabled in repository settings

## Code Notes

- The current GitHub repo contains both:
  - a local Pygame implementation
  - a browser-facing custom mode
- The local Pygame version is the one tied to:
  - `metrics_log.csv`
  - the 5-wall mechanic
  - CSV-based benchmark evidence
- The browser custom mode is the cleaner demo surface for a browser presentation and is now compatible with a direct GitHub Pages root entry

## Writing Notes

- Do not refer to `build/web` unless the team reintroduces that deployment path.
- Do not say the browser custom mode writes to `metrics_log.csv`.
- Do not say `game.html` is the main published entry; use `index.html` for deployment-facing wording.
- Do not claim complete feature parity between both interfaces.
- When using benchmark numbers, call them:
  - `the poster benchmark`, or
  - `the barrier preset benchmark`

## Suggested Submission Set

- Source code:
  - `main.py`, `algorithms.py`, `grid.py`, `constants.py`, `logger.py`, `index.html`, `game.html`, `src/`
- Report:
  - exported from `project_docs/final/FINAL_REPORT_DRAFT.md`
- Pseudocode:
  - exported from `project_docs/final/PSEUDOCODE.md`
- Presentation:
  - based on `project_docs/final/PRESENTATION_OUTLINE.md`
- GenAI appendix:
  - `project_docs/final/GENAI_APPENDIX_RECONSTRUCTED.md`
