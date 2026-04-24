# Contributing to IDev4life

Default contributing guide for the **IDev4life** organization. It applies to every
repo that does not provide its own `CONTRIBUTING.md`.

## Ground rules

- Open an issue before starting non-trivial work so direction can be aligned.
- One logical change per PR. Keep diffs small and reviewable.
- No force-push to `main` / default branches. Use feature branches + PRs.
- All PRs require review from a code owner (see each repo's `CODEOWNERS`).
- Do not commit secrets, credentials, or customer data.

## Branching & commits

- Feature branches: `feat/<short-topic>`, fixes: `fix/<short-topic>`,
  chores: `chore/<short-topic>`.
- Commit messages follow Conventional Commits when practical
  (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `refactor:`, `test:`).
- Keep commits self-contained; avoid "WIP" in merged history.

## Pull requests

1. Fork or branch, make your change, push.
2. Fill in the PR template (checklist + testing notes).
3. Ensure CI is green — including lint, tests, and any self-CI the repo ships.
4. Request review from the relevant code owner(s).
5. Squash-merge unless the repo's maintainers state otherwise.

## Local checks (this repo)

This repository ships a self-CI workflow (`.github/workflows/self-ci.yml`).
You can run the same checks locally before pushing:

```sh
# actionlint — workflow linting
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.12 -color

# ruff — python linting for scripts/
python -m pip install --user ruff==0.15.11
ruff check scripts/
python -m compileall -q scripts/

# markdownlint
npx --yes markdownlint-cli2@0.22.1 --config config/markdownlint.jsonc "**/*.md"
```

## Reporting security issues

Do **not** open a public issue for vulnerabilities. Follow [SECURITY.md](SECURITY.md).

## Code of conduct

Be respectful. Harassment or abusive behavior will result in removal from the
organization. Report incidents privately to the maintainers listed in
`CODEOWNERS`.
