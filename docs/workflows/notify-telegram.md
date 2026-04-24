# `notify-telegram.yml` — Thông báo Telegram

Gửi thông báo trạng thái CI/CD (success / failure / cancelled) vào một Telegram chat.

## Trigger

`workflow_call`

## Inputs

| Input    | Bắt buộc | Mặc định | Mô tả                                 |
| -------- | -------- | -------- | ------------------------------------- |
| `status` | ✅       | —        | `success` \| `failure` \| `cancelled` |
| `title`  | ❌       | `CI/CD`  | Nhãn hiển thị trong message           |

## Secrets

| Secret               | Bắt buộc |
| -------------------- | -------- |
| `TELEGRAM_BOT_TOKEN` | ✅       |
| `TELEGRAM_CHAT_ID`   | ✅       |

## Cách dùng

```yaml
jobs:
  build:
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with: { image_name: IDev4life/my-app }
    secrets: inherit

  notify:
    needs: build
    if: always()
    uses: IDev4life/.github/.github/workflows/notify-telegram.yml@main
    with:
      status: ${{ needs.build.result }}
      title: "BUILD"
    secrets: inherit
```

## Ghi chú

- Đặt `if: always()` ở job notify để message vẫn được gửi khi job trước fail/cancel.
- `${{ needs.<job>.result }}` trả đúng các giá trị `success` / `failure` / `cancelled` / `skipped`. Nếu là `skipped`, message vẫn gửi nhưng hiển thị `skipped`.
