import csv

from domain.entities.topic import Topic


class CsvTopicRepository:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def list_topics(self) -> list[Topic]:
        topics: list[Topic] = []
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                topic_id = r.get("topic_id") or r.get("id")
                name = r.get("name") or r.get("title") or ""
                description = r.get("description") or f"{r.get('domain', '')} L{r.get('level', '')}".strip()
                if topic_id:
                    topics.append(Topic(topic_id=topic_id, name=name, description=description))
        return topics

    def get_topic(self, topic_id: str) -> Topic | None:
        for topic in self.list_topics():
            if topic.topic_id == topic_id:
                return topic
        return None
