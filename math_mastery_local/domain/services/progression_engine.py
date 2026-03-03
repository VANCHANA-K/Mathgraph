class ProgressionEngine:
    def __init__(self, graph_repo, mastery_repo):
        self.graph = graph_repo
        self.mastery_repo = mastery_repo

    def is_unlocked(self, topic_id):
        prereqs = self.graph.get_prerequisites(topic_id)

        if not prereqs:
            return True

        for prereq_topic_id in prereqs:
            mastery, _ = self.mastery_repo.get_mastery(prereq_topic_id)
            if mastery < 0.85:
                return False

        return True

    def get_unlocked_topics(self):
        unlocked = []

        for topic_id in self.graph.get_all_topics():
            if self.is_unlocked(topic_id):
                unlocked.append(topic_id)

        return unlocked
