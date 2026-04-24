# `notify-pr.yml` — Thông báo PR qua Telegram

Gửi Telegram notification khi PR được `opened` / `closed` (bao gồm merged) / `reopened`.

## Trigger

`pull_request` với types: `opened`, `closed`, `reopened`.

Đây **không phải reusable workflow** — cần **copy** file vào từng repo muốn dùng.

## Secrets (ở repo đích)

| Secret               | Bắt buộc |
| -------------------- | -------- |
| `TELEGRAM_BOT_TOKEN` | ✅       |
| `TELEGRAM_CHAT_ID`   | ✅       |

## Cách dùng

1. Copy file `.github/workflows/notify-pr.yml` từ repo này sang repo của bạn.
2. Vào **Settings → Secrets and variables → Actions** của repo đích, thêm 2 secret ở trên.
3. Push — lần PR sau sẽ có notify.

## Phân biệt với `notify-telegram.yml`

|          | `notify-telegram.yml`      | `notify-pr.yml`         |
| -------- | -------------------------- | ----------------------- |
| Loại     | Reusable (`workflow_call`) | Event-driven standalone |
| Trigger  | Caller chủ động `uses:`    | `pull_request` events   |
| Dùng khi | Báo kết quả CI/CD build    | Báo lifecycle của PR    |
