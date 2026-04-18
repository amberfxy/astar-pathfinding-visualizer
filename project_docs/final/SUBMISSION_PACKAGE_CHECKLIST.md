# CS5800 Final Submission Package Checklist

This note is the practical packaging guide for the final Canvas upload. It focuses on **what to upload**, **how to name it**, and **what should go into the source-code ZIP**.

## Core Deliverables

Based on the current assignment wording, the safest submission set is:

1. `Project Report-jia-lu-fan-SP26.pdf`
2. `Interactive-A-Pathfinding-Puzzle-Game.pptx`
3. `PSEUDOCODE.pdf`
4. `source_code.zip`
5. `README.md`

If Canvas accepts only **one** upload for the group, create one wrapper archive such as:

- `CS5800-Final-Submission.zip`

and place the five files above inside it.

## Report PDF

Use the final exported PDF version of:

- `project_docs/final/FINAL_REPORT_DRAFT.md`

Before export, make sure the PDF includes:

- title and team members
- abstract
- introduction and central question
- methodology and implementation
- inputs and outputs
- pseudocode
- testing and results
- GenAI use
- how the solution differs from direct AI / online solutions
- limitations and future work
- collaboration
- conclusion
- one reflection paragraph per team member
- references
- appendix with the source-code map

## Presentation File

Submit the final PowerPoint file:

- `Interactive-A-Pathfinding-Puzzle-Game.pptx`

The presentation script in the repository is optional support material, not a required submission file:

- `project_docs/final/PRESENTATION_SCRIPT.md`

## Pseudocode File

The repository draft lives at:

- `project_docs/final/PSEUDOCODE.md`

For submission, export it or copy it into a cleaner standalone file such as:

- `PSEUDOCODE.pdf`

Submitting pseudocode both as a standalone file and as part of the report appendix is the safest approach.

## README

Use the repository root README:

- `README.md`

It should explain:

- browser / GitHub Pages run instructions
- local Pygame run instructions
- dependencies
- where the main source files live

## Source Code ZIP

Create:

- `source_code.zip`

Recommended contents:

- `index.html`
- `game.html`
- `src/`
- `pygame_app/`
- `requirements.txt`
- `README.md`
- `LICENSE`

Optional to include:

- `project_data/`

Only include `project_data/` if you want to preserve a sample metrics log as part of the submission. It is **not** required for the code to run.

## Files to Exclude from source_code.zip

Do **not** include:

- `.git/`
- `.claude/`
- `.idea/`
- `__pycache__/`
- `venv/`
- OS-generated files such as `.DS_Store`
- internal prep notes under `project_docs/internal/`
- archive notes that are not part of the final deliverables

You usually also do **not** need to include:

- `project_docs/internal/`
- `project_docs/archive/`
- `project_docs/final/PRESENTATION_SCRIPT.md`

unless the instructor specifically asks for all writing artifacts.

## Recommended Final File Set

If Canvas allows multiple files, upload:

- `Project Report-jia-lu-fan-SP26.pdf`
- `Interactive-A-Pathfinding-Puzzle-Game.pptx`
- `PSEUDOCODE.pdf`
- `source_code.zip`
- `README.md`

If Canvas allows only one file, upload:

- `CS5800-Final-Submission.zip`

with these inside:

- `Project Report-jia-lu-fan-SP26.pdf`
- `Interactive-A-Pathfinding-Puzzle-Game.pptx`
- `PSEUDOCODE.pdf`
- `source_code.zip`
- `README.md`

## Final Pre-Upload Check

Before uploading, verify:

- the report PDF matches the final PPT wording
- the PPT benchmark numbers still read `368 / 183 / 233 / 25.0`
- the README run commands are correct
- `python3 -m pygame_app` still launches locally
- the GitHub Pages URL opens the browser version
- the ZIP opens cleanly and does not contain local junk folders
