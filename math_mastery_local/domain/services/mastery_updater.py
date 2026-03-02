from datetime import datetime

from domain.entities.mastery_state import MasteryState


class MasteryUpdater:
    @staticmethod
    def update(
        state: MasteryState,
        *,
        is_correct: bool,
        response_seconds: int,
        used_hint: bool,
        now: datetime,
    ) -> MasteryState:
        delta = 0.12 if is_correct else -0.15
        if response_seconds > 90:
            delta -= 0.03
        elif response_seconds < 30:
            delta += 0.02
        if used_hint:
            delta -= 0.05

        state.mastery = min(1.0, max(0.0, state.mastery + delta))

        if is_correct:
            state.stability = min(365.0, state.stability * 1.25)
        else:
            state.stability = max(1.0, state.stability * 0.6)

        state.last_practiced_at = now
        return state
