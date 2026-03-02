import os
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from application.use_cases.generate_session import generate_session
from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.get_topic_report import get_topic_report
from application.use_cases.submit_attempt import submit_attempt
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.attempt_repo import SqliteAttemptRepository
from infrastructure.persistence_sqlite.db import connect, init_schema
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.mastery_repo import SqliteMasteryRepository
from infrastructure.persistence_sqlite.topic_repo import CsvTopicRepository

DB_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "math_mastery.db"))
USER_ID = os.getenv("DEFAULT_USER_ID", "local_user")

conn = connect(DB_PATH)
init_schema(conn)
topic_repo = CsvTopicRepository(str(BASE_DIR / "data/topics.csv"))
graph_repo = NetworkXGraphRepository(str(BASE_DIR / "data/edges.csv"))
item_repo = SqliteItemRepository(conn)
attempt_repo = SqliteAttemptRepository(conn)
mastery_repo = SqliteMasteryRepository(conn)

st.title("Math Mastery Local MVP")

if st.button("Start session"):
    actions = get_next_actions(USER_ID, topic_repo, graph_repo, mastery_repo)
    session = generate_session(actions, minutes=20)
    st.session_state["session_topics"] = session["topics"]
    st.write("Session plan:", session)

st.subheader("Do one problem")
all_topics = topic_repo.list_topics()
topic_id = st.selectbox("Topic", [t.topic_id for t in all_topics])
items = item_repo.list_items_by_topic(topic_id)
if items:
    item = items[0]
    st.write(item.question)
    is_correct = st.checkbox("Mark as correct")
    response_seconds = st.slider("Response seconds", 5, 180, 60)
    used_hint = st.checkbox("Used hint")
    if st.button("Submit attempt"):
        state = submit_attempt(
            USER_ID,
            item.item_id,
            topic_id,
            is_correct,
            response_seconds,
            used_hint,
            attempt_repo,
            mastery_repo,
        )
        st.success(f"Updated mastery={state.mastery:.2f}, due={state.due_at}")
else:
    st.warning("No items for this topic. Run seed first.")

st.subheader("Progress graph")
report = get_topic_report(USER_ID, topic_repo, mastery_repo)
st.dataframe(report)
