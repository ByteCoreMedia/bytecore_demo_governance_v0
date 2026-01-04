"""
simple_cli.py — Interactive CLI for ByteCore Demo Governance Pipeline (v0.1)
----------------------------------------------------------------------------
This command-line interface allows a user to enter a question and see the
entire demo governance pipeline execute:

1. Candidate generation
2. Truth Kernel evaluation (demo)
3. Invariant checks (demo)
4. Ordering stage (demo)
5. Audit chain (demo)
6. Final answer selection

This is a safe, non-IP version designed for demonstration and education.
"""

import json
import sys
from textwrap import indent

from demo_engine import run_governance_pipeline
from demo_runtime.mock_ordering import summarize_ordering
from demo_runtime.mock_audit import summarize_audit_chain


# ---------------------------------------------------------
# Pretty helpers (no dependencies)
# ---------------------------------------------------------

def _banner(text: str):
    """Simple banner for section separation."""
    print("\n" + "=" * 72)
    print(text)
    print("=" * 72 + "\n")


def _print_json(label: str, obj: dict, indent_level=2):
    print(f"{label}:")
    print(json.dumps(obj, indent=indent_level))
    print("")


# ---------------------------------------------------------
# CLI Loop
# ---------------------------------------------------------

def main():
    _banner("BYTECORE DEMO — DETERMINISTIC GOVERNANCE PIPELINE (v0.1)")

    print("Type a question and press Enter.")
    print("Type 'exit' or 'quit' to stop.")
    print("")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting demo.")
            break

        if question.lower() in ("exit", "quit"):
            print("Exiting demo.")
            break

        if not question:
            print("Please enter a question.")
            continue

        # --- Run pipeline ---
        result = run_governance_pipeline(question)

        # -----------------------------------------------------
        # Display Results
        # -----------------------------------------------------

        _banner("CANDIDATE ANSWERS (DEMO)")
        for idx, c in enumerate(result["candidates"]):
            print(f"[Candidate {idx}] ({c['meta']['variant']})")
            print(c["answer_text"])
            print("TK Verdict:", c["tk"]["verdict"])
            print("Invariant Status:", c["invariants"]["status"])
            print("")

        _banner("ORDERING SUMMARY")
        print(summarize_ordering(result["ordering"]))

        _banner("FINAL DECISION")
        print(f"Decision ID: {result['decision']['decision_id']}")
        print(f"Chosen Variant: {result['decision']['chosen_variant']}")
        print(f"Truth Kernel Verdict: {result['decision']['verdict']}")
        print("")
        print("Final Answer:")
        print(result["decision"]["final_answer_text"])
        print("")

        _banner("AUDIT CHAIN (DEMO)")
        print(summarize_audit_chain(result["audit_chain"]))
        print("\n")

    print("Demo terminated.")


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
