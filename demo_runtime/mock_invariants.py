"""
mock_invariants.py — Demo-Safe Invariant Layer (v0.1)
-----------------------------------------------------
This module provides a *demonstration-only* approximation of what
invariants look like in a deterministic governance system.

These are NOT the real ByteCore invariants.
They do NOT reveal structure, logic, evaluation rules, schema fields,
or enforcement mechanisms used in the real Truth Kernel.

They merely:
- Provide example rule objects
- Demonstrate PASS / WARN behavior
- Help users conceptually understand value constraints
"""

from datetime import datetime
import random

# ---------------------------------------------------------
# Demo invariant definitions (illustrative only)
# ---------------------------------------------------------

DEMO_INVARIANTS = [
    {
        "id": "INV-DEMO-001",
        "name": "Clarity Requirement",
        "severity": "WARN",
        "description": "Answer should avoid vague or ambiguous phrasing when possible.",
    },
    {
        "id": "INV-DEMO-002",
        "name": "Relevance to Query",
        "severity": "WARN",
        "description": "Answer should remain meaningfully related to the input question.",
    },
    {
        "id": "INV-DEMO-003",
        "name": "Responsible Framing",
        "severity": "WARN",
        "description": "Answer should frame information constructively and avoid unnecessary alarm.",
    },
    {
        "id": "INV-DEMO-004",
        "name": "Domain Boundary Awareness",
        "severity": "WARN",
        "description": "Answer should acknowledge uncertainty when leaving the domain of the question.",
    }
]

# ---------------------------------------------------------
# Fake evaluation logic (safe, shallow)
# ---------------------------------------------------------

def evaluate_invariants(candidate: dict, *, question: str = "") -> dict:
    """
    Demo-safe invariant evaluation.

    Returns:
        {
            "status": "PASS" | "WARN",
            "hits": [ { id, name, severity, detail } ],
            "evaluated_at": "...",
            "demo_version": "v0.1"
        }

    There are no FAIL states in this demo implementation.
    """
    hits = []

    text = candidate.get("answer_text", "").lower()

    # --- DEMO HEURISTICS (completely fake, non-IP) ---
    # Trigger clarity rule if vague language detected
    if any(w in text for w in ["maybe", "possibly", "uncertain", "appears"]):
        hits.append({
            "id": "INV-DEMO-001",
            "name": "Clarity Requirement",
            "severity": "WARN",
            "detail": "Detected vague or uncertain phrasing.",
        })

    # Trigger relevance rule randomly (demo only)
    if random.random() < 0.20:
        hits.append({
            "id": "INV-DEMO-002",
            "name": "Relevance to Query",
            "severity": "WARN",
            "detail": "Answer may partially diverge from user intent.",
        })

    # Trigger responsible framing occasionally (demo)
    if random.random() < 0.15:
        hits.append({
            "id": "INV-DEMO-003",
            "name": "Responsible Framing",
            "severity": "WARN",
            "detail": "Tone could be more balanced or contextualized.",
        })

    # Trigger boundary awareness occasionally
    if random.random() < 0.10:
        hits.append({
            "id": "INV-DEMO-004",
            "name": "Domain Boundary Awareness",
            "severity": "WARN",
            "detail": "Consider explicitly noting uncertainty about domain limits.",
        })

    # Final status
    status = "PASS" if len(hits) == 0 else "WARN"

    return {
        "status": status,
        "hits": hits,
        "evaluated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "demo_version": "v0.1"
    }


# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

if __name__ == "__main__":
    candidate = {
        "answer_text": "This is a clear but possibly uncertain example answer.",
        "trace": "demo-cctm-valid"
    }
    result = evaluate_invariants(candidate, question="Explain model drift.")
    import json
    print(json.dumps(result, indent=2))
