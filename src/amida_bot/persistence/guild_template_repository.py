from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from postgrest.exceptions import APIError
from supabase import Client

from amida_bot.domain.models import GuildTemplate
from amida_bot.errors import DuplicateTemplateTitleError, SaveFailedError, TemplateNotFoundError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GuildTemplatePage:
    templates: list[GuildTemplate]
    has_next: bool


class GuildTemplateRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list_by_guild(self, guild_id: str, *, limit: int = 25, offset: int = 0) -> GuildTemplatePage:
        fetch_size = limit + 1
        response = (
            self._client.table("guild_templates")
            .select("template_id,guild_id,title,options,created_by,created_at,updated_at")
            .eq("guild_id", guild_id)
            .order("updated_at", desc=True)
            .range(offset, offset + fetch_size - 1)
            .execute()
        )
        rows = response.data or []
        models = [_to_model(row) for row in rows[:limit]]
        return GuildTemplatePage(
            templates=models,
            has_next=len(rows) > limit,
        )

    def get_by_title(self, guild_id: str, title: str) -> GuildTemplate:
        response = (
            self._client.table("guild_templates")
            .select("template_id,guild_id,title,options,created_by,created_at,updated_at")
            .eq("guild_id", guild_id)
            .eq("title_normalized", _normalize_title(title))
            .limit(1)
            .execute()
        )
        if not response.data:
            raise TemplateNotFoundError("テンプレートが存在しません。")
        return _to_model(response.data[0])

    def create(self, guild_id: str, title: str, options: list[str], created_by: str) -> GuildTemplate:
        payload = {
            "guild_id": guild_id,
            "title": title,
            "options": options,
            "created_by": created_by,
        }
        try:
            response = (
                self._client.table("guild_templates")
                .insert(payload)
                .execute()
            )
        except APIError as error:
            message = str(error).lower()
            if "duplicate key" in message or "unique" in message:
                raise DuplicateTemplateTitleError("同名テンプレートが既に存在します。") from error
            logger.exception("guild_templates insert failed: %s", error)
            raise SaveFailedError("テンプレート保存に失敗しました。") from error

        if not response.data:
            raise SaveFailedError("テンプレート保存に失敗しました。")
        return _to_model(response.data[0])


def _to_model(row: dict[str, Any]) -> GuildTemplate:
    return GuildTemplate(
        template_id=str(row["template_id"]),
        guild_id=str(row["guild_id"]),
        title=str(row["title"]),
        options=[str(item) for item in row["options"]],
        created_by=str(row["created_by"]),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def _normalize_title(title: str) -> str:
    return " ".join(title.strip().split()).lower()
