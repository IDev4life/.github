# `validate.yml` — Validate schema & tài liệu

Kiểm tra:

- Plugin marketplace schema
- Các file `plugin.json`
- Frontmatter của `SKILL.md` (qua PyYAML)
- Link trong README và `references/*.md` của skill
- `markdownlint-cli2`

Toàn bộ logic nằm ở `scripts/` trong repo `IDev4life/.github` và được checkout runtime — caller repo **không cần ship thêm gì**.

## Trigger

`workflow_call`

## Inputs

| Input        | Bắt buộc | Mặc định | Mô tả                                                                           |
| ------------ | -------- | -------- | ------------------------------------------------------------------------------- |
| `shared_ref` | ❌       | `main`   | Ref của `IDev4life/.github` để load scripts/config (pin `@vX.Y.Z` ở production) |

## Secrets

| Secret               | Bắt buộc |
| -------------------- | -------- |
| `TELEGRAM_BOT_TOKEN` | ❌       |
| `TELEGRAM_CHAT_ID`   | ❌       |

## Yêu cầu

- Repo `IDev4life/.github` phải truy cập được bằng `GITHUB_TOKEN` của caller (public, hoặc internal trong cùng org).

## Cách dùng

```yaml
jobs:
  validate:
    uses: IDev4life/.github/.github/workflows/validate.yml@main
    secrets: inherit
```

### Pin shared_ref ở production

```yaml
with:
  shared_ref: v1.0.0
```

## Ghi chú

- Khi `IDev4life/.github` có breaking change ở `scripts/`, caller pin `@main` sẽ bị ảnh hưởng ngay. Luôn pin ref ở repo production.
