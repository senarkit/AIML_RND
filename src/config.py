"""Shared configuration for the knowledge-graph pipeline.

All path constants and tuneable settings live here so every module
imports from a single source of truth.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_PATH: Path = DATA_DIR / "knowledge_graph.graphml"
TRIPLES_PATH: Path = DATA_DIR / "knowledge_graph_triples.csv"
HTML_PATH: Path = DATA_DIR / "graph.html"

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_SEED: int = 42

# ---------------------------------------------------------------------------
# OpenAI / LLM settings
# ---------------------------------------------------------------------------
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
