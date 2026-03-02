import csv

from domain.entities.topic import Topic


class CsvTopicRepository:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def list_topics(self) -> list[Topic]:
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            return [Topic(r["topic_id"], r["name"], r.get("description", "")) for r in csv.DictReader(f)]

    def get_topic(self, topic_id: str) -> Topic | None:
        for topic in self.list_topics():
            if topic.topic_id == topic_id:
                return topic
        return None
