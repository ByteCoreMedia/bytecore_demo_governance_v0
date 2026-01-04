"""
mock_ordering.py — Demo-Safe Deterministic Ordering (v0.1)
-----------------------------------------------------------
This module provides a simplified and non-IP-derivative demonstration of
how an AI governance system might "order" or "rank" candidate outputs.

This does NOT implement the MIL ordering logic.
It does NOT reveal any ByteCore priority functions or graph logic.

It simply:
- Assigns a small set of fake scores
- Sorts candidates deterministically
- Returns the "winner" and a summary
"""

from datetime import datetime
import random

# ---------------------------------------------------------
# Fake scoring helpers (demo-only)
# ---------------------------------------------------------

def _clarity_score(text: str) -> float:
    """Simple demo heuristic: shorter sentences → slightly higher score."""
    length = len(text.split())
    if length == 0:
        return 0.0
    return max(0.1, min(1.0, 1.5 / (length ** 0.3)))


def _relevance_score(text: str, question: str) -> float:
    """Fake 'relevance' metric: count overlapping words."""
    t_words = set(text.lower().split())
    q_words = set(question.lower().split())
    overlap = len(t_words & q_words)
    return min(1.0, 0.2 + 0.1 * overlap)


def _style_score(text: str) -> float:
    """Demo scoring: random variation for feel of complexity."""
    return round(0.3 + random.random() * 0.3, 3)


# ---------------------------------------------------------
# Core ordering (demo)
# ---------------------------------------------------------

def order_candidates(question: str, candidates: list) -> dict:
    """
    Orders candidates by fake scores and selects the "top" one.

    Input:
        candidates: [
            {"answer_text": "...", "meta": {...}},
            ...
        ]

    Returns:
        {
            "winner": <candidate>,
            "ordering_table": [...],
            "evaluated_at": "...",
            "demo_version": "v0.1"
        }
    """
    table = []

    for idx, c in enumerate(candidates):
        text = c.get("answer_text", "")
        scores = {
            "clarity": _clarity_score(text),
            "relevance": _relevance_score(text, question),
            "style": _style_score(text),
        }

        final_score = round(
            0.5 * scores["clarity"]
            + 0.3 * scores["relevance"]
            + 0.2 * scores["style"],
            4
        )

        table.append({
            "candidate_index": idx,
            "text_preview": text[:60],
            "scores": scores,
            "final_score": final_score,
        })

    # Sort descending by final score
    table.sort(key=lambda x: x["final_score"], reverse=True)

    # Winner is first item
    winner_index = table[0]["candidate_index"]
    winner = candidates[winner_index]

    return {
        "winner": winner,
        "ordering_table": table,
        "evaluated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "demo_version": "v0.1"
    }


# ---------------------------------------------------------
# Human-readable summary
# ---------------------------------------------------------

def summarize_ordering(result: dict) -> str:
    lines = []
    lines.append("ORDERING RESULTS (DEMO)")
    lines.append("-----------------------")

    for row in result["ordering_table"]:
        lines.append(
            f"Candidate {row['candidate_index']} | "
            f"Final Score: {row['final_score']} | "
            f"Preview: {row['text_preview']}..."
        )
        scores = row["scores"]
        lines.append(
            f"  clarity={scores['clarity']}, "
            f"relevance={scores['relevance']}, "
            f"style={scores['style']}"
        )
        lines.append("")

    lines.append("Winner:")
    lines.append(result["winner"]["answer_text"])
    lines.append("")
    lines.append("Evaluation complete (demo).")

    return "\n".join(lines)


# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

if __name__ == "__main__":
    cands = [
        {"answer_text": "This is a short and clear answer."},
        {"answer_text": "This answer is perhaps slightly more elaborate and uncertain."},
        {"answer_text": "Direct response. Simple. Focused."}
    ]
    res = order_candidates("Explain governance drift.", cands)
    print(summarize_ordering(res))
