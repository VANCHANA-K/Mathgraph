import sys
from pathlib import Path

import streamlit as st

base_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_path))

from application.use_cases.generate_session import generate_session
from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items, seed_topics
from application.use_cases.submit_attempt import submit_attempt
from domain.services.graph_intelligence import GraphIntelligence
from domain.services.weak_node_detector import WeakNodeDetector
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.attempt_repo import AttemptRepository
from infrastructure.persistence_sqlite.db import init_db
from infrastructure.persistence_sqlite.item_repo import ItemRepository
from infrastructure.persistence_sqlite.mastery_repo import MasteryRepository


topics_path = base_path / "data" / "topics.csv"
edges_path = base_path / "data" / "edges.csv"

init_db()
seed_topics(topics_path)
seed_items()

graph_repo = NetworkXGraphRepository(topics_path, edges_path)
mastery_repo = MasteryRepository()
item_repo = ItemRepository()
attempt_repo = AttemptRepository()

if "session" not in st.session_state:
    st.session_state.session = None
if "index" not in st.session_state:
    st.session_state.index = 0
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None
if "last_mastery" not in st.session_state:
    st.session_state.last_mastery = None
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "adaptive_note" not in st.session_state:
    st.session_state.adaptive_note = None

st.title("📚 Math Mastery System (Local MVP)")

if st.button("Start Session"):
    actions = get_next_actions(graph_repo, mastery_repo)
    session = generate_session(actions, item_repo)
    all_items = session["review"] + session["remediate"] + session["new"]

    st.session_state.session = all_items
    st.session_state.index = 0
    st.session_state.streak = 0
    st.session_state.last_feedback = None
    st.session_state.last_mastery = None
    st.session_state.adaptive_note = None

if st.session_state.session:
    if st.session_state.last_feedback:
        kind, message = st.session_state.last_feedback
        if kind == "success":
            st.success(message)
        else:
            st.error(message)
    if st.session_state.last_mastery:
        st.write(st.session_state.last_mastery)
    if st.session_state.adaptive_note:
        note_kind, note_message = st.session_state.adaptive_note
        if note_kind == "warning":
            st.warning(note_message)
        else:
            st.success(note_message)

    idx = st.session_state.index
    session = st.session_state.session

    if idx < len(session):
        item_id, topic_id, question, correct_answer, difficulty = session[idx]

        st.subheader(f"Question {idx + 1}")
        st.write(question)

        answer = st.text_input("Your answer", key=f"ans_{idx}")

        if st.button("Submit", key=f"btn_{idx}"):
            is_correct = answer.strip() == str(correct_answer).strip()

            before, after, due_at = submit_attempt(
                topic_id=topic_id,
                correct=is_correct,
                difficulty=difficulty,
            )

            if is_correct:
                st.session_state.last_feedback = ("success", "Correct!")
                st.session_state.streak += 1
            else:
                st.session_state.last_feedback = (
                    "error",
                    f"Wrong! Correct answer: {correct_answer}",
                )
                st.session_state.streak -= 1

            st.session_state.last_mastery = (
                f"Mastery: {round(before, 3)} → {round(after, 3)} | Next review: {due_at}"
            )

            # Adaptive pivot heuristics
            if st.session_state.streak <= -2:
                st.session_state.adaptive_note = ("warning", "⚠ Switching to remediate topic")
                st.session_state.index += 1
                st.session_state.streak = 0
            elif st.session_state.streak >= 3:
                st.session_state.adaptive_note = ("success", "🚀 Increasing difficulty")
                st.session_state.streak = 0
                st.session_state.index += 1
            else:
                st.session_state.adaptive_note = None
                st.session_state.index += 1

            st.rerun()
    else:
        st.success("🎉 Session Completed!")
        if st.button("Start New Session"):
            st.session_state.session = None
            st.session_state.index = 0
            st.session_state.last_feedback = None
            st.session_state.last_mastery = None
            st.session_state.streak = 0
            st.session_state.adaptive_note = None
            st.rerun()
else:
    st.info("Click **Start Session** to begin.")

st.divider()
st.header("📊 Mastery Dashboard")

rows = mastery_repo.get_all_mastery()

if rows:
    for topic_id, mastery, stability, due_at in rows:
        st.write(
            f"{topic_id} | Mastery: {round(mastery, 2)} | Stability: {round(stability, 2)}"
        )
else:
    st.write("No mastery data yet.")


st.divider()
st.header("📈 Learning Velocity")

recent = attempt_repo.get_recent_attempts()

if recent:
    total = len(recent)
    correct = sum([r[1] for r in recent])
    accuracy = correct / total

    st.write(f"Recent Accuracy: {round(accuracy * 100, 1)}%")
    st.write(f"Attempts: {total}")
else:
    st.write("No recent data")

st.divider()
st.header("⚠ Weak Topics")

detector = WeakNodeDetector(attempt_repo)
weak_topics = detector.get_weak_topics()

if weak_topics:
    st.write(weak_topics)
else:
    st.write("No weak topics detected.")


st.divider()
st.header("🧭 Curriculum Intelligence")

intelligence = GraphIntelligence(graph_repo, mastery_repo)
bottlenecks = intelligence.get_bottlenecks()
central = intelligence.get_central_topics()

st.subheader("⚠ Bottleneck Topics")
if bottlenecks:
    for node, downstream in bottlenecks:
        st.write(f"{node} (blocking {downstream} topics)")
else:
    st.write("No major bottlenecks.")

st.subheader("⭐ High Importance Topics")
for node in central:
    st.write(node)

st.divider()
st.header("🧠 Knowledge Graph")

plotly_available = __import__("importlib").util.find_spec("plotly") is not None
if plotly_available:
    from infrastructure.graph_networkx.graph_visualizer import generate_graph_figure

    fig = generate_graph_figure(graph_repo, mastery_repo)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Plotly is not installed in this environment, so graph visualization is unavailable.")
