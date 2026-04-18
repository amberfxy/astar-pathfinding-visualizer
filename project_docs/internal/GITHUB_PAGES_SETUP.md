# GitHub Pages Setup Notes

This note documents the repository changes that make the browser version compatible with direct GitHub Pages hosting.

## What Changed in the Code

- `index.html` is now the main browser entry point.
- `game.html` is kept as a legacy redirect to the same browser interface.
- The browser interface still loads its logic from `src/states/customState.js` using relative module paths, so it can be served from the repository root without a build step.

## Why This Works for GitHub Pages

- The published browser mode is a static HTML/CSS/JavaScript site.
- It does not require a Python backend.
- Relative imports such as `./src/states/customState.js` work when the repository root is published as the site root.

## Remaining External Step

The codebase is now GitHub Pages-ready, but the public URL still depends on repository settings.

Typical next step:

- Enable GitHub Pages for the repository root on the main branch.

Typical published URL pattern:

- `https://<username>.github.io/<repository>/`

## Suggested README / Presentation Wording

- `The browser custom mode is rooted at index.html and can be published directly through GitHub Pages as a static site.`
- `The local Pygame version remains useful for CSV logging and validation runs.`
