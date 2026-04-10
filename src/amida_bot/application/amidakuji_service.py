from __future__ import annotations

import asyncio
from dataclasses import dataclass
from concurrent.futures import Executor, ThreadPoolExecutor
from functools import partial

from amida_bot.domain.models import (
    DrawResult,
    GuildTemplate,
    LastUsedTemplate,
    Participant,
    TemplateSnapshot,
)
from amida_bot.domain.raffle import draw_assignments, sanitize_options
from amida_bot.errors import DrawFailedError, SaveFailedError
from amida_bot.persistence.guild_template_repository import GuildTemplatePage, GuildTemplateRepository
from amida_bot.persistence.last_used_template_repository import LastUsedTemplateRepository


@dataclass(frozen=True)
class TemplateSelection:
    source_template_id: str | None
    snapshot: TemplateSnapshot


class AmidakujiService:
    def __init__(
        self,
        guild_template_repository: GuildTemplateRepository,
        last_used_template_repository: LastUsedTemplateRepository,
        db_executor: Executor | None = None,
    ) -> None:
        self._guild_templates = guild_template_repository
        self._last_used = last_used_template_repository
        self._db_executor = db_executor or ThreadPoolExecutor(max_workers=2, thread_name_prefix="amida-db")

    async def list_guild_templates(
        self,
        guild_id: str,
        *,
        limit: int = 25,
        offset: int = 0,
    ) -> GuildTemplatePage:
        return await self._run_db(
            self._guild_templates.list_by_guild,
            guild_id,
            limit=limit,
            offset=offset,
        )

    async def create_template(
        self,
        guild_id: str,
        user_id: str,
        title: str,
        options: list[str],
    ) -> GuildTemplate:
        normalized_title = title.strip()
        normalized_options = sanitize_options(options)
        if not normalized_title:
            raise SaveFailedError("テンプレート名は必須です。")
        if not normalized_options:
            raise SaveFailedError("選択肢は1件以上必要です。")
        return await self._run_db(
            self._guild_templates.create,
            guild_id,
            normalized_title,
            normalized_options,
            user_id,
        )

    async def get_last_used_template(self, user_id: str, guild_id: str) -> LastUsedTemplate:
        return await self._run_db(self._last_used.get, user_id, guild_id)

    async def draw_with_template(
        self,
        user_id: str,
        guild_id: str,
        selected_template: TemplateSelection,
        participants: list[Participant],
    ) -> DrawResult:
        if not participants:
            raise DrawFailedError("参加者を選択してください。")
        if not selected_template.snapshot.options:
            raise DrawFailedError("テンプレートの選択肢が空です。")

        result = draw_assignments(participants, selected_template.snapshot.options)
        if not result.assignments:
            raise DrawFailedError("抽選可能なユーザーがいません。")

        await self._run_db(
            self._last_used.upsert,
            user_id,
            guild_id,
            selected_template.source_template_id,
            selected_template.snapshot,
        )
        return result

    async def _run_db(self, func, /, *args, **kwargs):
        loop = asyncio.get_running_loop()
        call = partial(func, *args, **kwargs)
        return await loop.run_in_executor(self._db_executor, call)

    def shutdown(self) -> None:
        if isinstance(self._db_executor, ThreadPoolExecutor):
            self._db_executor.shutdown(wait=False, cancel_futures=True)
