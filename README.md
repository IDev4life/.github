# IDev4life/.github

Shared reusable GitHub Actions workflows for all IDev4life repositories.

## Workflows

### `docker-build.yml` — Reusable Docker Build

Builds and (optionally) pushes a Docker image with GHA layer cache, standard OCI labels/tags via `docker/metadata-action`, and provenance + SBOM attestations.

**Trigger:** `workflow_call`, `workflow_dispatch`

**Inputs:**

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `image_name` | ✅ | — | Image name, e.g. `IDev4life/my-app` |
| `dockerfile_path` | ❌ | `./Dockerfile` | Path to Dockerfile |
| `build_target` | ❌ | `production` | Docker build target stage |
| `registry` | ❌ | `ghcr.io` | Container registry |
| `context` | ❌ | `.` | Build context |
| `platforms` | ❌ | `linux/amd64` | Comma-separated target platforms |
| `build_args` | ❌ | `""` | Multi-line `KEY=VALUE` build args |
| `push` | ❌ | `true` | Whether to push the image |
| `provenance` | ❌ | `mode=max` | Provenance mode (`false` to disable) |
| `sbom` | ❌ | `true` | Generate SBOM attestation |

**Tag strategy** (via `docker/metadata-action`): long SHA, short SHA, branch name, PR ref, semver (on tag push), and `latest` **only on default branch**.

**Secrets:**

| Secret | Required | Notes |
|--------|----------|-------|
| `REGISTRY_TOKEN` | ❌ | Optional for `ghcr.io` (falls back to `GITHUB_TOKEN`). Required for other registries. |
| `TELEGRAM_BOT_TOKEN` | ✅ | Used by the notify job |
| `TELEGRAM_CHAT_ID` | ✅ | Used by the notify job |

**Permissions required in the caller:** `contents: read`, `packages: write`, `id-token: write`, `attestations: write`.

**Usage:**

```yaml
jobs:
  build:
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with:
      image_name: IDev4life/my-app
    secrets: inherit
```

---

### `notify-telegram.yml` — Reusable Telegram Notify

Sends a Telegram message with CI/CD status (success / failure / cancelled).

**Trigger:** `workflow_call`

**Inputs:**

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `status` | ✅ | — | `success` \| `failure` \| `cancelled` |
| `title` | ❌ | `CI/CD` | Label shown in the message |

**Secrets:** `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

**Usage:**

```yaml
notify:
  needs: build
  if: always()
  uses: IDev4life/.github/.github/workflows/notify-telegram.yml@main
  with:
    status: ${{ needs.build.result }}
    title: "BUILD"
  secrets: inherit
```

---

### `validate.yml` — Reusable Validate

Validates plugin marketplace schema, `plugin.json` files, `SKILL.md` frontmatter, README links, and runs markdownlint.

**Trigger:** `workflow_call`

**Secrets:** `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

**Usage:**

```yaml
jobs:
  validate:
    uses: IDev4life/.github/.github/workflows/validate.yml@main
    secrets: inherit
```

---

### `notify-pr.yml` — PR Telegram Notifications

Sends Telegram notifications on PR opened / merged / closed / reopened. Copy this workflow into any repository.

**Trigger:** `pull_request` (`opened`, `closed`, `reopened`)

**Secrets required in the target repo:** `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

---

## Dependabot

Actions dependencies are auto-updated weekly via Dependabot. Version pins use exact versions (e.g. `@v6.0.2`) so Dependabot can track and bump them.
