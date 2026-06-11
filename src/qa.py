"""Retrieval-based Question Answering over the knowledge graph.

Supports three backends in order of preference:
1. OpenAI ``>=1.0`` chat completions (if ``OPENAI_API_KEY`` is set).
2. HuggingFace ``transformers`` text-generation pipeline (local GPT-2).
3. Raw retrieval-only output (no LLM).
"""

import os
import re
import sys

try:
    from openai import OpenAI  # openai >= 1.0
except ImportError:
    OpenAI = None  # type: ignore[assignment,misc]

try:
    from transformers import pipeline as hf_pipeline, set_seed  # type: ignore[import-untyped]
except ImportError:
    hf_pipeline = None  # type: ignore[assignment]

from src.config import OPENAI_MODEL
from src.graph_builder import build_graph, graph_facts, load_graph

# Common English stop-words to ignore during keyword scoring
_STOP_WORDS: frozenset[str] = frozenset(
    {
        "a", "an", "the", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "shall", "should", "may", "might", "can", "could",
        "of", "in", "to", "for", "with", "on", "at", "from", "by",
        "about", "as", "into", "through", "during", "before", "after",
        "and", "but", "or", "nor", "not", "no", "so", "if", "then",
        "than", "too", "very", "just", "that", "this", "it", "its",
        "what", "which", "who", "whom", "how", "when", "where", "why",
    }
)


def _clean_text(text: str) -> str:
    """Collapse whitespace in *text* to single spaces."""
    return re.sub(r"\s+", " ", text.strip())


def _simple_retrieval(
    question: str, facts: list[str], top_n: int = 8
) -> list[str]:
    """Return the *top_n* facts most relevant to *question*.

    Scoring is a simple keyword overlap count, ignoring common stop-words
    so that high-frequency words don't drown real matches.
    """
    question_words = {
        w for w in question.lower().split() if w and w not in _STOP_WORDS
    }
    scored: list[tuple[int, str]] = []
    for fact in facts:
        fact_lower = fact.lower()
        score = sum(1 for word in question_words if word in fact_lower)
        if score > 0:
            scored.append((score, fact))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [fact for _, fact in scored[:top_n]]
    if not selected:
        selected = facts[: min(top_n, len(facts))]
    return selected


def _llm_answer(question: str, context: str) -> str:
    """Generate an answer using the best available LLM backend."""

    # --- OpenAI >= 1.0 ---------------------------------------------------
    api_key = os.getenv("OPENAI_API_KEY")
    if OpenAI is not None and api_key:
        client = OpenAI(api_key=api_key)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a precise knowledge-graph assistant. "
                    "Use only the provided context to answer."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ]
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    # --- Local transformers fallback -------------------------------------
    if hf_pipeline is not None:
        gen = hf_pipeline(
            "text-generation",
            model="gpt2",
            truncation=True,
        )
        set_seed(42)
        prompt = (
            "Use only the facts below to answer the question without "
            "inventing new information.\n"
            f"Facts:\n{context}\n"
            f"Question: {question}\n"
            "Answer:"
        )
        result = gen(prompt, max_new_tokens=150, num_return_sequences=1)
        return _clean_text(result[0]["generated_text"][len(prompt):].strip())

    # --- Retrieval-only (no LLM) -----------------------------------------
    return f"[retrieval-only answer]\n{context}\nQuestion: {question}"


def answer_question(question: str) -> str:
    """Load the knowledge graph and answer *question*.

    Attempts to load the persisted graph; falls back to building it when
    the GraphML file is not found.
    """
    try:
        graph = load_graph()
    except FileNotFoundError:
        print("Graph file not found — building graph now…")
        graph = build_graph()

    facts = graph_facts(graph)
    relevant = _simple_retrieval(question, facts)
    context = "\n".join(relevant)
    return _llm_answer(question, context)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python -m src.qa "Your question"')
        sys.exit(1)

    question_text = sys.argv[1]
    print(answer_question(question_text))
