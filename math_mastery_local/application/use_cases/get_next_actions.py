from domain.services.next_action_planner import NextActionPlanner


def get_next_actions(graph_repo, mastery_repo):
    planner = NextActionPlanner(graph_repo, mastery_repo)

    return {
        "review": planner.get_review_topics(),
        "remediate": planner.get_remediate_topics(),
        "new": planner.get_new_topics(),
    }
