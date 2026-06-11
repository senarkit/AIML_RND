from pathlib import Path
from pyvis.network import Network

from src.graph_builder import load_graph

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HTML_PATH = DATA_DIR / "graph.html"

NODE_COLORS = {
    "Customer": "#1f77b4",
    "Agent": "#2ca02c",
    "Conversation": "#ff7f0e",
}


def create_visualization():
    graph = load_graph()
    net = Network(height="850px", width="100%", notebook=False)
    net.toggle_physics(True)

    for node_id, attrs in graph.nodes(data=True):
        label = node_id.split(":", 1)[1]
        title = "<br>".join(f"{k}: {v}" for k, v in attrs.items())
        net.add_node(node_id, label=label, title=title, color=NODE_COLORS.get(attrs.get("type"), "#888"))

    for source, target, data in graph.edges(data=True):
        net.add_edge(source, target, title=data.get("relation"), label=data.get("relation"))

    net.show(HTML_PATH)
    print(f"Visualization saved to {HTML_PATH}")
    return HTML_PATH


if __name__ == "__main__":
    create_visualization()
