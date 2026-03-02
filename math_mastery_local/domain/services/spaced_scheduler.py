from datetime import datetime, timedelta

from domain.entities.mastery_state import MasteryState


class SpacedScheduler:
    @staticmethod
    def update_due(state: MasteryState, now: datetime) -> MasteryState:
        mastery_factor = 0.5 + state.mastery
        days = max(1.0, state.stability * mastery_factor)
        state.due_at = now + timedelta(days=days)
        return state
