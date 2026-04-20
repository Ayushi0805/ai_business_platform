"""
Phase 9 — Decision Engine.

Combines outputs from all AI layers into a single actionable verdict:
  - "approved"  → safe to process, trigger invoice generation
  - "flagged"   → needs manual review, notify admin
  - "rejected"  → fraud detected, block order, alert team
"""

def make_decision(fraud: bool, image_ok: bool, invoice_valid: bool, llm_verdict: str) -> str:
    if fraud:
        return 'rejected'
    
    if not image_ok or not invoice_valid:
        return 'flagged'
    
    if llm_verdict and 'approve' in llm_verdict.lower():
        return 'approved'
    
    return 'flagged'
