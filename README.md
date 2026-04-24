# IDev4life/.github

Shared reusable GitHub Actions workflows and organization-wide community
health defaults for every IDev4life repository.

## Versioning & pinning (callers)

All usage examples below reference `@main` for readability, but **for any
repository whose CI you care about, pin the workflow to a released tag** of
`IDev4life/.github` (e.g. `@v1.0.0`). Using `@main` means every merge into this
repo can change CI behaviour in downstream repos immediately, including
potentially breaking ones.

```yaml
# Recommended for production
uses: IDev4life/.github/.github/workflows/docker-build.yml@v1.0.0

# Convenient for experiments / internal repos only
uses: IDev4life/.github/.github/workflows/docker-build.yml@main
```

### Releases

Tags and `CHANGELOG.md` are produced automatically by
[release-please](https://github.com/googleapis/release-please) driven by
[Conventional Commits](https://www.conventionalcommits.org/):

- Merging `feat:` commits to `main` → minor bump (or patch while `0.x`).
- Merging `fix:` commits → patch bump.
- `feat!:` / `BREAKING CHANGE:` footer → major bump.
- release-please opens a "chore: release X.Y.Z" PR that aggregates the
  pending changes. Merging that PR creates the git tag + GitHub Release.
- To cut the first `v1.0.0` from `0.0.0`, include `Release-As: 1.0.0` in a
  commit footer (or `BREAKING CHANGE:`) before merging.

## Workflows

Tài liệu chi tiết cho từng workflow nằm trong thư mục [`docs/`](docs/README.md). Tóm tắt:

### CI / Build

| Workflow             | Mô tả                                                            | Tài liệu                                                             |
| -------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- |
| `docker-build.yml`   | Build & push Docker image (OCI labels, cache, provenance, SBOM)  | [docs/workflows/docker-build.md](docs/workflows/docker-build.md)     |
| `java-spring-ci.yml` | CI Java / Spring (Maven hoặc Gradle) + JUnit annotation + JaCoCo | [docs/workflows/java-spring-ci.md](docs/workflows/java-spring-ci.md) |
| `node-ci.yml`        | CI Node / TS (npm / pnpm / yarn) + JUnit annotation + Codecov    | [docs/workflows/node-ci.md](docs/workflows/node-ci.md)               |
| `validate.yml`       | Validate plugin schema / `SKILL.md` / links / markdownlint       | [docs/workflows/validate.md](docs/workflows/validate.md)             |

### Security

| Workflow         | Mô tả                                  | Tài liệu                                                     |
| ---------------- | -------------------------------------- | ------------------------------------------------------------ |
| `trivy-scan.yml` | Quét CVE container image, upload SARIF | [docs/workflows/trivy-scan.md](docs/workflows/trivy-scan.md) |
| `codeql.yml`     | CodeQL analysis đa ngôn ngữ            | [docs/workflows/codeql.md](docs/workflows/codeql.md)         |

### Notifications

| Workflow              | Mô tả                                               | Tài liệu                                                               |
| --------------------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| `notify-telegram.yml` | Reusable — báo kết quả CI/CD qua Telegram           | [docs/workflows/notify-telegram.md](docs/workflows/notify-telegram.md) |
| `notify-pr.yml`       | Standalone — báo PR open/merged/closed qua Telegram | [docs/workflows/notify-pr.md](docs/workflows/notify-pr.md)             |

### Org-local

| Workflow    | Mô tả                             | Tài liệu                                           |
| ----------- | --------------------------------- | -------------------------------------------------- |
| `stale.yml` | Bot đóng issue/PR không hoạt động | [docs/workflows/stale.md](docs/workflows/stale.md) |

---

## Dependabot

Actions dependencies are auto-updated weekly via Dependabot. Version pins use exact versions (e.g. `@v6.0.2`) so Dependabot can track and bump them.

## Organization defaults

This repository doubles as the special [`.github` repo](https://docs.github.com/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
for the IDev4life organization. The following files apply as defaults to every
repo in the org that does not ship its own copy:

| File                                                                   | Scope                                            |
| ---------------------------------------------------------------------- | ------------------------------------------------ |
| [`SECURITY.md`](SECURITY.md)                                           | How to report vulnerabilities                    |
| [`CONTRIBUTING.md`](CONTRIBUTING.md)                                   | Default contributing guide                       |
| [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | Default PR template                              |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE)                    | Default issue templates (bug / feature)          |
| [`.github/CODEOWNERS`](.github/CODEOWNERS)                             | Owners of **this** repo (not inherited by org)   |
| [`profile/README.md`](profile/README.md)                               | Org profile landing page on github.com/IDev4life |
