import os
import re
from pathlib import Path

try:
    import openai
except ImportError:
    openai = None

try:
    from transformers import pipeline, set_seed
except ImportError:
    pipeline = None

from src.graph_builder import build_graph, graph_facts, load_graph

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def _clean_text(text):
    return re.sub(r"\s+", " ", text.strip())


def _simple_retrieval(question, facts, top_n=8):
    question_lower = question.lower()
    scored = []
    for fact in facts:
        score = 0
        fact_lower = fact.lower()
        for word in set(question_lower.split()):
            if word and word in fact_lower:
                score += 1
        if score > 0:
            scored.append((score, fact))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [fact for _, fact in scored[:top_n]]
    if not selected:
        selected = facts[:min(top_n, len(facts))]
    return selected


def _llm_answer(question, context):
    if openai and os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.environ["OPENAI_API_KEY"]
        messages = [
            {"role": "system", "content": "You are a precise knowledge-graph assistant. Use only the provided context to answer."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]
        response = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages, max_tokens=300)
        return response.choices[0].message.content.strip()

    if pipeline is not None:
        gen = pipeline("text-generation", model="gpt2", max_length=250)
        set_seed(42)
        prompt = f"Use only the facts below to answer the question without inventing new information. Facts:\n{context}\nQuestion: {question}\nAnswer:"
        result = gen(prompt, num_return_sequences=1)
        return _clean_text(result[0]["generated_text"][len(prompt) :].strip())

    return f"[retrieval-only answer]\n{context}\nQuestion: {question}"


def answer_question(question, use_graph=True):
    if use_graph:
        graph = load_graph()
    else:
        graph = build_graph()
    facts = graph_facts(graph)
    relevant = _simple_retrieval(question, facts)
    context = "\n".join(relevant)
    answer = _llm_answer(question, context)
    return answer


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.qa \"Your question\"")
        sys.exit(1)

    question_text = sys.argv[1]
    print(answer_question(question_text))
