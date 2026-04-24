# `node-ci.yml` — CI cho Node / TypeScript

Install → lint → test → build cho dự án Node.js. Hỗ trợ **npm**, **pnpm**, **yarn**. Publish JUnit annotation và upload coverage lên Codecov.

## Trigger

`workflow_call`

## Inputs

| Input                | Bắt buộc | Mặc định        | Mô tả                                                     |
| -------------------- | -------- | --------------- | --------------------------------------------------------- |
| `node_version`       | ❌       | `24`            | Node.js major version (yêu cầu Actions Runner ≥ v2.327.1) |
| `package_manager`    | ❌       | `npm`           | `npm` / `pnpm` / `yarn`                                   |
| `pnpm_version`       | ❌       | `10`            | Chỉ áp dụng khi `package_manager: pnpm`                   |
| `install_command`    | ❌       | _infer_         | Override lệnh install (VD `npm ci --legacy-peer-deps`)    |
| `lint_command`       | ❌       | `run lint`      | Set chuỗi rỗng `""` để skip                               |
| `test_command`       | ❌       | `run test`      | Set chuỗi rỗng `""` để skip                               |
| `build_command`      | ❌       | `run build`     | Set chuỗi rỗng `""` để skip                               |
| `working_directory`  | ❌       | `.`             | Cho monorepo                                              |
| `coverage_paths`     | ❌       | _default_       | Glob coverage file để upload Codecov                      |
| `junit_report_paths` | ❌       | _default_       | Glob JUnit XML (jest-junit, vitest junit reporter, ...)   |
| `upload_coverage`    | ❌       | `true`          | Upload lên Codecov nếu có `CODECOV_TOKEN`                 |
| `runs_on`            | ❌       | `ubuntu-latest` | Runner label                                              |

### Lệnh install mặc định

| `package_manager` | Lệnh                             |
| ----------------- | -------------------------------- |
| `npm`             | `npm ci`                         |
| `pnpm`            | `pnpm install --frozen-lockfile` |
| `yarn`            | `yarn install --immutable`       |

## Secrets

| Secret          | Bắt buộc | Ghi chú                                                                        |
| --------------- | -------- | ------------------------------------------------------------------------------ |
| `CODECOV_TOKEN` | ❌       | Không có thì bước upload coverage tự skip                                      |
| `NPM_TOKEN`     | ❌       | Expose thành `NODE_AUTH_TOKEN` cho scripts `npm publish` hoặc private registry |

## Permissions (khai báo ở caller)

```yaml
permissions:
  contents: read
  checks: write # JUnit annotation
  pull-requests: write # coverage PR comment
```

## Cách dùng

### npm (default)

```yaml
jobs:
  ci:
    uses: IDev4life/.github/.github/workflows/node-ci.yml@main
    secrets: inherit
```

### pnpm + monorepo

```yaml
jobs:
  ci:
    uses: IDev4life/.github/.github/workflows/node-ci.yml@main
    with:
      package_manager: pnpm
      pnpm_version: "10"
      working_directory: packages/web
      test_command: "run test:ci"
    secrets: inherit
```

### Skip build (thư viện không có bước build)

```yaml
with:
  build_command: ""
```

### Override lệnh install cho repo có peer-deps phức tạp

```yaml
with:
  install_command: "npm ci --legacy-peer-deps"
```

## Đầu ra

- **JUnit annotation:** từ `mikepenz/action-junit-report@v6.4.0`, đòi hỏi test runner xuất JUnit XML (cấu hình `jest-junit` hoặc reporter tương tự trong repo caller).
- **Codecov upload:** tự động tìm `coverage/**/*.xml`, `coverage/**/lcov.info` trừ khi override `coverage_paths`.

## Lưu ý

- `setup-node@v6.4.0` cache theo cả 3 lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) nên caller nào cũng hit cache.
- Node 24 **yêu cầu Actions Runner ≥ v2.327.1**. GitHub-hosted runner đã đủ điều kiện; self-hosted cần update.
- Biến `$PKG_MANAGER $CMD` trong step lint/test/build cố tình word-split (`# shellcheck disable=SC2086`) để hỗ trợ command như `"run lint"` → `npm run lint`.
