"""
mock_tk.py — Fake Truth Kernel (Demo-Safe Version)
--------------------------------------------------
This file simulates the *surface behavior* of the ByteCore Truth Kernel
WITHOUT revealing any internal mechanisms.

It provides:
- A simple PASS / FAIL simulation
- A few demonstration "reason codes"
- A predictable, deterministic interface

It does NOT include:
- Real structural verification logic
- Real prohibited-field logic
- Real invariant evaluation
- Real CCTM validation
- Real decision ranking or TK internals
"""

from datetime import datetime
import hashlib
import random

# ---------------------------------------------------------
# Helper utilities (safe, purely cosmetic)
# ---------------------------------------------------------

def _ts():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

# ---------------------------------------------------------
# DEMO REASON CODES (NON-IP)
# ---------------------------------------------------------

REASONS = {
    "TK_DEMO_STRUCTURAL_OK": "Basic structure appears valid (demo).",
    "TK_DEMO_META_OK":       "Metadata fields present (demo).",
    "TK_DEMO_CLARITY_WARN":  "Answer includes uncertainty or vague phrasing (demo).",
    "TK_DEMO_PASS":          "Candidate acceptable under demo rules.",
    "TK_DEMO_FAIL":          "Candidate failed demo validation.",
}

# ---------------------------------------------------------
# FAKE TK EVALUATION LOGIC
# ---------------------------------------------------------

def evaluate_candidate(candidate: dict) -> dict:
    """
    Demo-safe TK imitation.
    Always returns:
        {
            "result": "PASS" | "FAIL" | "PASS_WITH_WARNINGS",
            "reasons": [ { code, message } ],
            "tk_evaluated_at": timestamp,
            "tk_evaluation_id": stable hash
        }
    """

    reasons = []

    # -----------------------------------------------------
    # 1. Demo structural check (ALWAYS PASSES)
    # -----------------------------------------------------
    reasons.append({
        "code": "TK_DEMO_STRUCTURAL_OK",
        "message": REASONS["TK_DEMO_STRUCTURAL_OK"]
    })

    # -----------------------------------------------------
    # 2. Demo metadata check (ALWAYS PASSES)
    # -----------------------------------------------------
    reasons.append({
        "code": "TK_DEMO_META_OK",
        "message": REASONS["TK_DEMO_META_OK"]
    })

    # -----------------------------------------------------
    # 3. Demonstration WARNING heuristic
    # -----------------------------------------------------
    warn = False
    if "uncertain" in candidate.get("answer_text", "").lower():
        warn = True
    if random.random() < 0.30:
        warn = True

    if warn:
        reasons.append({
            "code": "TK_DEMO_CLARITY_WARN",
            "message": REASONS["TK_DEMO_CLARITY_WARN"]
        })

    # -----------------------------------------------------
    # Demo verdict logic (SAFE)
    # -----------------------------------------------------
    if warn:
        result = "PASS_WITH_WARNINGS"
    else:
        result = "PASS"

    # (We never produce FAIL automatically in this demo unless scripted externally)
    # FAIL that you'd trigger manually for training:
    # if "forbidden" in candidate.get("answer_text", "").lower():
    #     result = "FAIL"
    #     reasons.append({
    #         "code": "TK_DEMO_FAIL",
    #         "message": REASONS["TK_DEMO_FAIL"]
    #     })

    evaluation = {
        "result": result,
        "reasons": reasons,
        "tk_evaluated_at": _ts(),
        "tk_evaluation_id": _hash(candidate.get("answer_text", "") + _ts()),
        "tk_demo_version": "v0.1",
    }

    # Alias for compatibility with demo_engine / CLI / reporter
    evaluation["verdict"] = evaluation["result"]

    return evaluation


# ---------------------------------------------------------
# Compatibility wrapper for demo_engine import expectations
# ---------------------------------------------------------

def evaluate_truth_kernel(candidate: dict) -> dict:
    """Alias wrapper so demo_engine.py can call the TK evaluation."""
    return evaluate_candidate(candidate)


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":
    test = {
        "answer_text": "This is a demonstration answer with uncertain elements.",
        "trace": "demo"
    }
    out = evaluate_candidate(test)
    import json
    print(json.dumps(out, indent=2))
