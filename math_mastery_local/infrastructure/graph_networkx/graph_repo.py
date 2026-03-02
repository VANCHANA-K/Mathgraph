import csv
from collections import defaultdict


class NetworkXGraphRepository:
    """In-memory graph adapter with the same role as a networkx-backed repository."""

    def __init__(self, edges_csv_path: str):
        self._prereq = defaultdict(list)
        self._children = defaultdict(list)
        with open(edges_csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                prereq = row["prereq_topic_id"]
                topic = row["topic_id"]
                self._prereq[topic].append(prereq)
                self._children[prereq].append(topic)

    def prerequisites_of(self, topic_id: str) -> list[str]:
        return list(self._prereq.get(topic_id, []))

    def children_of(self, topic_id: str) -> list[str]:
        return list(self._children.get(topic_id, []))
