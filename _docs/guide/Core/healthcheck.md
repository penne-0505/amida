---
title: Healthcheck Guide
status: active
draft_status: n/a
created_at: 2026-04-13
updated_at: 2026-04-13
references:
  - ../../reference/Core/healthcheck.md
related_issues: []
related_prs: []
---

# Healthcheck Guide

## Overview

Amida Bot は HTTP ヘルスチェックエンドポイントを公開できる。既定では `127.0.0.1:8080/healthz` を使用する。

## 設定

- `HEALTHCHECK_ENABLED`: `true` でヘルスチェックサーバを起動する
- `HEALTHCHECK_HOST`: listen するホスト
- `HEALTHCHECK_PORT`: listen するポート
- `HEALTHCHECK_PATH`: ヘルスチェックのパス

## 運用上の意味

- `200 OK`: Discord Gateway に接続済みで、Bot が `on_ready` を完了している
- `503 Service Unavailable`: 起動中、Gateway 切断中、または終了処理中

## 利用例

```bash
curl -i http://127.0.0.1:8080/healthz
```

Kubernetes や PaaS の liveness/readiness probe では、JSON 本文ではなく HTTP ステータスコードを優先して判定すること。
