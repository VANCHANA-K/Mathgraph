from dataclasses import dataclass


@dataclass(frozen=True)
class Topic:
    topic_id: str
    name: str
    description: str = ""
