"""Interactive HTML visualisation of the knowledge graph using PyVis."""

from pathlib import Path

from pyvis.network import Network

from src.config import HTML_PATH
from src.graph_builder import load_graph

NODE_COLORS: dict[str, str] = {
    "Customer": "#1f77b4",
    "Agent": "#2ca02c",
    "Conversation": "#ff7f0e",
}


def create_visualization() -> Path:
    """Build a PyVis HTML visualisation and write it to ``HTML_PATH``.

    Returns the path to the generated HTML file.
    """
    graph = load_graph()
    net = Network(height="850px", width="100%", notebook=False)
    net.toggle_physics(True)

    for node_id, attrs in graph.nodes(data=True):
        label = node_id.split(":", 1)[1]
        title = "<br>".join(f"{k}: {v}" for k, v in attrs.items())
        color = NODE_COLORS.get(attrs.get("type", ""), "#888")
        net.add_node(node_id, label=label, title=title, color=color)

    for source, target, data in graph.edges(data=True):
        relation = data.get("relation", "")
        net.add_edge(source, target, title=relation, label=relation)

    # write_html works across modern PyVis versions (net.show is deprecated)
    net.write_html(str(HTML_PATH))
    print(f"Visualization saved to {HTML_PATH}")
    return HTML_PATH


if __name__ == "__main__":
    create_visualization()
