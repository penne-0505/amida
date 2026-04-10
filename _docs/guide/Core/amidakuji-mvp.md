---
title: Amidakuji MVP Guide
status: active
draft_status: n/a
created_at: 2026-04-10
updated_at: 2026-04-10
references:
  - ../../reference/Core/amidakuji-mvp.md
related_issues: []
related_prs: []
---

# Amidakuji MVP Guide

## Overview

`/amidakuji` を起点として、テンプレート選択と参加者選択を行い、ランダムな役割割当を返す。

## 操作手順

1. Discord で `/amidakuji` を実行する。
2. 開始メニューで次のいずれかを選ぶ。
   - 既存テンプレートを使う
   - テンプレートを新規作成する
   - 最後に使ったテンプレートを使う
3. 新規作成の場合はテンプレート名を入力後、「選択肢を追加」で1件ずつ登録する。
4. 参加者を User Select で複数選択する。
5. 「抽選を実行」を押す。

## 抽選ルール

- Bot アカウントも抽選対象に含める。
- 対応付け件数は `min(参加者数, 選択肢数)`。
- 結果は対応付けのみ表示する。
- 抽選成功時に user x guild の last used を更新する。

## エラーハンドリング

以下は簡潔なメッセージを Discord 上に返す。

- テンプレートが存在しない
- last used が存在しない
- テンプレート名重複
- 保存失敗
- 抽選失敗
