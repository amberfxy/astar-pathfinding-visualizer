# Project Docs

This folder keeps team-facing writing and submission-prep material out of the repo root.

We intentionally use `project_docs/` instead of `docs/` so the submission documents stay separate from the browser-facing static files. The current GitHub Pages-ready browser entry lives at the repository root in `index.html`.

The current GitHub version of the repository includes both:

- the original local Pygame comparison tool in `main.py`
- a browser-facing custom mode in `index.html` and `src/`

The browser entry is now rooted at `index.html` so the repository can be published directly through GitHub Pages without introducing a separate static-site copy of the web files.

## final

Files in `project_docs/final/` are the polished deliverable drafts that are most likely to matter for submission:

- `FINAL_REPORT_DRAFT.md`
- `PSEUDOCODE.md`
- `PRESENTATION_OUTLINE.md`
- `GENAI_APPENDIX_RECONSTRUCTED.md`

## internal

Files in `project_docs/internal/` are working notes and audit artifacts used during submission prep.

They are useful for coordination, consistency checks, and deployment planning, but they are not the core project deliverables by themselves.

Current internal notes:

- `CONSISTENCY_AUDIT.md`
- `FINAL_DELIVERABLES_CHECKLIST.md`
- `HEADLESS_VALIDATION_RESULTS.md`
- `GAMMA_SLIDES_PROMPT.md`
- `GENAI_APPENDIX_TEMPLATE.md`
- `GITHUB_PAGES_SETUP.md`
