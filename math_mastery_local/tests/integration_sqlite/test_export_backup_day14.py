from pathlib import Path

from application.use_cases.backup_db import backup_database
from application.use_cases.export_reports import export_attempts_csv, export_mastery_csv
from application.use_cases.seed_data import seed_items, seed_topics
from application.use_cases.session_summary import get_session_summary
from application.use_cases.submit_attempt import submit_attempt
from infrastructure.persistence_sqlite.db import DB_NAME, init_db


def test_export_backup_and_summary_workflow():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()
    seed_topics(root / "data/topics.csv")
    seed_items()

    # create some attempt history for summary/export checks
    submit_attempt("T001", True, 0.2)
    submit_attempt("T001", False, 0.2)

    reports_dir = root / "outputs" / "reports"
    backups_dir = root / "outputs" / "backups"

    mastery_file = export_mastery_csv(reports_dir)
    attempts_file = export_attempts_csv(reports_dir, limit=100)
    backup_file = backup_database(root, backups_dir)
    summary = get_session_summary(recent_n=50)

    assert mastery_file.exists()
    assert attempts_file.exists()
    assert backup_file.exists()
    assert summary["attempts"] >= 2
    assert 0.0 <= summary["accuracy"] <= 1.0
