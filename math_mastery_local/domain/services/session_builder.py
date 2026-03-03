import random


class SessionBuilder:
    def __init__(self, item_repo):
        self.item_repo = item_repo

    def build_session(self, actions, total_questions=15):
        review_n = int(total_questions * 0.4)
        remediate_n = int(total_questions * 0.3)
        new_n = total_questions - review_n - remediate_n

        session = {
            "review": [],
            "remediate": [],
            "new": [],
        }

        def pick_items(topics, n):
            items = []
            for topic_id in topics:
                topic_items = self.item_repo.get_items_by_topic(topic_id)
                items.extend(topic_items)

            if not items or n <= 0:
                return []

            random.shuffle(items)
            if len(items) >= n:
                return items[:n]

            # Not enough unique items: cycle so we can still fill a full session.
            picked = []
            while len(picked) < n:
                picked.extend(items)
            return picked[:n]

        session["review"] = pick_items(actions.get("review", []), review_n)
        session["remediate"] = pick_items(actions.get("remediate", []), remediate_n)
        session["new"] = pick_items(actions.get("new", []), new_n)

        return session
