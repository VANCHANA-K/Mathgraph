from datetime import datetime

from domain.entities.mastery_state import MasteryState


class NextActionPlanner:
    @staticmethod
    def plan(states: list[MasteryState], now: datetime) -> dict[str, list[str]]:
        review = [s.topic_id for s in states if s.due_at and s.due_at <= now]
        remediate = [s.topic_id for s in states if s.mastery < 0.5]
        new = [s.topic_id for s in states if s.mastery == 0.0]
        return {
            "Review": sorted(set(review)),
            "Remediate": sorted(set(remediate)),
            "New": sorted(set(new)),
        }
