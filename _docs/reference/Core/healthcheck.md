---
title: Healthcheck Reference
status: active
draft_status: n/a
created_at: 2026-04-13
updated_at: 2026-04-13
references:
  - ../../guide/Core/healthcheck.md
related_issues: []
related_prs: []
---

# Healthcheck Reference

## Overview

Bot プロセスは軽量な組み込み HTTP サーバでヘルスチェックを提供する。

## API

### `GET /healthz`

- **Summary**: Bot の起動状態と Discord Gateway 接続状態を返す
- **Parameters**: なし
- **Returns**: JSON ボディと HTTP ステータスコード
- **Errors**: `404 Not Found` (`HEALTHCHECK_PATH` 以外)
- **Examples**:

正常時:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: no-store

{
  "status": "ok",
  "service": "amida-bot",
  "version": "0.1.0",
  "timestamp": "2026-04-13T04:40:00Z",
  "uptime_seconds": 86432
}
```

異常時:

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json; charset=utf-8
Cache-Control: no-store

{
  "status": "error",
  "service": "amida-bot",
  "version": "0.1.0",
  "timestamp": "2026-04-13T04:40:10Z",
  "uptime_seconds": 86442,
  "reason": "discord gateway disconnected"
}
```

## Notes

- `status code` を最優先の判定材料とする
- `reason` は現在 `bot is starting` / `discord gateway disconnected` / `bot is shutting down` を返す
- `HEAD /healthz` でも同じステータスコードとヘッダを返す
