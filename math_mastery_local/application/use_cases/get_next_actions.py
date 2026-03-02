from datetime import datetime

from domain.entities.mastery_state import MasteryState
from domain.services.next_action_planner import NextActionPlanner
from domain.services.prerequisite_resolver import PrerequisiteResolver


def get_next_actions(user_id: str, topic_repo, graph_repo, mastery_repo) -> dict[str, list[str]]:
    topics = topic_repo.list_topics()
    states = {s.topic_id: s for s in mastery_repo.list_states(user_id)}

    for topic in topics:
        if topic.topic_id not in states:
            states[topic.topic_id] = MasteryState(user_id=user_id, topic_id=topic.topic_id)

    unlocked = []
    for topic in topics:
        prereqs = graph_repo.prerequisites_of(topic.topic_id)
        if PrerequisiteResolver.is_unlocked(prereqs, states):
            unlocked.append(states[topic.topic_id])

    return NextActionPlanner.plan(unlocked, datetime.utcnow())
