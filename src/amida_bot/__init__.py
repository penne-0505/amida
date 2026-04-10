from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor

from amida_bot.application.amidakuji_service import AmidakujiService
from amida_bot.config import load_settings
from amida_bot.discord_ui.bot import AmidaBot
from amida_bot.infra.supabase_client import create_supabase_client
from amida_bot.persistence.guild_template_repository import GuildTemplateRepository
from amida_bot.persistence.last_used_template_repository import LastUsedTemplateRepository


def main() -> None:
    settings = load_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logging.getLogger("discord").setLevel(settings.discord_log_level)
    client = create_supabase_client(settings.supabase_url, settings.supabase_service_role_key)

    guild_repo = GuildTemplateRepository(client)
    last_used_repo = LastUsedTemplateRepository(client)
    db_executor = ThreadPoolExecutor(
        max_workers=settings.db_thread_workers,
        thread_name_prefix="amida-db",
    )
    service = AmidakujiService(guild_repo, last_used_repo, db_executor=db_executor)

    bot = AmidaBot(service=service, development_guild_id=settings.development_guild_id)
    # Use app-configured root logger for both app and discord.py logs.
    # This prevents duplicate handlers while keeping discord.py logs visible.
    bot.run(settings.discord_token, log_handler=None)
