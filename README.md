# Test Runs Knowledge Graph Prototype

This project simulates a BigQuery + Spanner workflow using CSV data and a Python pipeline.

## Overview

The project includes three main stages:

1. Generate synthetic customer, agent, and conversation CSV data in `data/`.
2. Build a NetworkX knowledge graph from those CSV files and serialize it to `data/knowledge_graph.graphml` and `data/knowledge_graph_triples.csv`.
3. Visualize the graph as an HTML page and query it using a simple retrieval-based QA flow.

## Requirements

- Python 3.10+ recommended
- `requirements.txt` includes dependencies: `pandas`, `networkx`, `pyvis`, `python-dotenv`, `openai`, `transformers`

## Setup

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows (PowerShell):** `.\\venv\\Scripts\\Activate.ps1`
- **macOS / Linux:** `source venv/bin/activate`

Then install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## How to Run

Run commands from the repository root.

1. Generate synthetic CSV data:

```bash
python -m src generate-data
```

You can optionally pass `--seed <N>` to override the random seed.

2. Build the knowledge graph from the generated CSV files:

```bash
python -m src build-graph
```

3. Create an interactive graph visualization:

```bash
python -m src visualize
```

Open `data/graph.html` in a browser after this completes.

4. Query the graph using QA:

```bash
python -m src qa "What type of account does customer 1001 have?"
```

Add `-v` or `--verbose` to any command for debug logging.

## Optional Configuration

- `OPENAI_API_KEY`: If set, the QA flow will use OpenAI via the `openai` package (requires `openai>=1.0`).
- `OPENAI_MODEL`: Optional model name, default is `gpt-3.5-turbo`.

If OpenAI is unavailable, the code falls back to a local `transformers` text-generation pipeline or a retrieval-only answer.

## Data Files

All generated files are placed in `data/` and are git-ignored since they can be reproduced:

- `data/customers.csv`
- `data/agents.csv`
- `data/conversations.csv`
- `data/knowledge_graph.graphml`
- `data/knowledge_graph_triples.csv`
- `data/graph.html`
