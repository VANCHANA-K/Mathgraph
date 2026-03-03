from domain.services.progression_engine import ProgressionEngine


class FakeGraphRepo:
    def __init__(self):
        self.prereq_map = {
            "T001": [],
            "T003": ["T001"],
            "T010": ["T003"],
        }

    def get_prerequisites(self, topic_id):
        return self.prereq_map.get(topic_id, [])

    def get_all_topics(self):
        return list(self.prereq_map.keys())


class FakeMasteryRepo:
    def __init__(self, mastery_map):
        self.mastery_map = mastery_map

    def get_mastery(self, topic_id):
        return self.mastery_map.get(topic_id, 0.0), 1.0


def test_root_topic_is_always_unlocked():
    engine = ProgressionEngine(FakeGraphRepo(), FakeMasteryRepo({}))
    assert engine.is_unlocked("T001") is True


def test_topic_locked_when_prerequisite_below_threshold():
    engine = ProgressionEngine(FakeGraphRepo(), FakeMasteryRepo({"T001": 0.84}))
    assert engine.is_unlocked("T003") is False


def test_topic_unlocks_when_all_prerequisites_meet_threshold():
    engine = ProgressionEngine(FakeGraphRepo(), FakeMasteryRepo({"T001": 0.85, "T003": 0.9}))
    assert engine.is_unlocked("T003") is True
    assert engine.is_unlocked("T010") is True
