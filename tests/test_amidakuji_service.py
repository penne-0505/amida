from __future__ import annotations

import asyncio
from dataclasses import replace

from amida_bot.application.amidakuji_service import AmidakujiService
from amida_bot.discord_ui.amidakuji_flow import _can_manage_template
from amida_bot.domain.models import GuildTemplate, LastUsedTemplate, TemplateSnapshot
from amida_bot.errors import DuplicateTemplateTitleError, SaveFailedError, TemplateNotFoundError


def test_update_template_normalizes_title_and_options() -> None:
    guild_repository = _FakeGuildTemplateRepository(
        [
            _build_template(template_id="template-1", title="朝会", options=["司会", "議事録"]),
        ]
    )
    service = AmidakujiService(guild_repository, _FakeLastUsedTemplateRepository())

    updated = asyncio.run(
        service.update_template(
            guild_id="guild-1",
            template_id="template-1",
            title="  週次会議担当  ",
            options=[" 司会 ", "", " 議事録 "],
        )
    )

    assert updated.title == "週次会議担当"
    assert updated.options == ["司会", "議事録"]


def test_update_template_rejects_empty_title() -> None:
    service = AmidakujiService(_FakeGuildTemplateRepository([]), _FakeLastUsedTemplateRepository())

    try:
        asyncio.run(
            service.update_template(
                guild_id="guild-1",
                template_id="template-1",
                title="   ",
                options=["司会"],
            )
        )
    except SaveFailedError as error:
        assert str(error) == "テンプレート名は必須です。"
    else:
        raise AssertionError("SaveFailedError was not raised")


def test_update_template_rejects_empty_options_after_sanitize() -> None:
    service = AmidakujiService(_FakeGuildTemplateRepository([]), _FakeLastUsedTemplateRepository())

    try:
        asyncio.run(
            service.update_template(
                guild_id="guild-1",
                template_id="template-1",
                title="朝会",
                options=[" ", ""],
            )
        )
    except SaveFailedError as error:
        assert str(error) == "選択肢は1件以上必要です。"
    else:
        raise AssertionError("SaveFailedError was not raised")


def test_update_template_raises_on_duplicate_title() -> None:
    guild_repository = _FakeGuildTemplateRepository(
        [
            _build_template(template_id="template-1", title="朝会", options=["司会"]),
            _build_template(template_id="template-2", title="夕会", options=["司会"]),
        ]
    )
    service = AmidakujiService(guild_repository, _FakeLastUsedTemplateRepository())

    try:
        asyncio.run(
            service.update_template(
                guild_id="guild-1",
                template_id="template-2",
                title="朝会",
                options=["議事録"],
            )
        )
    except DuplicateTemplateTitleError:
        pass
    else:
        raise AssertionError("DuplicateTemplateTitleError was not raised")


def test_delete_template_removes_template_from_repository() -> None:
    guild_repository = _FakeGuildTemplateRepository(
        [
            _build_template(template_id="template-1", title="朝会", options=["司会"]),
        ]
    )
    service = AmidakujiService(guild_repository, _FakeLastUsedTemplateRepository())

    deleted = asyncio.run(service.delete_template(guild_id="guild-1", template_id="template-1"))

    assert deleted.template_id == "template-1"
    try:
        guild_repository.get_by_id("guild-1", "template-1")
    except TemplateNotFoundError:
        pass
    else:
        raise AssertionError("TemplateNotFoundError was not raised")


def test_delete_template_raises_when_template_not_found() -> None:
    service = AmidakujiService(_FakeGuildTemplateRepository([]), _FakeLastUsedTemplateRepository())

    try:
        asyncio.run(service.delete_template(guild_id="guild-1", template_id="missing"))
    except TemplateNotFoundError:
        pass
    else:
        raise AssertionError("TemplateNotFoundError was not raised")


def test_can_manage_template_for_creator() -> None:
    interaction = _FakeInteraction(user_id=42, manage_guild=False)
    template = _build_template(template_id="template-1", title="朝会", options=["司会"], created_by="42")

    assert _can_manage_template(interaction, template) is True


def test_can_manage_template_for_manage_guild_member() -> None:
    interaction = _FakeInteraction(user_id=7, manage_guild=True)
    template = _build_template(template_id="template-1", title="朝会", options=["司会"], created_by="42")

    assert _can_manage_template(interaction, template) is True


def test_can_manage_template_for_regular_member_is_false() -> None:
    interaction = _FakeInteraction(user_id=7, manage_guild=False)
    template = _build_template(template_id="template-1", title="朝会", options=["司会"], created_by="42")

    assert _can_manage_template(interaction, template) is False


def _build_template(
    *,
    template_id: str,
    title: str,
    options: list[str],
    created_by: str = "user-1",
) -> GuildTemplate:
    return GuildTemplate(
        template_id=template_id,
        guild_id="guild-1",
        title=title,
        options=options,
        created_by=created_by,
    )


class _FakeGuildTemplateRepository:
    def __init__(self, templates: list[GuildTemplate]) -> None:
        self.templates = {(template.guild_id, template.template_id): template for template in templates}

    def list_by_guild(self, guild_id: str, *, limit: int = 25, offset: int = 0):  # noqa: ANN001
        matching = [template for (key_guild_id, _), template in self.templates.items() if key_guild_id == guild_id]
        matching.sort(key=lambda item: item.template_id)
        page_templates = matching[offset : offset + limit]
        has_next = len(matching) > offset + limit
        return type("GuildTemplatePage", (), {"templates": page_templates, "has_next": has_next})()

    def get_by_id(self, guild_id: str, template_id: str) -> GuildTemplate:
        try:
            return self.templates[(guild_id, template_id)]
        except KeyError as error:
            raise TemplateNotFoundError("テンプレートが存在しません。") from error

    def create(self, guild_id: str, title: str, options: list[str], created_by: str) -> GuildTemplate:
        self._ensure_title_unique(guild_id, title, ignore_template_id=None)
        template = GuildTemplate(
            template_id=f"template-{len(self.templates) + 1}",
            guild_id=guild_id,
            title=title,
            options=options,
            created_by=created_by,
        )
        self.templates[(guild_id, template.template_id)] = template
        return template

    def update(self, template_id: str, guild_id: str, title: str, options: list[str]) -> GuildTemplate:
        current = self.get_by_id(guild_id, template_id)
        self._ensure_title_unique(guild_id, title, ignore_template_id=template_id)
        updated = replace(current, title=title, options=options)
        self.templates[(guild_id, template_id)] = updated
        return updated

    def delete(self, template_id: str, guild_id: str) -> GuildTemplate:
        current = self.get_by_id(guild_id, template_id)
        del self.templates[(guild_id, template_id)]
        return current

    def _ensure_title_unique(self, guild_id: str, title: str, *, ignore_template_id: str | None) -> None:
        normalized = _normalize_title(title)
        for (current_guild_id, current_template_id), template in self.templates.items():
            if current_guild_id != guild_id:
                continue
            if ignore_template_id is not None and current_template_id == ignore_template_id:
                continue
            if _normalize_title(template.title) == normalized:
                raise DuplicateTemplateTitleError("同名テンプレートが既に存在します。")


class _FakeLastUsedTemplateRepository:
    def get(self, user_id: str, guild_id: str) -> LastUsedTemplate:  # noqa: ARG002
        return LastUsedTemplate(
            user_id=user_id,
            guild_id=guild_id,
            source_template_id=None,
            snapshot=TemplateSnapshot(title="default", options=["A"]),
        )

    def upsert(self, user_id: str, guild_id: str, source_template_id: str | None, snapshot: TemplateSnapshot) -> None:  # noqa: ARG002
        return None


class _FakeInteraction:
    def __init__(self, *, user_id: int, manage_guild: bool) -> None:
        self.user = _FakeUser(user_id=user_id, manage_guild=manage_guild)


class _FakeUser:
    def __init__(self, *, user_id: int, manage_guild: bool) -> None:
        self.id = user_id
        self.guild_permissions = _FakePermissions(manage_guild=manage_guild)


class _FakePermissions:
    def __init__(self, *, manage_guild: bool) -> None:
        self.manage_guild = manage_guild


def _normalize_title(title: str) -> str:
    return " ".join(title.strip().split()).lower()
