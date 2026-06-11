"""Build a NetworkX knowledge graph from the generated CSV files.

Produces a GraphML file and a triples CSV for downstream consumption by
the QA and visualisation modules.
"""

import csv
from pathlib import Path
from typing import Any

import networkx as nx

from src.config import DATA_DIR, GRAPH_PATH, TRIPLES_PATH

CUSTOMER_NODE_TYPE = "Customer"
AGENT_NODE_TYPE = "Agent"
CONVERSATION_NODE_TYPE = "Conversation"


def _read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as a list of dicts.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist, with a hint to run ``generate-data`` first.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Required CSV not found: {path}\n"
            "Run 'python -m src generate-data' first."
        )
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def _node_attrs(row: dict[str, str], id_key: str) -> dict[str, str]:
    """Return *row* without the primary-key field *id_key*."""
    return {k: v for k, v in row.items() if k != id_key}


def build_graph() -> nx.MultiDiGraph:
    """Read CSVs and construct the knowledge graph.

    Returns the graph and persists it as GraphML + triples CSV.
    """
    customers = _read_csv(DATA_DIR / "customers.csv")
    agents = _read_csv(DATA_DIR / "agents.csv")
    conversations = _read_csv(DATA_DIR / "conversations.csv")

    graph = nx.MultiDiGraph()

    for customer in customers:
        graph.add_node(
            f"cust:{customer['customer_id']}",
            type=CUSTOMER_NODE_TYPE,
            **_node_attrs(customer, "customer_id"),
        )

    for agent in agents:
        graph.add_node(
            f"agent:{agent['agent_id']}",
            type=AGENT_NODE_TYPE,
            **_node_attrs(agent, "agent_id"),
        )

    for conv in conversations:
        conv_id = f"conv:{conv['conversation_id']}"
        cust_id = f"cust:{conv['customer_id']}"
        agent_id = f"agent:{conv['agent_id']}"

        graph.add_node(
            conv_id,
            type=CONVERSATION_NODE_TYPE,
            **_node_attrs(conv, "conversation_id"),
        )
        graph.add_edge(cust_id, conv_id, relation="placed_call")
        graph.add_edge(conv_id, cust_id, relation="about_customer")
        graph.add_edge(agent_id, conv_id, relation="handled_call")
        graph.add_edge(conv_id, agent_id, relation="handled_by")

        if int(conv["transfer_count"]) > 0:
            graph.nodes[conv_id]["transferred"] = True

    nx.write_graphml(graph, GRAPH_PATH)
    _save_triples(graph)
    print(
        f"Graph built with {graph.number_of_nodes()} nodes "
        f"and {graph.number_of_edges()} edges."
    )
    print(f"Saved graph to {GRAPH_PATH}")
    return graph


def _save_triples(graph: nx.MultiDiGraph) -> None:
    """Persist every edge as a (subject, predicate, object) triple."""
    triples: list[dict[str, str]] = []
    for source, target, data in graph.edges(data=True):
        triples.append(
            {
                "subject": source,
                "predicate": data.get("relation", "related_to"),
                "object": target,
            }
        )

    fieldnames = ["subject", "predicate", "object"]
    with open(TRIPLES_PATH, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(triples)
    print(f"Saved triples file to {TRIPLES_PATH}")


def load_graph() -> nx.MultiDiGraph:
    """Load the persisted GraphML file.

    Raises
    ------
    FileNotFoundError
        If the graph file has not been created yet, with a hint to run
        ``build-graph`` first.
    """
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"Graph file not found: {GRAPH_PATH}\n"
            "Run 'python -m src build-graph' first."
        )
    return nx.read_graphml(GRAPH_PATH)


def graph_facts(graph: nx.MultiDiGraph) -> list[str]:
    """Flatten the graph into human-readable fact strings for the QA module."""
    facts: list[str] = []
    for node_id, attrs in graph.nodes(data=True):
        properties = ", ".join(
            f"{k}={v}" for k, v in attrs.items() if k != "type"
        )
        facts.append(f"Node {node_id} ({attrs.get('type')}): {properties}")

    for source, target, data in graph.edges(data=True):
        facts.append(f"Edge {source} -[{data.get('relation')}]-> {target}")

    return facts


if __name__ == "__main__":
    build_graph()
