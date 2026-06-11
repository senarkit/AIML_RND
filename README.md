# Test Runs Knowledge Graph Prototype

This project simulates a BigQuery + Spanner Graph workflow using CSV data and a Python pipeline.

## Overview

1. Generate synthetic customer, conversation, and agent CSV data.
2. Build an in-memory knowledge graph from those CSV files.
3. Visualize the graph as an interactive HTML file.
4. Query the graph with a retrieval-based QA flow and optionally use an LLM to produce answers.

## Getting Started

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Generate the data and build the graph:

```bash
python -m src.main generate-data
python -m src.main build-graph
python -m src.main visualize
```

3. Ask a question:

```bash
python -m src.main qa "What type of account does customer 1001 have?"
```

## Notes

- This code uses CSV files in `data/` instead of BigQuery.
- The knowledge graph is stored as a NetworkX graph and serialized into `data/knowledge_graph_triples.csv`.
- If `OPENAI_API_KEY` is set, the QA flow will use OpenAI. Otherwise it falls back to a local lightweight model.
