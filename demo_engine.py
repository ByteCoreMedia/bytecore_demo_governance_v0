"""
demo_engine.py — ByteCore Demo Governance Pipeline (v0.1)
----------------------------------------------------------
This file ties together all demo components:

- mock_tk           (fake Truth Kernel)
- mock_invariants   (demo invariant checks)
- mock_ordering     (fake deterministic ordering)
- mock_audit        (safe audit chain)
- demo candidate generation

This pipeline is designed to help viewers understand the
*shape* of deterministic AI governance without revealing
any real ByteCore mechanisms or IP-sensitive internals.
"""

import uuid
from datetime import datetime

from demo_runtime.mock_tk import evaluate_truth_kernel
from demo_runtime.mock_invariants import evaluate_invariants
from demo_runtime.mock_ordering import order_candidates
from demo_runtime.mock_audit import build_audit_chain


# ---------------------------------------------------------
# Generate demo candidates (safe, shallow)
# ---------------------------------------------------------

def _generate_demo_candidates(question: str) -> list:
    """
    Returns 2–3 superficial answer variants to demonstrate
    downstream governance operations.

    These are NOT models, NOT LLM calls, NOT your real system.
    Just fixed, templated variants for demonstration.
    """
    q = question.strip("?").strip()

    return [
        {
            "answer_text": f"This is a clear, concise response about '{q}'.",
            "meta": {"variant": "direct"}
        },
        {
            "answer_text": f"A slightly more elaborate explanation of {q}, "
                           "with some additional context for interpretation.",
            "meta": {"variant": "contextual"}
        },
        {
            "answer_text": f"An uncertain or speculative answer that maybe touches "
                           f"on {q} but uses softer or vague phrasing.",
            "meta": {"variant": "speculative"}
        }
    ]


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------

def run_governance_pipeline(question: str) -> dict:
    """
    The heart of the demo system.

    Steps:
    1. Generate demo candidates
    2. Evaluate each with:
       - Truth Kernel mock
       - Invariant evaluations
    3. Order candidates
    4. Select a winner
    5. Build audit chain
    6. Return final result bundle
    """

    # 1. Generate candidates
    candidates = _generate_demo_candidates(question)

    # 2. Evaluate TK + invariants for each candidate
    enriched_candidates = []
    for c in candidates:
        tk_result = evaluate_truth_kernel(c)
        inv_result = evaluate_invariants(c, question=question)

        enriched_candidates.append({
            "answer_text": c["answer_text"],
            "meta": c["meta"],
            "tk": tk_result,
            "invariants": inv_result,
        })

    # 3. Order candidates (demo deterministic sorting)
    ordering = order_candidates(question, enriched_candidates)
    winner = ordering["winner"]

    # 4. Construct decision object
    decision_id = "DEC-" + uuid.uuid4().hex[:8].upper()
    decision = {
        "decision_id": decision_id,
        "verdict": winner["tk"]["verdict"],
        "chosen_variant": winner["meta"]["variant"],
        "final_answer_text": winner["answer_text"],
        "ordered_by": "demo-ordering-v0.1",
        "evaluated_at": ordering["evaluated_at"],
    }

    # 5. Audit chain
    audit_events = build_audit_chain(
        question,
        candidate={"answer_text": winner["answer_text"]},
        decision=decision
    )

    # 6. Final output bundle
    return {
        "question": question,
        "candidates": enriched_candidates,
        "ordering": ordering,
        "winner": winner,
        "decision": decision,
        "audit_chain": audit_events,
        "engine_version": "v0.1",
        "evaluated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

if __name__ == "__main__":
    result = run_governance_pipeline("What is governance drift?")
    import json
    print(json.dumps(result, indent=2))
