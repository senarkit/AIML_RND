import csv
from pathlib import Path
import networkx as nx

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
GRAPH_PATH = DATA_DIR / "knowledge_graph.graphml"
TRIPLES_PATH = DATA_DIR / "knowledge_graph_triples.csv"

CUSTOMER_NODE_TYPE = "Customer"
AGENT_NODE_TYPE = "Agent"
CONVERSATION_NODE_TYPE = "Conversation"


def _read_csv(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def build_graph():
    customers = _read_csv(DATA_DIR / "customers.csv")
    agents = _read_csv(DATA_DIR / "agents.csv")
    conversations = _read_csv(DATA_DIR / "conversations.csv")

    graph = nx.MultiDiGraph()

    for customer in customers:
        graph.add_node(
            f"cust:{customer['customer_id']}",
            type=CUSTOMER_NODE_TYPE,
            **{k: customer[k] for k in customer if k != "customer_id"},
        )

    for agent in agents:
        graph.add_node(
            f"agent:{agent['agent_id']}",
            type=AGENT_NODE_TYPE,
            **{k: agent[k] for k in agent if k != "agent_id"},
        )

    for conv in conversations:
        graph.add_node(
            f"conv:{conv['conversation_id']}",
            type=CONVERSATION_NODE_TYPE,
            **{k: conv[k] for k in conv if k != "conversation_id"},
        )
        graph.add_edge(f"cust:{conv['customer_id']}", f"conv:{conv['conversation_id']}", relation="placed_call")
        graph.add_edge(f"conv:{conv['conversation_id']}", f"cust:{conv['customer_id']}", relation="about_customer")
        graph.add_edge(f"agent:{conv['agent_id']}", f"conv:{conv['conversation_id']}", relation="handled_call")
        graph.add_edge(f"conv:{conv['conversation_id']}", f"agent:{conv['agent_id']}", relation="handled_by")

        if int(conv["transfer_count"]) > 0:
            graph.nodes[f"conv:{conv['conversation_id']}"]["transferred"] = True
    nx.write_graphml(graph, GRAPH_PATH)
    _save_triples(graph)
    print(f"Graph built with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
    print(f"Saved graph to {GRAPH_PATH}")
    return graph


def _save_triples(graph):
    triples = []
    for source, target, data in graph.edges(data=True):
        triples.append({"subject": source, "predicate": data.get("relation", "related_to"), "object": target})

    fieldnames = ["subject", "predicate", "object"]
    with open(TRIPLES_PATH, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(triples)
    print(f"Saved triples file to {TRIPLES_PATH}")


def load_graph():
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(f"Graph file not found: {GRAPH_PATH}")
    return nx.read_graphml(GRAPH_PATH)


def graph_facts(graph):
    facts = []
    for node_id, attrs in graph.nodes(data=True):
        entry = f"Node {node_id} ({attrs.get('type')}): "
        properties = ", ".join(f"{k}={v}" for k, v in attrs.items() if k != "type")
        entry += properties
        facts.append(entry)
    for source, target, data in graph.edges(data=True):
        facts.append(f"Edge {source} -[{data.get('relation')}]-> {target}")
    return facts


if __name__ == "__main__":
    build_graph()
