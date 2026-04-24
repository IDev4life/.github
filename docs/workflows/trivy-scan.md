# `trivy-scan.yml` — Quét CVE container image

Quét image đã build bằng **Trivy**, fail build khi có CVE theo severity chỉ định, upload SARIF lên **GitHub Code Scanning** (tab Security).

## Trigger

`workflow_call`

## Inputs

| Input            | Bắt buộc | Mặc định        | Mô tả                                             |
| ---------------- | -------- | --------------- | ------------------------------------------------- |
| `image_ref`      | ✅       | —               | Image ref đầy đủ, VD `ghcr.io/org/app:sha-abc123` |
| `severity`       | ❌       | `CRITICAL,HIGH` | Severity gây fail (phẩy phân tách)                |
| `ignore_unfixed` | ❌       | `true`          | Bỏ qua CVE chưa có fix                            |
| `exit_code`      | ❌       | `"1"`           | Trivy exit code khi phát hiện vuln                |
| `upload_sarif`   | ❌       | `true`          | Upload SARIF lên GitHub Code Scanning             |

## Secrets

| Secret           | Bắt buộc | Ghi chú                                                |
| ---------------- | -------- | ------------------------------------------------------ |
| `REGISTRY_TOKEN` | ❌       | Cần khi image nằm ở private registry (ngoài `ghcr.io`) |

Với `ghcr.io`, workflow fallback sang `GITHUB_TOKEN` tự động (không cần secret).

## Permissions (khai báo ở caller)

```yaml
permissions:
  contents: read
  security-events: write # bắt buộc để upload SARIF
  packages: read # pull image từ ghcr.io
```

## Cách dùng

### Chain sau docker-build

```yaml
jobs:
  build:
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with:
      image_name: IDev4life/my-app
    secrets: inherit

  scan:
    needs: build
    permissions:
      contents: read
      security-events: write
      packages: read
    uses: IDev4life/.github/.github/workflows/trivy-scan.yml@main
    with:
      image_ref: ghcr.io/IDev4life/my-app:${{ github.sha }}
    secrets: inherit
```

### Nới severity, chỉ fail ở CRITICAL

```yaml
with:
  image_ref: ghcr.io/IDev4life/my-app:sha-${{ github.sha }}
  severity: CRITICAL
```

### Chỉ report (không fail build)

```yaml
with:
  image_ref: ghcr.io/IDev4life/my-app:sha-${{ github.sha }}
  exit_code: "0"
```

## Cơ chế

Workflow chạy Trivy **2 lượt**:

1. **Table format** — hiển thị log để developer đọc, dùng `exit_code` của caller → fail build khi có vuln.
2. **SARIF format** — `exit_code: "0"` (không fail), upload qua `codeql-action/upload-sarif@v4.35.2` để hiện ở tab _Security → Code scanning_.

Bước "Detect registry" dùng shell vì GitHub Actions **không cho phép** `secrets.*` trong `if:` cấp step → phải tính sẵn output `has_token`.

## Lưu ý

- `aquasecurity/trivy-action@v0.36.0` cache DB tự động giữa các run.
- SARIF category là `trivy` — nếu bạn chạy nhiều scanner (Trivy + Grype + Snyk), mỗi scanner nên có category riêng để không ghi đè nhau.
