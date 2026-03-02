
def generate_session(next_actions: dict[str, list[str]], minutes: int = 20) -> dict:
    capacity = max(3, minutes // 3)
    ordered = next_actions.get("Review", []) + next_actions.get("Remediate", []) + next_actions.get("New", [])
    return {
        "minutes": minutes,
        "topics": ordered[:capacity],
        "counts": {k: len(v) for k, v in next_actions.items()},
    }
