## Commit Messages
* Use this format: `type(scope): short description`
* Allowed types: `feat, fix, docs, chore, refactor, ci`

## Branching
* `main`: Protected. All work must be done in feature branches (no direct commits).
* `feature/*`: Used for new features or updates.

## Pull Requests
* Create PRs **only** from a `feature/*` branch.
* The PR title must follow the Commit Message format (e.g. `feat(ci): Add Docker build step`).
* All **CI checks (lint, test)** must pass before merging (show a "green checkmark").