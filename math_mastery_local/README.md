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
│  └─ reports/
└─ tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app/cli.py seed
streamlit run app/ui_streamlit.py
```

## Day 1 Definition of Done

- [x] Folder structure created
- [x] Virtual environment command documented
- [ ] `pip install -r requirements.txt` completed in local machine
- [x] `README.md` + `.gitignore` prepared
