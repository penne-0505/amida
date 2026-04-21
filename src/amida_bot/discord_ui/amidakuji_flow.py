from __future__ import annotations

import logging

import discord
from discord import app_commands

from amida_bot.application.amidakuji_service import AmidakujiService, TemplateSelection
from amida_bot.domain.models import Assignment, GuildTemplate, Participant, TemplateSnapshot
from amida_bot.errors import (
    AmidaError,
    DeleteFailedError,
    DrawFailedError,
    DuplicateTemplateTitleError,
    LastUsedNotFoundError,
    SaveFailedError,
    TemplateNotFoundError,
)

logger = logging.getLogger(__name__)


def build_system_embed(
    title: str,
    description: str | None = None,
    *,
    is_error: bool = False,
) -> discord.Embed:
    color = discord.Color.red() if is_error else discord.Color.blurple()
    embed = discord.Embed(title=title, color=color)
    if description:
        embed.description = description
    return embed


async def handle_amidakuji_command(interaction: discord.Interaction, service: AmidakujiService) -> None:
    if interaction.guild_id is None:
        await interaction.response.send_message(
            embed=build_system_embed("guild内でのみ使用できます。", is_error=True),
            ephemeral=True,
        )
        return
    view = StartView(service=service, owner_id=interaction.user.id)
    await interaction.response.send_message(
        embed=build_system_embed("テンプレートの使い方を選択してください。"),
        view=view,
        ephemeral=True,
    )


class OwnerOnlyView(discord.ui.View):
    def __init__(self, owner_id: int, *, timeout: float = 600.0) -> None:
        super().__init__(timeout=timeout)
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                embed=build_system_embed("この操作はコマンド実行者のみ可能です。", is_error=True),
                ephemeral=True,
            )
            return False
        return True


class StartView(OwnerOnlyView):
    def __init__(self, service: AmidakujiService, owner_id: int) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service

    @discord.ui.button(label="既存テンプレートを使う", style=discord.ButtonStyle.primary)
    async def use_existing(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        try:
            page = await self.service.list_guild_templates(
                str(interaction.guild_id),
                limit=25,
                offset=0,
            )
        except Exception as error:  # noqa: BLE001
            logger.exception("template list failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート一覧取得に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        if not page.templates:
            await interaction.response.send_message(
                embed=build_system_embed("利用可能なテンプレートがありません。", is_error=True),
                ephemeral=True,
            )
            return

        view = ExistingTemplateView(
            service=self.service,
            owner_id=self.owner_id,
            guild_id=str(interaction.guild_id),
            page_index=0,
            page_size=25,
            templates=page.templates,
            has_next=page.has_next,
        )
        await interaction.response.edit_message(
            embed=view.build_page_embed(),
            view=view,
        )

    @discord.ui.button(label="テンプレートを新規作成する", style=discord.ButtonStyle.secondary)
    async def create_new(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        await interaction.response.send_modal(NewTemplateTitleModal(service=self.service, owner_id=self.owner_id))

    @discord.ui.button(label="最後に使ったテンプレートを使う", style=discord.ButtonStyle.success)
    async def use_last_used(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        try:
            last_used = await self.service.get_last_used_template(
                user_id=str(interaction.user.id),
                guild_id=str(interaction.guild_id),
            )
        except LastUsedNotFoundError:
            await interaction.response.send_message(
                embed=build_system_embed("last used テンプレートが見つかりません。", is_error=True),
                ephemeral=True,
            )
            return
        except Exception as error:  # noqa: BLE001
            logger.exception("last used fetch failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("last used 取得に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        selected_template = TemplateSelection(
            source_template_id=last_used.source_template_id,
            snapshot=last_used.snapshot,
        )
        view = ParticipantSelectionView(
            service=self.service,
            owner_id=self.owner_id,
            selected_template=selected_template,
        )
        await interaction.response.edit_message(
            embed=build_system_embed(
                f"last used テンプレート: {last_used.snapshot.title}",
                "参加者を選択してください。",
            ),
            view=view,
        )


class ExistingTemplateSelect(discord.ui.Select["ExistingTemplateView"]):
    def __init__(self, templates: list[GuildTemplate]) -> None:
        options = [
            discord.SelectOption(
                label=template.title[:100],
                value=template.template_id,
                description=f"選択肢: {len(template.options)}件",
            )
            for template in templates
        ]
        super().__init__(
            placeholder="テンプレートを選択",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.view.on_template_selected(interaction, self.values[0])


class ExistingTemplateView(OwnerOnlyView):
    def __init__(
        self,
        service: AmidakujiService,
        owner_id: int,
        guild_id: str,
        page_index: int,
        page_size: int,
        templates: list[GuildTemplate],
        has_next: bool,
    ) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service
        self.guild_id = guild_id
        self.page_index = page_index
        self.page_size = page_size
        self.has_next = has_next
        self.templates = {item.template_id: item for item in templates}
        self.add_item(ExistingTemplateSelect(templates))
        self._update_pagination_buttons()

    def _update_pagination_buttons(self) -> None:
        self.go_prev.disabled = self.page_index == 0
        self.go_next.disabled = not self.has_next

    def build_page_embed(self) -> discord.Embed:
        return build_system_embed(
            f"既存テンプレートを選択してください。（ページ {self.page_index + 1}）",
            "テンプレートが25件を超える場合は「前へ/次へ」で移動できます。",
        )

    async def _load_page(self, interaction: discord.Interaction, next_page_index: int) -> None:
        try:
            page = await self.service.list_guild_templates(
                self.guild_id,
                limit=self.page_size,
                offset=next_page_index * self.page_size,
            )
        except Exception as error:  # noqa: BLE001
            logger.exception("template list page fetch failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート一覧取得に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        if not page.templates:
            await interaction.response.send_message(
                embed=build_system_embed("このページに表示できるテンプレートがありません。", is_error=True),
                ephemeral=True,
            )
            return

        self.page_index = next_page_index
        self.has_next = page.has_next
        self.templates = {item.template_id: item for item in page.templates}

        self.clear_items()
        self.add_item(ExistingTemplateSelect(page.templates))
        self.add_item(self.go_prev)
        self.add_item(self.go_next)
        self._update_pagination_buttons()
        await interaction.response.edit_message(embed=self.build_page_embed(), view=self)

    @discord.ui.button(label="前へ", style=discord.ButtonStyle.secondary)
    async def go_prev(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if self.page_index == 0:
            await interaction.response.defer()
            return
        await self._load_page(interaction, self.page_index - 1)

    @discord.ui.button(label="次へ", style=discord.ButtonStyle.secondary)
    async def go_next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if not self.has_next:
            await interaction.response.defer()
            return
        await self._load_page(interaction, self.page_index + 1)

    async def on_template_selected(self, interaction: discord.Interaction, template_id: str) -> None:
        selected = self.templates.get(template_id)
        if selected is None:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレートが存在しません。", is_error=True),
                ephemeral=True,
            )
            return
        next_view = TemplateActionView(
            service=self.service,
            owner_id=self.owner_id,
            guild_id=self.guild_id,
            page_index=self.page_index,
            page_size=self.page_size,
            template=selected,
            can_manage=_can_manage_template(interaction, selected),
        )
        await interaction.response.edit_message(
            embed=next_view.build_embed(),
            view=next_view,
        )


class NewTemplateTitleModal(discord.ui.Modal, title="新規テンプレート作成"):
    template_title = discord.ui.TextInput(
        label="テンプレート名",
        placeholder="例: 週次ミーティング担当",
        max_length=100,
    )

    def __init__(self, service: AmidakujiService, owner_id: int) -> None:
        super().__init__()
        self.service = service
        self.owner_id = owner_id

    async def on_submit(self, interaction: discord.Interaction) -> None:
        title = str(self.template_title).strip()
        if not title:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート名は必須です。", is_error=True),
                ephemeral=True,
            )
            return

        builder_view = TemplateBuilderView(
            service=self.service,
            owner_id=self.owner_id,
            title=title,
        )
        await interaction.response.send_message(embed=builder_view.render_embed(), view=builder_view, ephemeral=True)
        message = await interaction.original_response()
        builder_view.message = message


class EditTemplateTitleModal(discord.ui.Modal, title="テンプレート名を編集"):
    template_title = discord.ui.TextInput(
        label="テンプレート名",
        placeholder="例: 週次ミーティング担当",
        max_length=100,
    )

    def __init__(self, builder: "TemplateBuilderView") -> None:
        super().__init__()
        self.builder = builder
        self.template_title.default = builder.title

    async def on_submit(self, interaction: discord.Interaction) -> None:
        title = str(self.template_title).strip()
        if not title:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート名は必須です。", is_error=True),
                ephemeral=True,
            )
            return
        self.builder.title = title
        await interaction.response.defer(ephemeral=True)
        await self.builder.refresh_message()


class AddOptionModal(discord.ui.Modal, title="選択肢を追加"):
    option_name = discord.ui.TextInput(
        label="選択肢",
        placeholder="例: 司会",
        max_length=100,
    )

    def __init__(self, builder: "TemplateBuilderView") -> None:
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction: discord.Interaction) -> None:
        option = str(self.option_name).strip()
        if not option:
            await interaction.response.send_message(
                embed=build_system_embed("空の選択肢は追加できません。", is_error=True),
                ephemeral=True,
            )
            return
        self.builder.options.append(option)
        await interaction.response.defer(ephemeral=True)
        await self.builder.refresh_message()


class BulkEditOptionsModal(discord.ui.Modal, title="選択肢を一括編集"):
    options_input = discord.ui.TextInput(
        label="選択肢（1行に1件）",
        placeholder="司会\n議事録\nタイムキーパー",
        max_length=2000,
        style=discord.TextStyle.paragraph,
    )

    def __init__(self, builder: "TemplateBuilderView") -> None:
        super().__init__()
        self.builder = builder
        self.options_input.default = "\n".join(builder.options)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        options = [line.strip() for line in str(self.options_input).splitlines() if line.strip()]
        if not options:
            await interaction.response.send_message(
                embed=build_system_embed("選択肢を1件以上入力してください。", is_error=True),
                ephemeral=True,
            )
            return
        self.builder.options = options
        await interaction.response.defer(ephemeral=True)
        await self.builder.refresh_message()


class TemplateActionView(OwnerOnlyView):
    def __init__(
        self,
        service: AmidakujiService,
        owner_id: int,
        guild_id: str,
        page_index: int,
        page_size: int,
        template: GuildTemplate,
        can_manage: bool,
    ) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service
        self.guild_id = guild_id
        self.page_index = page_index
        self.page_size = page_size
        self.template = template
        self.can_manage = can_manage
        if not can_manage:
            self.remove_item(self.edit_template)
            self.remove_item(self.delete_template)

    def build_embed(self) -> discord.Embed:
        lines = [
            f"選択肢: {len(self.template.options)}件",
            "",
            "次の操作を選択してください。",
        ]
        preview = _build_options_preview(self.template.options)
        if preview:
            lines.append("")
            lines.append(preview)
        if not self.can_manage:
            lines.extend(
                [
                    "",
                    "このテンプレートは抽選のみ利用できます。",
                ]
            )
        return build_system_embed(f"テンプレート: {self.template.title}", "\n".join(lines))

    @discord.ui.button(label="抽選へ進む", style=discord.ButtonStyle.success)
    async def start_draw(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        template_selection = TemplateSelection(
            source_template_id=self.template.template_id,
            snapshot=TemplateSnapshot(title=self.template.title, options=self.template.options),
        )
        next_view = ParticipantSelectionView(
            service=self.service,
            owner_id=self.owner_id,
            selected_template=template_selection,
        )
        await interaction.response.edit_message(
            embed=build_system_embed(
                f"テンプレート: {self.template.title}",
                "参加者を選択してください。",
            ),
            view=next_view,
        )

    @discord.ui.button(label="編集する", style=discord.ButtonStyle.primary)
    async def edit_template(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if not self.can_manage:
            await interaction.response.send_message(
                embed=build_system_embed("このテンプレートを編集する権限がありません。", is_error=True),
                ephemeral=True,
            )
            return
        try:
            latest = await self.service.get_template(self.guild_id, self.template.template_id)
        except TemplateNotFoundError:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレートが存在しません。", is_error=True),
                ephemeral=True,
            )
            return
        except Exception as error:  # noqa: BLE001
            logger.exception("template fetch failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート取得に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        builder_view = TemplateBuilderView(
            service=self.service,
            owner_id=self.owner_id,
            title=latest.title,
            options=latest.options,
            template_id=latest.template_id,
        )
        await interaction.response.send_message(
            embed=builder_view.render_embed(),
            view=builder_view,
            ephemeral=True,
        )
        builder_view.message = await interaction.original_response()

    @discord.ui.button(label="削除する", style=discord.ButtonStyle.danger)
    async def delete_template(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if not self.can_manage:
            await interaction.response.send_message(
                embed=build_system_embed("このテンプレートを削除する権限がありません。", is_error=True),
                ephemeral=True,
            )
            return
        confirm_view = TemplateDeleteConfirmView(
            service=self.service,
            owner_id=self.owner_id,
            guild_id=self.guild_id,
            page_index=self.page_index,
            page_size=self.page_size,
            template=self.template,
        )
        await interaction.response.edit_message(embed=confirm_view.build_embed(), view=confirm_view)

    @discord.ui.button(label="一覧へ戻る", style=discord.ButtonStyle.secondary)
    async def back_to_list(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        try:
            embed, view = await _build_existing_template_listing(
                service=self.service,
                owner_id=self.owner_id,
                guild_id=self.guild_id,
                page_index=self.page_index,
                page_size=self.page_size,
            )
        except Exception as error:  # noqa: BLE001
            logger.exception("template list restore failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート一覧取得に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(embed=embed, view=view)


class TemplateDeleteConfirmView(OwnerOnlyView):
    def __init__(
        self,
        service: AmidakujiService,
        owner_id: int,
        guild_id: str,
        page_index: int,
        page_size: int,
        template: GuildTemplate,
    ) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service
        self.guild_id = guild_id
        self.page_index = page_index
        self.page_size = page_size
        self.template = template

    def build_embed(self) -> discord.Embed:
        description = "\n".join(
            [
                "この操作は取り消せません。",
                "削除後も last used に保存されたスナップショットからの抽選は継続できます。",
            ]
        )
        return build_system_embed(f"テンプレート {self.template.title} を削除しますか？", description, is_error=True)

    @discord.ui.button(label="削除を確定", style=discord.ButtonStyle.danger)
    async def confirm_delete(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        try:
            deleted = await self.service.delete_template(self.guild_id, self.template.template_id)
            embed, view = await _build_existing_template_listing(
                service=self.service,
                owner_id=self.owner_id,
                guild_id=self.guild_id,
                page_index=self.page_index,
                page_size=self.page_size,
            )
        except TemplateNotFoundError:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレートが存在しません。", is_error=True),
                ephemeral=True,
            )
            return
        except DeleteFailedError as error:
            logger.exception("template delete failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed(str(error), is_error=True),
                ephemeral=True,
            )
            return
        except Exception as error:  # noqa: BLE001
            logger.exception("template delete failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("テンプレート削除に失敗しました。", is_error=True),
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(
            embed=build_system_embed(
                f"テンプレート {deleted.title} を削除しました。",
                embed.description,
            ),
            view=view,
        )

    @discord.ui.button(label="キャンセル", style=discord.ButtonStyle.secondary)
    async def cancel_delete(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        action_view = TemplateActionView(
            service=self.service,
            owner_id=self.owner_id,
            guild_id=self.guild_id,
            page_index=self.page_index,
            page_size=self.page_size,
            template=self.template,
            can_manage=True,
        )
        await interaction.response.edit_message(embed=action_view.build_embed(), view=action_view)


class TemplateBuilderView(OwnerOnlyView):
    def __init__(
        self,
        service: AmidakujiService,
        owner_id: int,
        title: str,
        *,
        options: list[str] | None = None,
        template_id: str | None = None,
    ) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service
        self.title = title
        self.options = options[:] if options else []
        self.template_id = template_id
        self.message: discord.InteractionMessage | None = None
        self.save_template.label = "更新して抽選へ進む" if self.template_id else "保存して抽選へ進む"

    def render_embed(self) -> discord.Embed:
        mode_text = "テンプレートを編集しています。" if self.template_id else "テンプレートを作成しています。"
        lines = [
            mode_text,
            "「選択肢を追加」で1件ずつ追加するか、「選択肢を一括編集」でまとめて更新してください。",
            "",
        ]
        preview = _build_options_preview(self.options)
        lines.append(preview if preview else "現在の選択肢: なし")
        return build_system_embed(f"テンプレート名: {self.title}", "\n".join(lines))

    async def refresh_message(self) -> None:
        if self.message is None:
            return
        await self.message.edit(embed=self.render_embed(), view=self)

    @discord.ui.button(label="タイトルを編集", style=discord.ButtonStyle.secondary)
    async def edit_title(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        await interaction.response.send_modal(EditTemplateTitleModal(self))

    @discord.ui.button(label="選択肢を追加", style=discord.ButtonStyle.primary)
    async def add_option(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        await interaction.response.send_modal(AddOptionModal(self))

    @discord.ui.button(label="選択肢を一括編集", style=discord.ButtonStyle.secondary)
    async def edit_options(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        await interaction.response.send_modal(BulkEditOptionsModal(self))

    @discord.ui.button(label="保存して抽選へ進む", style=discord.ButtonStyle.success)
    async def save_template(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if not self.options:
            await interaction.response.send_message(
                embed=build_system_embed("選択肢を1件以上追加してください。", is_error=True),
                ephemeral=True,
            )
            return
        try:
            if self.template_id is None:
                saved = await self.service.create_template(
                    guild_id=str(interaction.guild_id),
                    user_id=str(interaction.user.id),
                    title=self.title,
                    options=self.options,
                )
            else:
                saved = await self.service.update_template(
                    guild_id=str(interaction.guild_id),
                    template_id=self.template_id,
                    title=self.title,
                    options=self.options,
                )
        except DuplicateTemplateTitleError:
            await interaction.response.send_message(
                embed=build_system_embed("同名テンプレートが既に存在します。", is_error=True),
                ephemeral=True,
            )
            return
        except TemplateNotFoundError:
            await interaction.response.send_message(
                embed=build_system_embed("テンプレートが存在しません。", is_error=True),
                ephemeral=True,
            )
            return
        except SaveFailedError as error:
            logger.exception("template save failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed(str(error), is_error=True),
                ephemeral=True,
            )
            return
        except Exception as error:  # noqa: BLE001
            logger.exception("template save failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("保存失敗", is_error=True),
                ephemeral=True,
            )
            return

        selected_template = TemplateSelection(
            source_template_id=saved.template_id,
            snapshot=TemplateSnapshot(title=saved.title, options=saved.options),
        )
        next_view = ParticipantSelectionView(
            service=self.service,
            owner_id=self.owner_id,
            selected_template=selected_template,
        )
        message = f"テンプレート {saved.title} を更新しました。" if self.template_id else f"テンプレート {saved.title} を保存しました。"
        await interaction.response.edit_message(
            embed=build_system_embed(
                message,
                "参加者を選択してください。",
            ),
            view=next_view,
        )


class ParticipantSelect(discord.ui.UserSelect["ParticipantSelectionView"]):
    def __init__(self) -> None:
        super().__init__(min_values=1, max_values=25, placeholder="参加者を選択")

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.view.on_participants_selected(interaction, list(self.values))


class ParticipantSelectionView(OwnerOnlyView):
    def __init__(
        self,
        service: AmidakujiService,
        owner_id: int,
        selected_template: TemplateSelection,
    ) -> None:
        super().__init__(owner_id=owner_id)
        self.service = service
        self.selected_template = selected_template
        self.selected_members: list[discord.Member | discord.User] = []
        self.add_item(ParticipantSelect())

    async def on_participants_selected(
        self,
        interaction: discord.Interaction,
        members: list[discord.Member | discord.User],
    ) -> None:
        self.selected_members = members
        await interaction.response.defer()

    @discord.ui.button(label="抽選を実行", style=discord.ButtonStyle.success)
    async def run_draw(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[discord.ui.View],  # noqa: ARG002
    ) -> None:
        if not self.selected_members:
            await interaction.response.send_message(
                embed=build_system_embed("参加者を選択してください。", is_error=True),
                ephemeral=True,
            )
            return

        participants = [
            Participant(
                user_id=str(member.id),
                display_name=getattr(member, "display_name", member.name),
                mention=member.mention,
                is_bot=member.bot,
                avatar_url=str(member.display_avatar.url),
            )
            for member in self.selected_members
        ]

        try:
            draw_result = await self.service.draw_with_template(
                user_id=str(interaction.user.id),
                guild_id=str(interaction.guild_id),
                selected_template=self.selected_template,
                participants=participants,
            )
        except DrawFailedError as error:
            logger.warning("draw failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed(str(error), is_error=True),
                ephemeral=True,
            )
            return
        except AmidaError as error:
            logger.exception("amida operation failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed(str(error), is_error=True),
                ephemeral=True,
            )
            return
        except Exception as error:  # noqa: BLE001
            logger.exception("draw failed: %s", error)
            await interaction.response.send_message(
                embed=build_system_embed("抽選失敗", is_error=True),
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(
            embeds=build_assignment_embeds(draw_result.assignments),
            view=None,
        )


def build_assignment_embed(assignment: Assignment) -> discord.Embed:
    embed = discord.Embed(
        description=f"> **{assignment.option}**",
        color=discord.Color.from_rgb(43, 45, 49),
    )
    if assignment.participant.avatar_url:
        embed.set_author(
            name=assignment.participant.display_name,
            icon_url=assignment.participant.avatar_url,
        )
    else:
        embed.set_author(name=assignment.participant.display_name)
    return embed


def build_assignment_embeds(assignments: list[Assignment]) -> list[discord.Embed]:
    embeds = [build_assignment_embed(item) for item in assignments]
    if len(embeds) <= 10:
        return embeds

    visible = embeds[:9]
    remaining = assignments[9:]
    lines = [f"- {item.participant.mention} -> **{item.option}**" for item in remaining]
    description = "\n".join(lines)
    if len(description) > 3500:
        description = f"{description[:3500]}\n..."
    visible.append(
        build_system_embed(
            f"残り {len(remaining)} 件",
            description,
        )
    )
    return visible


def _build_options_preview(options: list[str]) -> str:
    if not options:
        return ""
    lines = ["現在の選択肢:"]
    visible_options = options[:10]
    lines.extend([f"{index}. {option}" for index, option in enumerate(visible_options, start=1)])
    if len(options) > len(visible_options):
        lines.append(f"...他 {len(options) - len(visible_options)} 件")
    preview = "\n".join(lines)
    if len(preview) > 1500:
        return f"{preview[:1500]}\n..."
    return preview


def _can_manage_template(interaction: discord.Interaction, template: GuildTemplate) -> bool:
    if str(interaction.user.id) == template.created_by:
        return True
    permissions = getattr(interaction.user, "guild_permissions", None)
    return bool(permissions and getattr(permissions, "manage_guild", False))


async def _build_existing_template_listing(
    service: AmidakujiService,
    owner_id: int,
    guild_id: str,
    page_index: int,
    page_size: int,
) -> tuple[discord.Embed, discord.ui.View]:
    current_page_index = page_index
    while current_page_index > 0:
        page = await service.list_guild_templates(
            guild_id,
            limit=page_size,
            offset=current_page_index * page_size,
        )
        if page.templates:
            view = ExistingTemplateView(
                service=service,
                owner_id=owner_id,
                guild_id=guild_id,
                page_index=current_page_index,
                page_size=page_size,
                templates=page.templates,
                has_next=page.has_next,
            )
            return view.build_page_embed(), view
        current_page_index -= 1

    first_page = await service.list_guild_templates(
        guild_id,
        limit=page_size,
        offset=0,
    )
    if not first_page.templates:
        start_view = StartView(service=service, owner_id=owner_id)
        return build_system_embed("利用可能なテンプレートがありません。", is_error=True), start_view

    view = ExistingTemplateView(
        service=service,
        owner_id=owner_id,
        guild_id=guild_id,
        page_index=0,
        page_size=page_size,
        templates=first_page.templates,
        has_next=first_page.has_next,
    )
    return view.build_page_embed(), view


def register_amidakuji_command(tree: app_commands.CommandTree, service: AmidakujiService) -> None:
    @tree.command(name="amidakuji", description="テンプレートで担当をランダム割当します")
    async def amidakuji(interaction: discord.Interaction) -> None:
        await handle_amidakuji_command(interaction, service)
