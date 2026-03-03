def generate_session(next_actions: dict[str, list[str]], minutes: int = 20) -> dict:
    capacity = max(3, minutes // 3)

    review = next_actions.get("review", next_actions.get("Review", []))
    remediate = next_actions.get("remediate", next_actions.get("Remediate", []))
    new = next_actions.get("new", next_actions.get("New", []))
    ordered = review + remediate + new

    return {
        "minutes": minutes,
        "topics": ordered[:capacity],
        "counts": {k: len(v) for k, v in next_actions.items()},
    }
