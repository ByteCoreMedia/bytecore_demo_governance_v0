"""
demo_reporter.py — Structured Governance Report Generator (v0.1)
-----------------------------------------------------------------
Takes the full output from run_governance_pipeline() and formats it
into a clean, readable Markdown governance report.

This is meant for:
- demonstrations
- technical evaluations
- partner discussions
- audit-style walkthroughs

It exposes no real ByteCore logic. Only organizes the demo data.
"""

import os
from datetime import datetime
from textwrap import indent


# ---------------------------------------------------------
# Utility formatting
# ---------------------------------------------------------

def _section(title: str) -> str:
    return f"\n# {title}\n\n"

def _subsection(title: str) -> str:
    return f"\n## {title}\n\n"

def _bullet_list(items) -> str:
    return "".join(f"- {item}\n" for item in items)

def _codeblock(content: str) -> str:
    return f"```\n{content}\n```\n"

def _kv_block(obj: dict) -> str:
    return _codeblock(
        "\n".join([f"{k}: {v}" for k, v in obj.items()])
    )


# ---------------------------------------------------------
# Main report generator
# ---------------------------------------------------------

def generate_governance_report(result: dict) -> str:
    """
    Accepts the full pipeline result and returns a complete
    Markdown-formatted governance report.

    Sections include:
    - Overview
    - Question
    - Candidate Answers
    - Truth Kernel Summary
    - Invariant Summary
    - Ordering Results
    - Final Decision
    - Audit Chain
    """
    report = []

    # -----------------------------------------------------
    # REPORT HEADER
    # -----------------------------------------------------
    report.append("# ByteCore Deterministic Governance — Demo Report (v0.1)\n")
    report.append(f"Generated: **{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}**")
    report.append("\n---\n")

    # -----------------------------------------------------
    # SECTION: INPUT QUESTION
    # -----------------------------------------------------
    report.append(_section("Input Question"))
    report.append(f"**Question:** {result['question']}\n")

    # -----------------------------------------------------
    # SECTION: CANDIDATES
    # -----------------------------------------------------
    report.append(_section("Candidate Answers"))

    for idx, cand in enumerate(result["candidates"]):
        report.append(_subsection(f"Candidate {idx + 1}: {cand['meta']['variant']}"))
        report.append(f"**Text:**\n{cand['answer_text']}\n")
        report.append("**Truth Kernel Verdict:** " + cand["tk"]["verdict"])
        report.append("\n\n**Invariant Evaluation:**")
        report.append(_codeblock(
            f"status: {cand['invariants']['status']}\n"
            f"hits: {len(cand['invariants']['hits'])}"
        ))

    # -----------------------------------------------------
    # SECTION: ORDERING
    # -----------------------------------------------------
    report.append(_section("Ordering Results"))

    ordering_table = result["ordering"]["ordering_table"]
    for row in ordering_table:
        report.append(_subsection(f"Candidate {row['candidate_index']} Score"))
        report.append(_codeblock(
            f"final_score: {row['final_score']}\n"
            f"text_preview: {row['text_preview']}...\n"
            f"clarity: {row['scores']['clarity']}\n"
            f"relevance: {row['scores']['relevance']}\n"
            f"style: {row['scores']['style']}"
        ))

    # -----------------------------------------------------
    # SECTION: FINAL DECISION
    # -----------------------------------------------------
    report.append(_section("Final Decision"))

    dec = result["decision"]
    report.append(_kv_block(dec))

    report.append("\n### Answer Text\n")
    report.append(result["decision"]["final_answer_text"] + "\n")

    # -----------------------------------------------------
    # SECTION: AUDIT CHAIN
    # -----------------------------------------------------
    report.append(_section("Audit Chain (Demo)"))

    for evt in result["audit_chain"]:
        report.append(_subsection(evt["event"]))
        block = "\n".join(
            f"{k}: {v}"
            for k, v in evt.items()
            if k != "event"
        )
        report.append(_codeblock(block))

    # -----------------------------------------------------
    # END
    # -----------------------------------------------------
    report.append("\n---\n")
    report.append("**End of Report**\n")

    return "".join(report)


# ---------------------------------------------------------
# Export Function
# ---------------------------------------------------------

def save_report(result: dict, out_path: str = None) -> str:
    """
    Saves a Markdown report to disk.

    If out_path is not provided, generate a timestamped file.
    Returns the file path.
    """
    if out_path is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_path = f"governance_report_{timestamp}.md"

    md = generate_governance_report(result)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    return out_path


# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

if __name__ == "__main__":
    from demo_engine import run_governance_pipeline
    example = run_governance_pipeline("Explain governance drift.")
    path = save_report(example)
    print(f"Report saved to {path}")
