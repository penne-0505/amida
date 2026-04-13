# Amida Discord Bot

Amida は、Discord guild で共有されるテンプレートを使って参加者へ役割をランダム割当する Bot です。  
MVP では `/amidakuji` から以下の体験を提供します。

- 既存テンプレートを使う
- テンプレートを新規作成する（選択肢を一件ずつ追加）
- 最後に使ったテンプレートを使う（user x guild 単位）

## 技術スタック

- Python 3.12
- `discord.py`
- Supabase (PostgreSQL)
- `uv`（環境/依存管理）

## セットアップ

1. 依存インストール

```bash
uv sync
```

2. 環境変数設定

`.env.example` を `.env` にコピーし、値を設定してください。

```env
DISCORD_TOKEN=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
DEVELOPMENT_GUILD_ID=
LOG_LEVEL=WARNING
DISCORD_LOG_LEVEL=WARNING
DB_THREAD_WORKERS=2
HEALTHCHECK_ENABLED=true
HEALTHCHECK_HOST=127.0.0.1
HEALTHCHECK_PORT=8080
HEALTHCHECK_PATH=/healthz
```

`LOG_LEVEL` はアプリ全体、`DISCORD_LOG_LEVEL` は `discord.py` ログの出力レベルです。  
低スペック環境でログI/Oを抑える場合は `WARNING` などを指定してください。
`DB_THREAD_WORKERS` はDBアクセス用スレッドプールのワーカー数です。
`HEALTHCHECK_ENABLED=true` の場合は、`HEALTHCHECK_HOST:HEALTHCHECK_PORT` に HTTP ヘルスチェックエンドポイントを公開します。
`HEALTHCHECK_PATH` の既定値は `/healthz` です。

3. Supabase マイグレーション適用

`supabase/migrations/20260410_000001_amida_mvp.sql` を Supabase 側で適用してください。

## 実行

```bash
uv run amida-bot
```

Bot 起動中は `GET /healthz` が利用できます。Discord Gateway に接続して `on_ready` 済みであれば `200 OK`、起動中・切断中・終了中は `503 Service Unavailable` を返します。  
ヘルスチェックは本文よりステータスコードを優先する前提で、`Cache-Control: no-store` を返します。

## テスト

```bash
uv run pytest
```
