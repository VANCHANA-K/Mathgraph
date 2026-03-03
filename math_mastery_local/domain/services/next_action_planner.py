from datetime import datetime


class NextActionPlanner:
    def __init__(self, graph_repo, mastery_repo):
        self.graph = graph_repo
        self.mastery_repo = mastery_repo

    def get_review_topics(self):
        review = []
        rows = self.mastery_repo.get_all_mastery()

        for topic_id, mastery, stability, due_at in rows:
            if due_at:
                due_time = datetime.fromisoformat(due_at)
                if due_time <= datetime.now():
                    review.append(topic_id)

        return review

    def get_remediate_topics(self):
        remediate = []
        rows = self.mastery_repo.get_all_mastery()

        for topic_id, mastery, stability, _ in rows:
            if mastery < 0.5:
                children = self.graph.get_children(topic_id)
                for child in children:
                    prereqs = self.graph.get_prerequisites(child)
                    if topic_id in prereqs:
                        remediate.append(topic_id)
                        break

        return remediate

    def get_new_topics(self):
        new_topics = []

        for topic_id in self.graph.get_all_topics():
            prereqs = self.graph.get_prerequisites(topic_id)

            unlocked = True
            for prereq_topic_id in prereqs:
                mastery, _ = self.mastery_repo.get_mastery(prereq_topic_id)
                if mastery < 0.85:
                    unlocked = False
                    break

            mastery, _ = self.mastery_repo.get_mastery(topic_id)
            if unlocked and mastery < 0.2:
                new_topics.append(topic_id)

        return new_topics
