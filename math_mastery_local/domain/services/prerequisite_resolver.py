from domain.entities.mastery_state import MasteryState


class PrerequisiteResolver:
    @staticmethod
    def is_unlocked(prerequisites: list[str], state_by_topic: dict[str, MasteryState], threshold: float = 0.7) -> bool:
        if not prerequisites:
            return True
        for prereq in prerequisites:
            if state_by_topic.get(prereq, MasteryState(user_id="", topic_id=prereq)).mastery < threshold:
                return False
        return True
