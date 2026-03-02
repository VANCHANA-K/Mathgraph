from typing import Protocol

from domain.entities.attempt import Attempt


class AttemptRepository(Protocol):
    def add_attempt(self, attempt: Attempt) -> None: ...
    def list_attempts(self, user_id: str, topic_id: str | None = None) -> list[Attempt]: ...
