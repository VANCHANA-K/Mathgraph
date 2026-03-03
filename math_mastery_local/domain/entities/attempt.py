from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Attempt:
    user_id: str
    item_id: str
    topic_id: str
    is_correct: bool
    response_seconds: int
    used_hint: bool
    attempted_at: datetime
