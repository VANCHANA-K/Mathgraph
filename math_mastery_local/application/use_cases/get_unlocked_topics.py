from domain.services.progression_engine import ProgressionEngine


def get_unlocked_topics(graph_repo, mastery_repo):
    engine = ProgressionEngine(graph_repo, mastery_repo)
    return engine.get_unlocked_topics()
