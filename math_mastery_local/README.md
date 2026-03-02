# Math Mastery Local MVP

Local-first MVP for practicing math with topic mastery, prerequisites, and spaced review.

## Run

```bash
cd math_mastery_local
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/cli.py seed
streamlit run app/ui_streamlit.py
```

## What is included

- Graph + unlock by prerequisites from CSV (`topics.csv`, `edges.csv`).
- Mastery state per topic (`mastery`, `stability`, `due_at`, `last_practiced_at`).
- Submit attempt flow updates mastery + due date.
- Next actions bucketed into `Review`, `Remediate`, `New`.
- Streamlit UI for start session, submit answer, and view report.
