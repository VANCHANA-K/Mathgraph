from datetime import datetime

from domain.entities.attempt import Attempt
from domain.entities.mastery_state import MasteryState
from domain.services.mastery_updater import MasteryUpdater
from domain.services.spaced_scheduler import SpacedScheduler


def submit_attempt(
    user_id: str,
    item_id: str,
    topic_id: str,
    is_correct: bool,
    response_seconds: int,
    used_hint: bool,
    attempt_repo,
    mastery_repo,
) -> MasteryState:
    now = datetime.utcnow()
    attempt_repo.add_attempt(
        Attempt(
            user_id=user_id,
            item_id=item_id,
            topic_id=topic_id,
            is_correct=is_correct,
            response_seconds=response_seconds,
            used_hint=used_hint,
            attempted_at=now,
        )
    )

    state = mastery_repo.get_state(user_id, topic_id) or MasteryState(user_id=user_id, topic_id=topic_id)
    state = MasteryUpdater.update(
        state,
        is_correct=is_correct,
        response_seconds=response_seconds,
        used_hint=used_hint,
        now=now,
    )
    state = SpacedScheduler.update_due(state, now)
    mastery_repo.upsert_state(state)
    return state
