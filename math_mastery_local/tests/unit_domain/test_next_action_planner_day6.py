from datetime import datetime, timedelta

from domain.services.next_action_planner import NextActionPlanner


class FakeGraphRepo:
    def __init__(self):
        self.edges = {
            "T001": ["T003"],
            "T003": ["T010"],
            "T010": [],
            "T020": [],
        }

    def get_children(self, topic_id):
        return self.edges.get(topic_id, [])

    def get_prerequisites(self, topic_id):
        prereqs = []
        for src, children in self.edges.items():
            if topic_id in children:
                prereqs.append(src)
        return prereqs

    def get_all_topics(self):
        return list(self.edges.keys())


class FakeMasteryRepo:
    def __init__(self, mastery_map, all_rows):
        self.mastery_map = mastery_map
        self.all_rows = all_rows

    def get_mastery(self, topic_id):
        return self.mastery_map.get(topic_id, 0.0), 1.0

    def get_all_mastery(self):
        return self.all_rows


def test_next_action_groups_cover_review_remediate_and_new():
    now = datetime.now()
    rows = [
        ("T001", 0.3, 1.0, (now - timedelta(days=1)).isoformat()),
        ("T003", 0.4, 1.0, None),
        ("T010", 0.9, 1.0, None),
    ]
    mastery_map = {
        "T001": 0.9,
        "T003": 0.4,
        "T010": 0.0,
        "T020": 0.0,
    }

    planner = NextActionPlanner(FakeGraphRepo(), FakeMasteryRepo(mastery_map, rows))

    assert "T001" in planner.get_review_topics()
    assert "T003" in planner.get_remediate_topics()
    assert "T020" in planner.get_new_topics()
