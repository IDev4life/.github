# IDev4life/.github

Shared reusable GitHub Actions workflows for all IDev4life repositories.

## Workflows

### `docker-build.yml` — Reusable Docker Build

Builds and pushes a Docker image to a container registry with GHA layer cache.

**Trigger:** `workflow_call`

**Inputs:**

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `image_name` | ✅ | — | Image name, e.g. `IDev4life/my-app` |
| `dockerfile_path` | ❌ | `./Dockerfile` | Path to Dockerfile |
| `build_target` | ❌ | `production` | Docker build target stage |
| `registry` | ❌ | `ghcr.io` | Container registry |

**Secrets:** `REGISTRY_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

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
