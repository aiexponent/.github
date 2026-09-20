# aiexponent/.github

Org-level defaults for every repo under `aiexponent`. Two kinds of thing live here:

- **Community health files** at the root and in `.github/`: code of conduct, contributing guide, security policy, issue forms, PR template, and the org profile under `profile/`. GitHub serves these to any repo in the org that does not carry its own copy.
- **Reusable workflows** in `.github/workflows/`, called by the repos rather than copied into them, plus starter files in `workflow-templates/` so a new repo can add them from the Actions tab in one click.

## Design rule for the workflows

Every gate has to be able to fail. This estate has collected nine checks that were green because they were not looking at anything: a secret scan that scanned zero commits, an audit with `continue-on-error: true`, a publish that treated a duplicate version as a no-op. Each workflow here states, in a comment block at the top of its own file, the exact conditions that turn it red. If a change to one of these files cannot name that condition, the change is wrong.

Three rules follow from that:

1. No `continue-on-error` and no `|| true` on a gate step.
2. Every script step runs under `set -euo pipefail`, so a tool that fails to install becomes a failure instead of a skipped check.
3. When the thing being measured is empty in a way that means the gate is blind, the job fails. When it is empty in a way that is genuinely in scope and clean, the job passes and says so in the log.

## The four workflows

| Workflow | Purpose | Goes red when |
|---|---|---|
| `gitleaks.yml` | Secret scanning with the MIT gitleaks binary | A secret appears in the PR commit range, or anywhere in history on a push. Also red if the binary download or checksum check fails, or if the PR range holds zero commits. |
| `npm-audit.yml` | Node dependency audit | `npm audit` reports an advisory at or above the audit level, default `high`. Also red if `npm ci` fails because the lockfile is missing or out of sync. |
| `python-publish.yml` | PyPI upload over trusted publishing | The build fails, produces no sdist or no wheel, fails `twine check --strict`, or the version already exists on PyPI. Also red if the OIDC exchange is refused because the trusted publisher does not match. |
| `ai-signal-scan.yml` | Human voice gate on changed text | A changed text file has more than two em-dashes, a cluster of terms from the AI lexicon, signpost scaffolding, or two or more negation constructions of the `not-just-X` shape. Also red if a listed path cannot be read, or if the shared scanner is missing. |

## How to call them

Add one file per gate under `.github/workflows/` in the calling repo. Pin to `@main` for now; switch to a tag when this repo starts tagging.

### Secret scan

```yaml
name: Secret scan

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  gitleaks:
    uses: aiexponent/.github/.github/workflows/gitleaks.yml@main
    # with:
    #   config-path: .gitleaks.toml
    #   extra-args: --baseline-path .gitleaks-baseline.json
```

Inputs: `gitleaks-version` (default `8.30.1`), `config-path`, `extra-args`.

Two things about this one are load bearing. It uses the gitleaks **binary**, because `gitleaks/gitleaks-action` is commercially licensed for org-owned repos and refuses to run on ours. And it uses `gitleaks detect`, never `gitleaks protect`, because `protect` reads the uncommitted working tree and ignores `--log-opts`, which in CI means it scans nothing and passes. Both traps are written into the comments in the workflow file.

### Dependency audit

```yaml
name: Dependency audit

on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"

permissions:
  contents: read

jobs:
  npm-audit:
    uses: aiexponent/.github/.github/workflows/npm-audit.yml@main
    # with:
    #   node-version: "20"
    #   working-directory: apps/web
    #   audit-level: high
    #   production-only: false
```

To accept one advisory that has no fix, record it in the calling repo with an `overrides` entry or an `.npmrc` line and a dated comment saying why. Never turn the gate off.

### PyPI publish

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    uses: aiexponent/.github/.github/workflows/python-publish.yml@main
    permissions:
      contents: read
      id-token: write
    with:
      environment: pypi
```

`environment` is an input because the environments already differ: riskforge publishes from `pypi-publish`, the other packages from `pypi`. A PyPI trusted publisher is bound to one environment name, so a hardcoded value would lock riskforge out. Other inputs: `python-version` (default `3.12`), `package-dir`, `repository-url`, which you can point at TestPyPI to rehearse a release.

Before the first run, configure a trusted publisher on the PyPI project with the owner `aiexponent`, the calling repo name, the workflow filename as it exists **in the calling repo**, and the environment name above. No API token is stored anywhere.

### Human voice gate

```yaml
name: Human voice gate

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  ai-signal-scan:
    uses: aiexponent/.github/.github/workflows/ai-signal-scan.yml@main
    # with:
    #   paths: "*.md *.mdx *.txt content/**/*.md"
    #   scan-all: false
```

The scanner itself is vendored here at `.github/scripts/scan-ai-signals-ci.py`, and the job checks this repo out beside the caller to reach it. Callers hold no copy, so one edit here reaches every repo. The canonical signal list lives in `vibe_skills/hooks/scan-ai-signals.py`, which is a Claude Code editor hook: it reads a JSON payload on stdin, looks at a single edit, and warns without blocking. That shape cannot run in CI, and the repo holding it is private, so the vendored file is a port with the same thresholds in a file-in, exit-code-out shape. When the canonical list changes, update the port in the same change. The prose rules behind the thresholds are in `askajay-thought-leadership/skills/_shared/ai-writing-signals.md`.

Thresholds, as implemented:

| Check | Bar |
|---|---|
| Em-dashes per file | more than 2 fails |
| AI lexicon terms | 2 distinct terms in prose files, 3 elsewhere |
| Signpost scaffolding | any hit in a prose file |
| Negation constructions, the `not-just-X` shape | 2 or more fail |

Files under 120 characters are skipped as too short to judge, and paths that quote the blocklist on purpose, such as the gate docs themselves, are skipped by name.

## Starter templates

`workflow-templates/` carries a caller file and a `.properties.json` for each of the four. They show up under **Actions, New workflow** for any repo in the org, with `$default-branch` filled in automatically.

## Adding a workflow here

1. Put it in `.github/workflows/` with `on: workflow_call` and typed inputs.
2. Open the file with a comment block naming what makes the job red.
3. Run `actionlint` over the whole directory.
4. Add a `workflow-templates/` pair and a row in the table above.
5. Migrate callers in a separate change, one repo at a time. Landing a shared workflow and switching a caller are different risks and belong in different pull requests.
