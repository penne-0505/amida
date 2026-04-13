from __future__ import annotations

import os
from dataclasses import dataclass
import logging

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    discord_token: str
    supabase_url: str
    supabase_service_role_key: str
    development_guild_id: int | None
    log_level: int
    discord_log_level: int
    db_thread_workers: int
    healthcheck_enabled: bool
    healthcheck_host: str
    healthcheck_port: int
    healthcheck_path: str


def load_settings() -> Settings:
    load_dotenv()

    discord_token = os.getenv("DISCORD_TOKEN", "").strip()
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    dev_guild_id_raw = os.getenv("DEVELOPMENT_GUILD_ID", "").strip()
    log_level_raw = os.getenv("LOG_LEVEL", "WARNING").strip()
    discord_log_level_raw = os.getenv("DISCORD_LOG_LEVEL", log_level_raw).strip()
    db_thread_workers_raw = os.getenv("DB_THREAD_WORKERS", "2").strip()
    healthcheck_enabled_raw = os.getenv("HEALTHCHECK_ENABLED", "true").strip()
    healthcheck_host = os.getenv("HEALTHCHECK_HOST", "127.0.0.1").strip()
    healthcheck_port_raw = os.getenv("HEALTHCHECK_PORT", "8080").strip()
    healthcheck_path_raw = os.getenv("HEALTHCHECK_PATH", "/healthz").strip()

    if not discord_token:
        raise ValueError("DISCORD_TOKEN is required.")
    if not supabase_url:
        raise ValueError("SUPABASE_URL is required.")
    if not supabase_service_role_key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required.")
    if not healthcheck_host:
        raise ValueError("HEALTHCHECK_HOST is required.")

    development_guild_id = int(dev_guild_id_raw) if dev_guild_id_raw else None
    log_level = _parse_log_level(log_level_raw, "LOG_LEVEL")
    discord_log_level = _parse_log_level(discord_log_level_raw, "DISCORD_LOG_LEVEL")
    db_thread_workers = _parse_positive_int(db_thread_workers_raw, "DB_THREAD_WORKERS")
    healthcheck_enabled = _parse_bool(healthcheck_enabled_raw, "HEALTHCHECK_ENABLED")
    healthcheck_port = _parse_port(healthcheck_port_raw, "HEALTHCHECK_PORT")
    healthcheck_path = _parse_http_path(healthcheck_path_raw, "HEALTHCHECK_PATH")

    return Settings(
        discord_token=discord_token,
        supabase_url=supabase_url,
        supabase_service_role_key=supabase_service_role_key,
        development_guild_id=development_guild_id,
        log_level=log_level,
        discord_log_level=discord_log_level,
        db_thread_workers=db_thread_workers,
        healthcheck_enabled=healthcheck_enabled,
        healthcheck_host=healthcheck_host,
        healthcheck_port=healthcheck_port,
        healthcheck_path=healthcheck_path,
    )


def _parse_log_level(value: str, name: str) -> int:
    normalized = value.strip().upper()
    if normalized.isdigit():
        return int(normalized)
    level = logging.getLevelName(normalized)
    if isinstance(level, int):
        return level
    raise ValueError(f"{name} must be a valid logging level.")


def _parse_positive_int(value: str, name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer.") from error
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return parsed


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean.")


def _parse_port(value: str, name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer.") from error
    if parsed < 0 or parsed > 65535:
        raise ValueError(f"{name} must be between 0 and 65535.")
    return parsed


def _parse_http_path(value: str, name: str) -> str:
    normalized = value.strip()
    if not normalized.startswith("/"):
        raise ValueError(f"{name} must start with '/'.")
    return normalized
