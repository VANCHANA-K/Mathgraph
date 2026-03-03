from domain.services.session_builder import SessionBuilder


class FakeItemRepo:
    def __init__(self):
        self.items = {
            "T001": [("Q1", "T001", "q", "12", 0.2)],
            "T003": [("Q2", "T003", "q", "24", 0.3)],
            "T010": [("Q3", "T010", "q", "1", 0.4)],
            "T030": [("Q4", "T030", "q", "4", 0.5)],
        }

    def get_items_by_topic(self, topic_id):
        return self.items.get(topic_id, [])


def test_session_builder_returns_items_with_topic_id_shape():
    builder = SessionBuilder(FakeItemRepo())
    actions = {
        "review": ["T001"],
        "remediate": ["T003"],
        "new": ["T010", "T030"],
    }

    session = builder.build_session(actions, total_questions=15)

    assert all(len(item) == 5 for item in session["review"])
    assert all(len(item) == 5 for item in session["remediate"])
    assert all(len(item) == 5 for item in session["new"])
