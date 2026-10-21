"""Transparent interview intake, without simulated strategic confidence."""
from html import escape

PHASES = (
    ("Interaction frequency", "How often does the customer need this outcome? What observed behavior supports the acquisition or referral mechanism?"),
    ("Incumbent alternatives", "Which alternative does the customer use today? What sourced evidence supports a reason to switch?"),
    ("User and buyer", "Who uses the product and who pays? Which adoption and security requirements must be met before a pilot?"),
    ("Initial market and expansion", "Which initial segment has the strongest evidence of demand? What observation would justify expanding beyond it?"),
    ("Value delivery", "Which task creates measurable value? When should the user initiate it or authorize background execution?"),
    ("Model and context control", "Which model dependencies matter to reliability or cost? How can the customer export and delete their context?"),
    ("Pricing and costs", "What evidence supports willingness to pay? What measured costs and limits protect the unit economics?"),
    ("Integration and exit", "Which integrations are required to deliver value? How are permissions, failures and customer exit handled?"),
)


def validate_text(value, name, max_length=10000):
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        raise ValueError(f"{name} must be a non-empty string of at most {max_length} characters")
    return value


def validate_scores(scores):
    if (not isinstance(scores, (list, tuple)) or len(scores) != 8
            or any(type(score) is not int or not 0 <= score <= 100 for score in scores)):
        raise ValueError("scores must contain exactly 8 integers between 0 and 100")
    return list(scores)


def assess_answer(phase, answer):
    if type(phase) is not int or not 1 <= phase <= 8:
        raise ValueError("phase must be an integer from 1 through 8")
    validate_text(answer, "founder_answer")
    return {
        "phase": phase,
        "confidence_score": None,
        "status": "REVIEW_REQUIRED",
        "guidance": PHASES[phase - 1][1],
        "evidence_state": "founder_reported",
        "limitation": "Intake only. No model evaluation, source verification or calibrated confidence is implemented.",
    }


def render_playbook(startup_name, answers):
    """Preserve founder inputs and distinguish them from reviewer conclusions."""
    lines = [f"# {escape(startup_name)}: GTM interview draft", "",
             "Status: REVIEW REQUIRED. Answers are founder-reported, not validated strategy.",
             "No confidence probability or market outcome is inferred.", ""]
    for (title, question), answer in zip(PHASES, answers):
        lines.extend([f"## {title}", "", question, "",
                      "Founder response:", "",
                      *("    " + line for line in escape(answer).splitlines()), "",
                      "Evidence, counterexample and next experiment: EVIDENCE REQUIRED.", ""])
    return "\n".join(lines)
