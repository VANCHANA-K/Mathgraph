from datetime import datetime
from pathlib import Path
import shutil

from infrastructure.persistence_sqlite.db import DB_NAME


def backup_database(project_root: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = project_root / DB_NAME
    dst = backup_dir / f"{DB_NAME.replace('.db', '')}_{ts}.db"
    shutil.copy2(src, dst)
    return dst
