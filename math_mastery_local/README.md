# math_mastery_local

Local-first Mastery Learning MVP (Clean Architecture)

## Project Structure

```bash
math_mastery_local/
├─ app/
├─ domain/
│  ├─ entities/
│  ├─ services/
│  └─ ports/
├─ application/
│  └─ use_cases/
├─ infrastructure/
│  ├─ persistence_sqlite/
│  └─ graph_networkx/
├─ data/
├─ outputs/
│  ├─ reports/
│  └─ backups/
└─ tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run (Local)

```bash
# path: math_mastery_local/
streamlit run app/ui_streamlit.py
```

## Outputs

- `outputs/reports/` : mastery and attempts exports (CSV)
- `outputs/backups/` : SQLite database backups
- database file: `mastery.db`

## Day 3 readiness

- SQLite schema includes: `topics`, `items`, `attempts`, `mastery_state`.
- CLI seeds DB (`python app/cli.py`) by running init + topic/item seed.
