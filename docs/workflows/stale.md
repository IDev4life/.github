# `stale.yml` — Stale bot cho issue & PR

Chạy **daily lúc 03:00 UTC** (có thể trigger thủ công qua `workflow_dispatch`) để đánh dấu `stale` và đóng các issue / PR không hoạt động.

Đây là workflow **org-local** — chỉ chạy trong repo `IDev4life/.github`. Nếu muốn hành vi tương tự ở repo khác, **copy** file này sang.

## Trigger

- `schedule`: `cron: "0 3 * * *"` — 03:00 UTC mỗi ngày
- `workflow_dispatch`

## Cấu hình hiện tại

|                       | Issue                           | PR                                       |
| --------------------- | ------------------------------- | ---------------------------------------- |
| Ngày inactive → stale | 60                              | 30                                       |
| Ngày stale → close    | 14                              | 14                                       |
| Label stale           | `stale`                         | `stale`                                  |
| Exempt labels         | `pinned`, `security`, `roadmap` | `pinned`, `security`, `work-in-progress` |

- `operations-per-run: 100` — giới hạn 100 thao tác mỗi run để không vượt rate limit API.

## Message

- **Stale issue:** "This issue has been automatically marked as stale..."
- **Stale PR:** "This PR has been automatically marked as stale..."
- **Close issue:** "Closing stale issue. Reopen if still relevant."
- **Close PR:** "Closing stale PR. Reopen once ready to continue."

Chỉnh message trong file workflow trực tiếp.

## Permissions

Đã khai báo trong chính workflow (file này _không_ gọi qua `workflow_call`):

```yaml
permissions:
  issues: write
  pull-requests: write
```

## Copy sang repo khác

1. Copy `.github/workflows/stale.yml` sang repo đích.
2. Review ngày inactive — repo product nhỏ có thể muốn 30/7 thay vì 60/14.
3. Kiểm tra các label exempt có tồn tại trong repo không (nếu không sẽ không có tác dụng nhưng cũng không lỗi).
