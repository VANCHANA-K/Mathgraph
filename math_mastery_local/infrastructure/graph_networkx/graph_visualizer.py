import networkx as nx
import plotly.graph_objects as go


def generate_graph_figure(graph_repo, mastery_repo):
    graph = nx.DiGraph()

    for topic_id in graph_repo.get_all_topics():
        graph.add_node(topic_id)
        for child_id in graph_repo.get_children(topic_id):
            graph.add_edge(topic_id, child_id)

    pos = nx.spring_layout(graph, seed=42)

    mastery_dict = {}
    rows = mastery_repo.get_all_mastery()
    for topic_id, mastery, _, _ in rows:
        mastery_dict[topic_id] = mastery

    node_x = []
    node_y = []
    node_color = []
    node_text = []

    for node in graph.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        mastery = mastery_dict.get(node, None)

        if mastery is None:
            color = "lightgray"
        elif mastery >= 0.85:
            color = "green"
        elif mastery >= 0.5:
            color = "orange"
        else:
            color = "red"

        node_color.append(color)
        node_text.append(f"{node} (Mastery: {round(mastery or 0, 2)})")

    edge_x = []
    edge_y = []

    for src, dst in graph.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            size=15,
            color=node_color,
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
        ),
    )

    return fig
