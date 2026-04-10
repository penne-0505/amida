from __future__ import annotations

import random

from amida_bot.domain.models import Participant
from amida_bot.domain.raffle import draw_assignments


def test_draw_assignments_respects_min_rule() -> None:
    participants = [
        Participant(user_id="1", display_name="u1", mention="<@1>", is_bot=False),
        Participant(user_id="2", display_name="u2", mention="<@2>", is_bot=False),
        Participant(user_id="3", display_name="u3", mention="<@3>", is_bot=False),
    ]
    options = ["A", "B"]

    result = draw_assignments(participants, options, rng=random.Random(1))

    assert len(result.assignments) == 2
    assert len(result.unassigned_participants) == 1
    assert len(result.unused_options) == 0


def test_draw_assignments_includes_bots() -> None:
    participants = [
        Participant(user_id="1", display_name="bot", mention="<@1>", is_bot=True),
        Participant(user_id="2", display_name="user", mention="<@2>", is_bot=False),
    ]

    result = draw_assignments(participants, ["X"], rng=random.Random(1))

    assert len(result.assignments) == 1
    assigned_user_ids = {item.participant.user_id for item in result.assignments}
    assert assigned_user_ids in ({"1"}, {"2"})
    assert len(result.excluded_bots) == 0
