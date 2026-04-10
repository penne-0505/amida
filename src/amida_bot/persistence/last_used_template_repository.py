from __future__ import annotations

import logging
from typing import Any

from postgrest.exceptions import APIError
from supabase import Client

from amida_bot.domain.models import LastUsedTemplate, TemplateSnapshot
from amida_bot.errors import LastUsedNotFoundError, SaveFailedError

logger = logging.getLogger(__name__)


class LastUsedTemplateRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self, user_id: str, guild_id: str) -> LastUsedTemplate:
        response = (
            self._client.table("user_guild_last_used_templates")
            .select("user_id,guild_id,source_template_id,template_snapshot,updated_at")
            .eq("user_id", user_id)
            .eq("guild_id", guild_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            raise LastUsedNotFoundError("last used テンプレートが存在しません。")
        return _to_model(response.data[0])

    def upsert(
        self,
        user_id: str,
        guild_id: str,
        source_template_id: str | None,
        snapshot: TemplateSnapshot,
    ) -> None:
        payload = {
            "user_id": user_id,
            "guild_id": guild_id,
            "source_template_id": source_template_id,
            "template_snapshot": {
                "title": snapshot.title,
                "options": snapshot.options,
            },
        }
        try:
            self._client.table("user_guild_last_used_templates").upsert(
                payload,
                on_conflict="user_id,guild_id",
            ).execute()
        except APIError as error:
            logger.exception("last_used upsert failed: %s", error)
            raise SaveFailedError("last used の保存に失敗しました。") from error


def _to_model(row: dict[str, Any]) -> LastUsedTemplate:
    snapshot = row["template_snapshot"]
    return LastUsedTemplate(
        user_id=str(row["user_id"]),
        guild_id=str(row["guild_id"]),
        source_template_id=str(row["source_template_id"]) if row["source_template_id"] else None,
        snapshot=TemplateSnapshot(
            title=str(snapshot["title"]),
            options=[str(item) for item in snapshot["options"]],
        ),
        updated_at=row.get("updated_at"),
    )
