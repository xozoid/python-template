# Contributing

## Environment and dependencies

Install Git, Python 3.12 or later, `uv`, Node.js 24 or later with npm, and Vale. Run
`tools/env.sh` from any directory in the repository to sync the locked Python
dependencies, install `prek` Git hooks, fetch Vale styles, run `npm ci`, and create
`.env` and `.env.leave` if they aren't present. The script installs Vale when needed
through a supported package manager. Use `tools/env.sh --upgrade` to upgrade Python
dependencies before setup.

Add Python development dependencies to the appropriate group in `pyproject.toml`
(`lint`, `spell`, `test`, `coverage`, `types`, `format`, `prek`, or the aggregate `dev`
group), then update and commit `uv.lock`:

```sh
uv add --dev package-name
uv lock
uv sync --locked --all-groups
```

Use `uv add --group <group> package-name` for another dependency group, or edit the
project metadata and run `uv lock` when needed. The `dev` group includes all groups for
the complete local environment. The `format` group includes `prek` for its `yamlfmt`
hook; CI selects only the groups each independent job needs. Update npm development
dependencies with `npm install --save-dev package-name` and commit both `package.json`
and `package-lock.json`. Dependabot also checks uv, npm, and GitHub Actions dependencies
weekly.

## Tests and checks

Run tests and coverage from the repository root:

```sh
uv run pytest
uv run coverage run -m pytest
uv run coverage report
```

The coverage report enforces the configured 85% minimum. `tools/linters.sh` runs Ruff,
`basedpyright`, `codespell`, and Vale (errors only). `tools/formatters.sh` runs Ruff
format, Prettier, `Taplo`, and `yamlfmt`. These scripts apply formatting changes; review
the resulting diff.

`uv run prek run --all-files` runs the configured hooks against all files. The hooks
include Ruff lint and format, `codespell`, `Taplo`, `basedpyright`, `yamlfmt`, standard
file checks, Vale, and Prettier. `tools/env.sh` installs the Git hooks so `prek` runs on
commits. The `sync-with-uv` hook keeps hook revisions aligned with Python packages in
`uv.lock`; run it after changing hook revisions or relevant dependencies, then review
and commit the lockfile changes.

CI runs `sync-with-uv` on every pull request, including Dependabot pull requests. The
check installs the `prek` dependency group from `uv.lock`, runs the hook, and fails if
it modifies tracked files. Dependabot doesn't provide a native arbitrary post-update
script in `dependabot.yml`; its supported configuration covers dependency update
behavior
([options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)).
When a Dependabot update changes a synchronized package version, run
`uv run prek run --all-files sync-with-uv` locally and commit the resulting `prek.toml`
change with the lockfile update. CI validates every pull request, including Dependabot
pull requests.

## Agent instructions and skills

Persistent repository guidance lives in the root `AGENTS.md`. Focused, task-specific
Agent Skills live under `.agents/skills/`; each skill has a `SKILL.md` with metadata
that helps compatible agents discover when to use it. `AGENTS.md` describes project-wide
expectations, while skills provide checklists for particular tasks. Contributors can
extend or maintain skills by adding a narrowly scoped directory and a valid `SKILL.md`,
then updating its instructions when project workflows change. See the
[Agent Skills specification](https://agentskills.io/specification) for the format.

## Pull requests and CI

Open a pull request against `main`. CI keeps checks in separate jobs: pytest on Python
3.12 through 3.15, Ruff, `basedpyright`, formatting (Ruff, Prettier, `Taplo`,
`yamlfmt`), spelling, Vale, coverage, and build/import validation. Run the relevant
local commands and ensure CI passes. Update tests and documentation when behavior or
contributor instructions change.

## Releases

`hatch-vcs` reads the package version from Git tags. Create and publish a GitHub Release
with a version tag such as `1.2.3` or `v1.2.3`; the optional `v` is removed for
comparison with the package version. The published-release event starts
`.github/workflows/publish.yml`. It runs CI first, builds the distribution, verifies
that the release tag matches the built version, then publishes to PyPI through trusted
publishing.

Before releasing, ensure the tag resolves to the intended source commit, the matching
PyPI project exists, and trusted publishing is configured for this repository's `pypi`
GitHub environment. A tag that doesn't match the package version fails validation and
isn't published.
