# Tài liệu workflow `IDev4life/.github`

Thư mục này chứa tài liệu chi tiết cho từng reusable workflow và các tiện ích org-level do repo `IDev4life/.github` cung cấp.

## Mục lục

### CI / Build

| Workflow             | Mô tả                                                             | Tài liệu                                         |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| `docker-build.yml`   | Build & push Docker image kèm OCI labels, cache, provenance, SBOM | [docker-build.md](workflows/docker-build.md)     |
| `java-spring-ci.yml` | CI cho dự án Java / Spring (Maven hoặc Gradle)                    | [java-spring-ci.md](workflows/java-spring-ci.md) |
| `node-ci.yml`        | CI cho dự án Node / TypeScript (npm / pnpm / yarn)                | [node-ci.md](workflows/node-ci.md)               |
| `validate.yml`       | Kiểm tra plugin marketplace schema + `SKILL.md` + link            | [validate.md](workflows/validate.md)             |

### Security

| Workflow         | Mô tả                                      | Tài liệu                                   |
| ---------------- | ------------------------------------------ | ------------------------------------------ |
| `trivy-scan.yml` | Quét CVE cho container image, upload SARIF | [trivy-scan.md](workflows/trivy-scan.md)   |
| `codeql.yml`     | Phân tích CodeQL đa ngôn ngữ               | [workflows/codeql.md](workflows/codeql.md) |

### Notifications

| Workflow              | Mô tả                                        | Tài liệu                                           |
| --------------------- | -------------------------------------------- | -------------------------------------------------- |
| `notify-telegram.yml` | Gửi kết quả CI/CD qua Telegram               | [notify-telegram.md](workflows/notify-telegram.md) |
| `notify-pr.yml`       | Thông báo PR open/merged/closed qua Telegram | [notify-pr.md](workflows/notify-pr.md)             |

### Org-local

| Workflow    | Mô tả                                        | Tài liệu                       |
| ----------- | -------------------------------------------- | ------------------------------ |
| `stale.yml` | Bot đánh dấu & đóng issue/PR không hoạt động | [stale.md](workflows/stale.md) |

## Quy ước chung

- **Pin phiên bản:** các ví dụ bên dưới dùng `@main` cho gọn, nhưng repo thật cần pin `@vX.Y.Z` (xem mục _Versioning_ trong [README gốc](../README.md)).
- **`secrets: inherit`** là cách đơn giản nhất để caller truyền toàn bộ secret cho reusable workflow. Nếu repo caller không có secret `CODECOV_TOKEN` / `NPM_TOKEN` / `TELEGRAM_*` thì các bước tương ứng sẽ tự bỏ qua (đã gate bằng `if:`).
- **Permissions:** mỗi tài liệu liệt kê rõ các quyền caller cần khai báo ở job gọi `uses:`. Nếu thiếu, GitHub Actions sẽ fail ngay bước đầu.
- **Concurrency:** tất cả workflow trong bộ này đều set concurrency group theo repo + ref để các push nhanh liên tiếp tự cancel run cũ — không cần caller config thêm.
