from domain.services.session_builder import SessionBuilder


def generate_session(actions, item_repo=None, minutes: int = 20):
    if item_repo is None:
        # Backward compatibility with old topic-only planning flow.
        capacity = max(3, minutes // 3)
        review = actions.get("review", actions.get("Review", []))
        remediate = actions.get("remediate", actions.get("Remediate", []))
        new = actions.get("new", actions.get("New", []))
        ordered = review + remediate + new
        return {
            "minutes": minutes,
            "topics": ordered[:capacity],
            "counts": {k: len(v) for k, v in actions.items()},
        }

    builder = SessionBuilder(item_repo)
    return builder.build_session(actions, total_questions=15)
