from dataclasses import dataclass
from datetime import datetime


@dataclass
class MasteryState:
    user_id: str
    topic_id: str
    mastery: float = 0.0
    stability: float = 1.0
    due_at: datetime | None = None
    last_practiced_at: datetime | None = None
