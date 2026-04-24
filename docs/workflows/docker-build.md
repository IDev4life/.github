# `docker-build.yml` — Build & Push Docker image

Build và (tuỳ chọn) push Docker image lên registry với GHA layer cache, OCI labels/tags chuẩn qua `docker/metadata-action`, kèm **build provenance attestation** và **SBOM**.

## Trigger

- `workflow_call`
- `workflow_dispatch`

## Inputs

| Input             | Bắt buộc | Mặc định       | Mô tả                                               |
| ----------------- | -------- | -------------- | --------------------------------------------------- |
| `image_name`      | ✅       | —              | Tên image, ví dụ `IDev4life/my-app`                 |
| `dockerfile_path` | ❌       | `./Dockerfile` | Đường dẫn tới Dockerfile                            |
| `build_target`    | ❌       | `""`           | Stage trong Dockerfile để build (rỗng = stage cuối) |
| `registry`        | ❌       | `ghcr.io`      | Container registry                                  |
| `context`         | ❌       | `.`            | Build context                                       |
| `platforms`       | ❌       | `linux/amd64`  | Platform target (phẩy phân tách nếu nhiều)          |
| `build_args`      | ❌       | `""`           | Build args dạng `KEY=VALUE`, mỗi dòng một cặp       |
| `push`            | ❌       | `true`         | Có push image lên registry không                    |
| `provenance`      | ❌       | `mode=max`     | Provenance mode của buildx. Set `"false"` để tắt    |
| `sbom`            | ❌       | `true`         | Sinh SBOM attestation                               |

### Chiến lược tag

`docker/metadata-action` tự sinh các tag sau:

- Long SHA, short SHA
- Tên branch / PR ref
- Semver khi push tag
- `latest` **chỉ** trên default branch

## Secrets

| Secret               | Bắt buộc | Ghi chú                                                                                 |
| -------------------- | -------- | --------------------------------------------------------------------------------------- |
| `REGISTRY_TOKEN`     | ❌       | Không bắt buộc cho `ghcr.io` (fallback sang `GITHUB_TOKEN`). Bắt buộc cho registry khác |
| `TELEGRAM_BOT_TOKEN` | ✅       | Dùng cho job notify                                                                     |
| `TELEGRAM_CHAT_ID`   | ✅       | Dùng cho job notify                                                                     |

## Permissions (khai báo ở caller)

```yaml
permissions:
  contents: read
  packages: write
  id-token: write
  attestations: write
```

## Cách dùng

### Đơn giản nhất

```yaml
jobs:
  build:
    permissions:
      contents: read
      packages: write
      id-token: write
      attestations: write
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with:
      image_name: IDev4life/my-app
    secrets: inherit
```

### Build target tuỳ biến + multi-arch

```yaml
jobs:
  build:
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with:
      image_name: IDev4life/my-app
      build_target: runtime
      platforms: linux/amd64,linux/arm64
      build_args: |
        NODE_ENV=production
        APP_VERSION=${{ github.sha }}
    secrets: inherit
```

### Build không push (chạy PR)

```yaml
with:
  image_name: IDev4life/my-app
  push: false
  provenance: "false" # không sinh attestation khi không push
```

## Verify provenance sau khi build

Attestation được push kèm image, verify bằng GitHub CLI:

```bash
gh attestation verify oci://ghcr.io/IDev4life/my-app:sha-abc123 \
  --owner IDev4life
```

## Ghi chú

- `build_target` default là chuỗi rỗng, nghĩa là `docker build` sẽ build stage cuối của Dockerfile. Các Dockerfile single-stage hoạt động bình thường mà không cần override input này.
- Provenance attestation dùng `actions/attest-build-provenance@v4.1.0`, **tách biệt** với provenance nội bộ của buildx — verify bằng `gh attestation verify` / cosign dễ hơn.
