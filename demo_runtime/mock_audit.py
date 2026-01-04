"""
mock_audit.py — Demo-Safe Audit Chain (v0.1)
--------------------------------------------
This module imitates the *surface appearance* of a deterministic audit
trail without exposing DAL, MIL, or trace integrity logic.

It provides:
- A sequence of readable audit events
- A "chain integrity: OK" surface indicator
- Fake run IDs and event IDs
- Safe timestamps

It does NOT provide:
- Hash chaining
- Canonical serialization
- Snapshot pointer logic
- DAL invariants
- True audit integrity verification
"""

from datetime import datetime
import hashlib
import json
import random

# ---------------------------------------------------------
# Safe helpers (these are purely cosmetic)
# ---------------------------------------------------------

def _ts():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _fake_hash(seed: str) -> str:
    """Truncated hash to give the impression of a chain, without being real."""
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]

# ---------------------------------------------------------
# Main audit chain builder (safe)
# ---------------------------------------------------------

def build_audit_chain(question: str, candidate: dict, decision: dict) -> list:
    """
    Constructs a demo audit chain.
    Each item is a dict representing a logged event.

    This is purely demonstrational and does not reflect the actual DAL/MIL
    audit mechanics inside the protected ByteCore system.
    """

    run_id = _fake_hash(question + candidate.get("answer_text", ""))

    events = []

    # 1. Snapshot creation event
    events.append({
        "ts": _ts(),
        "event": "SNAPSHOT_CREATED",
        "run_id": run_id,
        "info": "Demo snapshot recorded (safe mock).",
        "event_id": _fake_hash("snapshot" + run_id)
    })

    # 2. Candidate persisted
    events.append({
        "ts": _ts(),
        "event": "CANDIDATE_PERSISTED",
        "run_id": run_id,
        "info": "Candidate captured for governance (demo).",
        "candidate_preview": candidate.get("answer_text", "")[:60],
        "event_id": _fake_hash("candidate" + run_id)
    })

    # 3. TK evaluation event
    events.append({
        "ts": _ts(),
        "event": "TK_EVALUATED",
        "run_id": run_id,
        "result": decision.get("verdict", "UNKNOWN"),
        "info": "Truth Kernel (demo) evaluation complete.",
        "event_id": _fake_hash("tk" + run_id)
    })

    # 4. Decision recorded event
    events.append({
        "ts": _ts(),
        "event": "DECISION_RECORDED",
        "run_id": run_id,
        "decision_id": decision.get("decision_id", "DEMO"),
        "verdict": decision.get("verdict", "UNKNOWN"),
        "event_id": _fake_hash("decision" + run_id)
    })

    return events

# ---------------------------------------------------------
# Human-readable summary functions
# ---------------------------------------------------------

def summarize_audit_chain(chain: list) -> str:
    """Pretty summary for CLI or UI output."""
    lines = []
    lines.append("AUDIT CHAIN (DEMO):")
    lines.append("-------------------")

    for evt in chain:
        lines.append(f"[{evt['ts']}] {evt['event']}: {evt.get('info','')}")
        if "verdict" in evt:
            lines.append(f"  Verdict: {evt['verdict']}")
        if "candidate_preview" in evt:
            lines.append(f"  Candidate Preview: {evt['candidate_preview']}...")
        lines.append(f"  Event ID: {evt['event_id']}")
        lines.append("")

    lines.append("Chain integrity: OK (demo)")
    return "\n".join(lines)

# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

if __name__ == "__main__":
    mock_candidate = {
        "answer_text": "This is a demonstration answer showing governance structure."
    }
    mock_decision = {
        "verdict": "PASS_WITH_WARNINGS",
        "decision_id": "DEC-123456"
    }
    chain = build_audit_chain(
        "How does governance work?",
        mock_candidate,
        mock_decision
    )
    print(summarize_audit_chain(chain))
