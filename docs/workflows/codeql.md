# `codeql.yml` — CodeQL Analysis

GitHub Advanced Security — phân tích tĩnh đa ngôn ngữ qua CodeQL, chạy **song song** cho mỗi ngôn ngữ trong matrix.

## Trigger

`workflow_call`

## Inputs

| Input        | Bắt buộc | Mặc định                                 | Mô tả                                                                 |
| ------------ | -------- | ---------------------------------------- | --------------------------------------------------------------------- |
| `languages`  | ✅       | —                                        | **JSON array string**, VD `'["java-kotlin","javascript-typescript"]'` |
| `build_mode` | ❌       | `none`                                   | `none` / `autobuild` / `manual`                                       |
| `queries`    | ❌       | `security-extended,security-and-quality` | Query suite CodeQL                                                    |
| `runs_on`    | ❌       | `ubuntu-latest`                          | Runner label                                                          |

### Language codes CodeQL

| Code                    | Ngôn ngữ                 |
| ----------------------- | ------------------------ |
| `actions`               | GitHub Actions workflows |
| `c-cpp`                 | C / C++                  |
| `csharp`                | C#                       |
| `go`                    | Go                       |
| `java-kotlin`           | Java & Kotlin            |
| `javascript-typescript` | JavaScript & TypeScript  |
| `python`                | Python                   |
| `ruby`                  | Ruby                     |
| `rust`                  | Rust                     |
| `swift`                 | Swift                    |

## Permissions (khai báo ở caller)

```yaml
permissions:
  contents: read
  security-events: write # upload CodeQL database analysis
  actions: read
  packages: read
```

## Cách dùng

### Repo Java/Kotlin

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 3 * * 1" # Thứ 2 hàng tuần

jobs:
  codeql:
    permissions:
      contents: read
      security-events: write
      actions: read
      packages: read
    uses: IDev4life/.github/.github/workflows/codeql.yml@main
    with:
      languages: '["java-kotlin"]'
      build_mode: autobuild
```

### Repo polyglot (TS + Python)

```yaml
with:
  languages: '["javascript-typescript","python"]'
  build_mode: none
```

### Build manual (Java custom)

```yaml
with:
  languages: '["java-kotlin"]'
  build_mode: manual
```

Với `build_mode: manual`, caller cần tuỳ biến workflow (hoặc fork) để thêm bước build trước `analyze` — reusable workflow này không hỗ trợ inject step.

## Ghi chú

- `languages` **bắt buộc là JSON array string** (để dùng với `fromJSON()` trong matrix). Không chấp nhận CSV.
- Query suite mặc định `security-extended,security-and-quality` cho ra **nhiều warning hơn** `security` thuần — chấp nhận để audit code quality.
- Timeout 360 phút: CodeQL trên repo lớn (monorepo Java) chạy lâu.
- Chỉ repo có **GitHub Advanced Security** (enterprise hoặc public) mới thấy kết quả ở tab Security.
