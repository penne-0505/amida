---
title: Amidakuji MVP Reference
status: active
draft_status: n/a
created_at: 2026-04-10
updated_at: 2026-04-10
references:
  - ../../guide/Core/amidakuji-mvp.md
related_issues: []
related_prs: []
---

# Amidakuji MVP Reference

## Slash Command

- `/amidakuji`
- 実装: `src/amida_bot/discord_ui/amidakuji_flow.py`

## レイヤ構成

- Discord Interface: `src/amida_bot/discord_ui/`
- Application: `src/amida_bot/application/amidakuji_service.py`
- Domain: `src/amida_bot/domain/`
- Persistence: `src/amida_bot/persistence/`

## Repository API

### GuildTemplateRepository

- `list_by_guild(guild_id)`
- `get_by_title(guild_id, title)`
- `create(guild_id, title, options, created_by)`

### LastUsedTemplateRepository

- `get(user_id, guild_id)`
- `upsert(user_id, guild_id, source_template_id, snapshot)`

## データベース

マイグレーション: `supabase/migrations/20260410_000001_amida_mvp.sql`

### `guild_templates`

- `options`: `jsonb` 配列（空不可）
- `title_normalized`: trim + 空白圧縮 + 小文字化の generated column
- 制約:
  - `unique (guild_id, title_normalized)`
  - `unique (template_id, guild_id)`

### `user_guild_last_used_templates`

- 主キー: `(user_id, guild_id)`
- `template_snapshot`: `jsonb` オブジェクト（`title` と `options` 必須、`options` は空不可）
- 外部キー:
  - `(source_template_id, guild_id)` -> `guild_templates(template_id, guild_id)`
  - `on delete set null`
