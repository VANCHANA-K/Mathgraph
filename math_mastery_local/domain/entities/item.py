from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    item_id: str
    topic_id: str
    question: str
    answer: str
    difficulty: float = 0.5
