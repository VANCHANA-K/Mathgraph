from typing import Protocol

from domain.entities.topic import Topic


class TopicRepository(Protocol):
    def list_topics(self) -> list[Topic]: ...
    def get_topic(self, topic_id: str) -> Topic | None: ...
