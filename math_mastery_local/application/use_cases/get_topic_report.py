
def get_topic_report(user_id: str, topic_repo, mastery_repo) -> list[dict]:
    states = {s.topic_id: s for s in mastery_repo.list_states(user_id)}
    report = []
    for topic in topic_repo.list_topics():
        st = states.get(topic.topic_id)
        report.append(
            {
                "topic_id": topic.topic_id,
                "topic_name": topic.name,
                "mastery": round(st.mastery, 3) if st else 0.0,
                "stability": round(st.stability, 2) if st else 1.0,
                "due_at": st.due_at.isoformat() if st and st.due_at else "-",
            }
        )
    return report
