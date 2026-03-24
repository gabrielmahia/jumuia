"""
Magisterial Boundary Layer — Jumuia — Parish Community
=====================================================
Spec §3: AI components must avoid doctrinal innovation, political endorsement,
moral speculation; must defer controversial questions; must log doctrinal-sensitive
interactions. No AI may impersonate clergy.

This module is the single point of enforcement for all AI theological guardrails.
Import and apply to any AI service that handles user queries.

Architecture:
- classify_query()   → flags topic sensitivity before sending to model
- build_system_prompt() → Magisterial-safe system prompt fragments
- post_process()     → validates response doesn't violate boundaries
- log_sensitive()    → audit trail for doctrinal-sensitive interactions
"""

import re
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# ── Sensitivity classification ─────────────────────────────────────────────────
# Topics requiring extra guardrail — deference to clergy, CCC citation expected

DOCTRINAL_SENSITIVE_PATTERNS = [
    # Sacramental theology
    re.compile(r"\b(valid|validity|invalid|licit|illicit|nullity|annulment)\b", re.I),
    # Controversial moral questions
    re.compile(r"\b(contraception|abortion|divorce|remarri|euthanasi|homosexual|same.sex|ivf|surrogac)\b", re.I),
    # Ecclesiological disputes
    re.compile(r"\b(schism|heresy|excommunicat|sedevacantist|SSPX|ordination.*women|female.*priest)\b", re.I),
    # Papal / magisterial authority questions
    re.compile(r"\b(infallible|ex cathedra|papal.*error|pope.*wrong|magisterium.*wrong)\b", re.I),
    # End-of-life / medical ethics
    re.compile(r"\b(assisted.*dying|palliative.*hasten|withdrawing.*treatment)\b", re.I),
    # Political
    re.compile(r"\b(vote|election|democrat|republican|labour|conservative|political party)\b", re.I),
    # Spiritual direction boundary
    re.compile(r"\b(my sin|confess to you|absolve|penance|my spiritual director)\b", re.I),
]

CLERGY_IMPERSONATION_PATTERNS = [
    re.compile(r"\b(I absolve|ego te absolvo|your sins are forgiven|I grant.*penance)\b", re.I),
    re.compile(r"\b(as your priest|as your pastor|I am.*father|I am.*clergy)\b", re.I),
]

# Standard CCC citation topics — reference these in responses
CCC_REFERENCES = {
    "sacraments":      "CCC 1210–1666",
    "baptism":         "CCC 1213–1284",
    "confirmation":    "CCC 1285–1321",
    "eucharist":       "CCC 1322–1419",
    "reconciliation":  "CCC 1422–1498",
    "anointing":       "CCC 1499–1532",
    "marriage":        "CCC 1601–1666",
    "holy_orders":     "CCC 1536–1600",
    "prayer":          "CCC 2558–2865",
    "morality":        "CCC 1691–2557",
    "creed":           "CCC 185–1065",
    "social_teaching": "CCC 2401–2463",
}


def classify_query(text: str) -> dict:
    """
    Classify a user query for theological sensitivity.

    Returns:
        {
            "sensitive": bool,
            "categories": list[str],
            "clergy_impersonation_risk": bool,
            "requires_deference": bool,
        }
    """
    sensitive_categories = []
    for pattern in DOCTRINAL_SENSITIVE_PATTERNS:
        if pattern.search(text):
            sensitive_categories.append(pattern.pattern[:40].strip("\\b()").split("|")[0])

    clergy_risk = any(p.search(text) for p in CLERGY_IMPERSONATION_PATTERNS)

    return {
        "sensitive": len(sensitive_categories) > 0 or clergy_risk,
        "categories": sensitive_categories,
        "clergy_impersonation_risk": clergy_risk,
        "requires_deference": len(sensitive_categories) > 0,
    }


def build_system_prompt(lang_name: str = "English", parish_context: str = "") -> str:
    """
    Return the Magisterial-safe system prompt fragment.
    Inject into any AI service handling theological questions.
    """
    return f"""You are a warm, knowledgeable Catholic parish assistant serving a global community.
{parish_context}

CORE BOUNDARIES (Magisterial Boundary Layer — non-negotiable):
1. You are NOT a priest, deacon, bishop, or spiritual director. Never impersonate clergy.
2. Do NOT grant absolution, assign penance, or simulate the Sacrament of Reconciliation.
3. Avoid doctrinal innovation — stay within the Magisterium of the Catholic Church.
4. When answering theological questions, ground your response in:
   - The Catechism of the Catholic Church (CCC)
   - Scripture (with book/chapter/verse)
   - Church documents (cited by name)
5. On controversial moral, social, or political questions:
   - Present the Church's teaching from the CCC without personal commentary
   - Do NOT endorse political parties or candidates
   - Recommend consulting a priest for personal pastoral guidance
6. Use non-authoritative language: "The Church teaches...", "According to the CCC..."
   Never: "You should...", "God wants you to..." as personal declarations.
7. For pastoral counseling, grief, addiction, or personal crisis:
   - Offer compassion, point to Church resources, recommend speaking with a priest.
8. For questions about confession content, private prayer, or spiritual direction notes:
   - Do not engage with or store the content. Redirect warmly.

TONE: Warm, pastoral, humble, precise. Appropriate for a 70-year-old catechist or a 14-year-old student.
LANGUAGE: Always respond in {lang_name}.
LENGTH: 2–3 sentences for most questions. Longer only when catechetical depth is clearly needed."""


def post_process(response: str) -> tuple[str, bool]:
    """
    Validate AI response doesn't violate Magisterial boundaries.
    Returns (response, is_clean).
    If violation detected, returns (safe_fallback_response, False).
    """
    for pattern in CLERGY_IMPERSONATION_PATTERNS:
        if pattern.search(response):
            logger.warning("MAGISTERIAL_VIOLATION: clergy impersonation detected in response")
            return (
                "I'm not able to provide that response. Please speak with your parish priest "
                "for sacramental guidance.",
                False,
            )
    return response, True


def log_sensitive(query: str, classification: dict, session_id: str = "") -> None:
    """
    Audit log for doctrinal-sensitive interactions.
    Logs category and anonymised session — never logs query content.
    Spec §3: 'Log doctrinal-sensitive interactions.'
    """
    from services.privacy import scrub_pii, anonymise
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": "doctrinal_sensitive_query",
        "categories": classification.get("categories", []),
        "clergy_risk": classification.get("clergy_impersonation_risk", False),
        "session_hash": anonymise(session_id) if session_id else "anon",
    }
    logger.info("MAGISTERIAL_LOG: %s", entry)
    try:
        from services.sheets import _save
        _save("magisterial_audit", entry)
    except Exception:
        pass


def ccc_hint(topic_keyword: str) -> str:
    """Return a CCC reference hint for a given topic keyword, or empty string."""
    kw = topic_keyword.lower()
    for topic, ref in CCC_REFERENCES.items():
        if topic in kw or kw in topic:
            return f" (See {ref})"
    return ""
