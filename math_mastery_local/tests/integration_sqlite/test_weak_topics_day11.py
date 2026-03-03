from pathlib import Path

from domain.services.weak_node_detector import WeakNodeDetector
from infrastructure.persistence_sqlite.attempt_repo import AttemptRepository, save_attempt
from infrastructure.persistence_sqlite.db import DB_NAME, init_db


def test_weak_topics_detection_from_recent_attempts():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()

    save_attempt("T001", False)
    save_attempt("T001", False)
    save_attempt("T001", True)

    save_attempt("T003", True)
    save_attempt("T003", True)
    save_attempt("T003", False)

    detector = WeakNodeDetector(AttemptRepository())
    weak_topics = detector.get_weak_topics(threshold=0.5, min_attempts=3)

    assert "T001" in weak_topics
    assert "T003" not in weak_topics
