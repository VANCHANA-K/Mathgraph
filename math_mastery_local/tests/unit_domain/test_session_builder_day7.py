from domain.services.session_builder import SessionBuilder


class FakeItemRepo:
    def __init__(self):
        self.items = {
            "T001": [("Q1", "q", 0.2)],
            "T003": [("Q2", "q", 0.3)],
            "T010": [("Q3", "q", 0.4)],
            "T030": [("Q4", "q", 0.5)],
        }

    def get_items_by_topic(self, topic_id):
        return self.items.get(topic_id, [])


def test_session_builder_uses_40_30_30_split():
    builder = SessionBuilder(FakeItemRepo())
    actions = {
        "review": ["T001"],
        "remediate": ["T003"],
        "new": ["T010", "T030"],
    }

    session = builder.build_session(actions, total_questions=15)

    assert len(session["review"]) == 6
    assert len(session["remediate"]) == 4
    assert len(session["new"]) == 5
