from __future__ import annotations

import random

from amida_bot.domain.models import Assignment, DrawResult, Participant


def sanitize_options(raw_options: list[str]) -> list[str]:
    cleaned: list[str] = []
    for option in raw_options:
        normalized = option.strip()
        if normalized:
            cleaned.append(normalized)
    return cleaned


def draw_assignments(
    participants: list[Participant],
    options: list[str],
    rng: random.Random | None = None,
) -> DrawResult:
    rng = rng or random.Random()
    valid_options = sanitize_options(options)

    shuffled_participants = participants[:]
    shuffled_options = valid_options[:]
    rng.shuffle(shuffled_participants)
    rng.shuffle(shuffled_options)

    assignable_count = min(len(shuffled_participants), len(shuffled_options))
    assignments = [
        Assignment(participant=shuffled_participants[i], option=shuffled_options[i])
        for i in range(assignable_count)
    ]
    unassigned_participants = shuffled_participants[assignable_count:]
    unused_options = shuffled_options[assignable_count:]

    return DrawResult(
        assignments=assignments,
        unassigned_participants=unassigned_participants,
        unused_options=unused_options,
        excluded_bots=[],
    )
