from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateSnapshot:
    title: str
    options: list[str]


@dataclass(frozen=True)
class GuildTemplate:
    template_id: str
    guild_id: str
    title: str
    options: list[str]
    created_by: str
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True)
class LastUsedTemplate:
    user_id: str
    guild_id: str
    source_template_id: str | None
    snapshot: TemplateSnapshot
    updated_at: str | None = None


@dataclass(frozen=True)
class Participant:
    user_id: str
    display_name: str
    mention: str
    is_bot: bool
    avatar_url: str | None = None


@dataclass(frozen=True)
class Assignment:
    participant: Participant
    option: str


@dataclass(frozen=True)
class DrawResult:
    assignments: list[Assignment]
    unassigned_participants: list[Participant]
    unused_options: list[str]
    excluded_bots: list[Participant]
