from __future__ import annotations

import logging

import discord
from discord.ext import commands

from amida_bot.application.amidakuji_service import AmidakujiService
from amida_bot.discord_ui.amidakuji_flow import register_amidakuji_command
from amida_bot.healthcheck import HealthState

logger = logging.getLogger(__name__)


class AmidaBot(commands.Bot):
    def __init__(
        self,
        service: AmidakujiService,
        development_guild_id: int | None,
        health_state: HealthState | None = None,
    ) -> None:
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.service = service
        self.development_guild_id = development_guild_id
        self.health_state = health_state

    async def on_interaction(self, interaction: discord.Interaction) -> None:
        if interaction.type is discord.InteractionType.application_command:
            guild_id = str(interaction.guild_id) if interaction.guild_id is not None else "DM"
            guild_name = interaction.guild.name if interaction.guild else "DM"
            command_name = _extract_command_name(interaction)
            logger.info(
                "Command executed guild_id=%s guild_name=%s user_id=%s user_name=%s command=%s",
                guild_id,
                guild_name,
                interaction.user.id,
                str(interaction.user),
                command_name,
            )
        await super().on_interaction(interaction)

    async def setup_hook(self) -> None:
        register_amidakuji_command(self.tree, self.service)

        if self.development_guild_id:
            guild = discord.Object(id=self.development_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Slash commands synced for guild=%s", self.development_guild_id)
            return

        await self.tree.sync()
        logger.info("Global slash commands synced.")

    async def on_ready(self) -> None:
        if self.health_state is not None:
            self.health_state.mark_ready()
        logger.info("Discord gateway is ready.")

    async def on_resumed(self) -> None:
        if self.health_state is not None:
            self.health_state.mark_ready()
        logger.info("Discord gateway resumed.")

    async def on_disconnect(self) -> None:
        if self.health_state is not None:
            self.health_state.mark_gateway_disconnected()
        logger.warning("Discord gateway disconnected.")

    async def close(self) -> None:
        if self.health_state is not None:
            self.health_state.mark_closing()
        self.service.shutdown()
        await super().close()


def _extract_command_name(interaction: discord.Interaction) -> str:
    data = interaction.data
    if not isinstance(data, dict):
        return "unknown"

    command_name = str(data.get("name", "unknown"))
    options = data.get("options")
    if not isinstance(options, list):
        return command_name

    current = options
    while current:
        first = current[0]
        if not isinstance(first, dict):
            break
        option_type = first.get("type")
        if option_type in (1, 2):  # 1=subcommand, 2=subcommand_group
            command_name = f"{command_name} {first.get('name', '')}".strip()
            nested = first.get("options")
            if isinstance(nested, list):
                current = nested
                continue
        break
    return command_name
