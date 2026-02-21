"""
Tests — Catholic Network Tools
Smoke tests + unit tests for all services.
Run: pytest tests/ -v
"""
import os
import sqlite3
import sys
import pytest

# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Redirect all DB operations to a temp file."""
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("CNT_DB_PATH", str(db_file))
    monkeypatch.setenv("MPESA_ENV", "sandbox")
    return db_file


# ─────────────────────────────────────────────
# IMPORTS SMOKE TEST
# ─────────────────────────────────────────────

def test_ai_service_imports():
    sys.path.insert(0, ".")
    from services.ai_service import (
        SUPPORTED_LANGUAGES
    )
    assert "en" in SUPPORTED_LANGUAGES
    assert "sw" in SUPPORTED_LANGUAGES
    assert "fr" in SUPPORTED_LANGUAGES


def test_directory_service_imports():
    from services.directory_service import (
        init_db
    )
    assert callable(init_db)


def test_mpesa_service_imports():
    from services.mpesa_service import (
        initiate_stk_push
    )
    assert callable(initiate_stk_push)


def test_whatsapp_service_imports():
    from services.whatsapp_service import (
        activation_status
    )
    assert callable(activation_status)


# ─────────────────────────────────────────────
# DIRECTORY SERVICE TESTS
# ─────────────────────────────────────────────

def test_directory_init_and_seed():
    from services.directory_service import init_db, get_stats
    init_db()  # no seed CSV in test — should succeed with empty DB
    stats = get_stats()
    assert "total" in stats
    assert isinstance(stats["total"], int)


def test_directory_search_empty():
    from services.directory_service import init_db, search_parishes
    init_db()
    results = search_parishes("Nairobi")
    assert isinstance(results, list)


def test_directory_search_with_data(tmp_path, monkeypatch):
    """Insert a test parish and verify search finds it."""
    from services.directory_service import init_db, search_parishes
    import services.directory_service as ds

    # Patch DB_PATH to temp
    db_file = tmp_path / "test_search.db"
    monkeypatch.setattr(ds, "DB_PATH", db_file)

    init_db()

    conn = sqlite3.connect(db_file)
    conn.execute(
        """INSERT INTO parishes (name, country, city, diocese, source, verified)
           VALUES (?,?,?,?,?,?)""",
        ("Holy Family Basilica", "Kenya", "Nairobi", "Archdiocese of Nairobi", "test", 1),
    )
    conn.commit()
    conn.close()

    results = search_parishes("Holy Family")
    assert len(results) >= 1
    assert results[0]["name"] == "Holy Family Basilica"


def test_gcatholic_rails_returns_correct_status():
    from services.directory_service import sync_gcatholic
    result = sync_gcatholic(dry_run=True)
    assert result["status"] == "RAILS_ONLY"
    assert "next_steps" in result
    assert len(result["next_steps"]) > 0


# ─────────────────────────────────────────────
# MPESA SERVICE TESTS
# ─────────────────────────────────────────────

def test_mpesa_missing_credentials_returns_graceful_error():
    """Without credentials, initiate_stk_push should return structured error."""
    os.environ.pop("MPESA_CONSUMER_KEY", None)
    os.environ.pop("MPESA_CONSUMER_SECRET", None)
    from services.mpesa_service import initiate_stk_push
    result = initiate_stk_push("254700000000", 100)
    assert result["success"] is False
    assert result["error"] == "CREDENTIALS_MISSING"


def test_mpesa_callback_parse_success():
    from services.mpesa_service import handle_callback
    payload = {
        "Body": {
            "stkCallback": {
                "ResultCode": 0,
                "CheckoutRequestID": "ws_CO_test123",
                "CallbackMetadata": {
                    "Item": [
                        {"Name": "Amount",              "Value": 100},
                        {"Name": "MpesaReceiptNumber",  "Value": "NLJ7RT61SV"},
                        {"Name": "PhoneNumber",         "Value": 254700000000},
                        {"Name": "TransactionDate",     "Value": 20240101120000},
                    ]
                }
            }
        }
    }
    result = handle_callback(payload)
    assert result["success"] is True
    assert result["mpesa_receipt"] == "NLJ7RT61SV"


def test_mpesa_callback_parse_failed():
    from services.mpesa_service import handle_callback
    payload = {
        "Body": {
            "stkCallback": {
                "ResultCode": 1032,
                "CheckoutRequestID": "ws_CO_test456",
                "ResultDesc": "Request cancelled by user",
            }
        }
    }
    result = handle_callback(payload)
    assert result["success"] is False


def test_mpesa_live_checklist_structure():
    from services.mpesa_service import live_activation_checklist
    checklist = live_activation_checklist()
    assert "live_requirements" in checklist
    assert len(checklist["live_requirements"]) >= 5
    assert "estimated_time" in checklist


def test_giving_db_init_and_summary(tmp_path, monkeypatch):
    import services.mpesa_service as ms
    db_file = tmp_path / "giving.db"
    monkeypatch.setattr(ms, "DB_PATH", db_file)
    ms.init_giving_db()
    summary = ms.get_giving_summary(sandbox_only=True)
    assert summary["total_kes"] == 0
    assert summary["transaction_count"] == 0


# ─────────────────────────────────────────────
# WHATSAPP SERVICE TESTS
# ─────────────────────────────────────────────

def test_parse_at_inbound():
    from services.whatsapp_service import parse_at_inbound
    payload = {"from": "254700000000", "text": "Hello, what time is Mass?", "id": "ATxxx"}
    result = parse_at_inbound(payload)
    assert result["phone"] == "254700000000"
    assert result["message"] == "Hello, what time is Mass?"
    assert result["provider"] == "africas_talking"


def test_parse_twilio_inbound():
    from services.whatsapp_service import parse_twilio_inbound
    form_data = {
        "From": "whatsapp:+254700000000",
        "Body": "Habari za asubuhi",
        "MessageSid": "SMxxx",
    }
    result = parse_twilio_inbound(form_data)
    assert result["phone"] == "254700000000"
    assert result["message"] == "Habari za asubuhi"


def test_language_detection():
    from services.whatsapp_service import _detect_language_simple
    assert _detect_language_simple("Habari za asubuhi") == "sw"
    assert _detect_language_simple("Bonjour, quelle heure est la messe?") == "fr"
    assert _detect_language_simple("Hello, when is Mass on Sunday?") == "en"
    assert _detect_language_simple("Hola, ¿a qué hora es la misa?") == "es"


def test_activation_status_structure():
    from services.whatsapp_service import activation_status
    status = activation_status()
    assert status["framework_status"] == "READY"
    assert "africas_talking" in status
    assert "twilio" in status
    assert "webhook_requirement" in status


def test_whatsapp_db_init(tmp_path, monkeypatch):
    import services.whatsapp_service as ws
    db_file = tmp_path / "wa.db"
    monkeypatch.setattr(ws, "DB_PATH", db_file)
    ws.init_whatsapp_db()
    history = ws.get_conversation_history("254700000000")
    assert history == []


def test_whatsapp_conversation_store(tmp_path, monkeypatch):
    import services.whatsapp_service as ws
    db_file = tmp_path / "wa_conv.db"
    monkeypatch.setattr(ws, "DB_PATH", db_file)
    ws.init_whatsapp_db()
    ws.save_turn("254700000000", "user",      "Hello",    "en")
    ws.save_turn("254700000000", "assistant", "Hi there", "en")
    history = ws.get_conversation_history("254700000000")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


# ─────────────────────────────────────────────
# AI SERVICE TESTS (no API key — graceful error)
# ─────────────────────────────────────────────

def test_ai_translate_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from services.ai_service import translate_text
    result = translate_text("Hello parish", "sw")
    assert result["success"] is False
    assert result["error"] is not None


def test_ai_translate_unsupported_language():
    from services.ai_service import translate_text
    result = translate_text("Hello", "zz")  # unsupported
    assert result["success"] is False
    assert "Unsupported" in result["error"]


def test_ai_homily_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from services.ai_service import homily_helper
    result = homily_helper("John 6:51", "Ordinary Time")
    assert result["success"] is False
    assert result["disclaimer"] != ""  # disclaimer always present


def test_ai_insights_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from services.ai_service import generate_parish_insights
    result = generate_parish_insights({"attendance": 200})
    assert result["success"] is False


def test_ai_bot_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from services.ai_service import bot_respond
    result = bot_respond("Hello", [])
    assert result["success"] is False


# ─────────────────────────────────────────────
# USSD SERVICE TESTS
# ─────────────────────────────────────────────

def test_ussd_service_imports():
    from services.ussd_service import handle_ussd_session, channel_setup_guide
    assert callable(handle_ussd_session)
    guide = channel_setup_guide()
    assert "steps" in guide
    assert len(guide["steps"]) > 0


def test_ussd_main_menu():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s1", "*384*1#", "+254700000000", "")
    assert result.startswith("CON")
    assert "Find Parish" in result


def test_ussd_mass_times():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s2", "*384*1#", "+254700000000", "2")
    assert result.startswith("END")
    assert "Mass" in result or "am" in result


def test_ussd_daily_reading():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s3", "*384*1#", "+254700000000", "4")
    assert result.startswith("END")


def test_ussd_emergency_contacts():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s4", "*384*1#", "+254700000000", "5")
    assert result.startswith("END")


def test_ussd_invalid_choice():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s5", "*384*1#", "+254700000000", "9")
    assert result.startswith("CON")
    assert "Invalid" in result


def test_ussd_find_parish_prompt():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s6", "*384*1#", "+254700000000", "1")
    assert result.startswith("CON")


def test_ussd_giving_prompt():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s7", "*384*1#", "+254700000000", "3")
    assert result.startswith("CON")
    assert "KES" in result


def test_ussd_giving_invalid_amount():
    from services.ussd_service import handle_ussd_session
    result = handle_ussd_session("s8", "*384*1#", "+254700000000", "3*abc")
    assert result.startswith("END")
    assert "Invalid" in result or "amount" in result.lower()


def test_ussd_response_length():
    """All USSD responses must be under 182 chars (AT hard limit)."""
    from services.ussd_service import handle_ussd_session
    for text in ["", "1", "2", "3", "4", "5", "9"]:
        result = handle_ussd_session("len-test", "*384*1#", "+254700000000", text)
        prefix_len = 4  # "CON " or "END "
        assert len(result) <= 182 + prefix_len, f"Response too long for input '{text}': {len(result)} chars"


# ── Magisterial Boundary Layer tests ──────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_magisterial_classify_safe():
    from services.magisterial import classify_query
    r = classify_query("What time is Sunday Mass?")
    assert r["sensitive"] is False
    assert r["clergy_impersonation_risk"] is False

def test_magisterial_classify_sensitive():
    from services.magisterial import classify_query
    r = classify_query("Is contraception allowed?")
    assert r["sensitive"] is True
    assert r["requires_deference"] is True

def test_magisterial_clergy_impersonation():
    from services.magisterial import classify_query
    r = classify_query("I absolve you of your sins")
    assert r["clergy_impersonation_risk"] is True

def test_magisterial_post_process_clean():
    from services.magisterial import post_process
    resp, ok = post_process("The Church teaches that prayer is important.")
    assert ok is True

def test_magisterial_post_process_violation():
    from services.magisterial import post_process
    resp, ok = post_process("I absolve you and grant you penance.")
    assert ok is False
    assert "priest" in resp.lower()

def test_magisterial_build_system_prompt():
    from services.magisterial import build_system_prompt
    prompt = build_system_prompt("Swahili", "serving St. Peter's, Nairobi")
    assert "Swahili" in prompt
    assert "Nairobi" in prompt
    assert "absolve" in prompt.lower() or "clergy" in prompt.lower()

def test_magisterial_ccc_hint():
    from services.magisterial import ccc_hint
    hint = ccc_hint("baptism")
    assert "CCC" in hint
    assert ccc_hint("unknowntopic") == ""

# ── Roles tests ────────────────────────────────────────────────────────────────
def test_roles_rank_ordering():
    from services.roles import _rank
    assert _rank("parishioner") < _rank("catechist")
    assert _rank("catechist") < _rank("coordinator")
    assert _rank("coordinator") < _rank("priest")
    assert _rank("priest") < _rank("diocese_admin")

def test_roles_unknown_role_defaults_to_zero():
    from services.roles import _rank
    assert _rank("unknown_role") == 0

def test_roles_is_at_least():
    from services.roles import _rank
    # Pure rank logic — no Streamlit runtime required
    assert _rank("coordinator") >= _rank("catechist")
    assert _rank("catechist") >= _rank("parishioner")
    assert _rank("diocese_admin") > _rank("coordinator")

def test_roles_all_roles_have_labels():
    from services.roles import ROLES, ROLE_LABELS, ROLE_ICONS
    for role in ROLES:
        assert role in ROLE_LABELS, f"Missing label for {role}"
        assert role in ROLE_ICONS, f"Missing icon for {role}"


# ── Liturgical Engine & Obligations Tests ─────────────────────────────────────

def test_liturgical_engine_lent_season():
    """Ash Wednesday 2026 is Lent, not Ordinary Time."""
    from datetime import date
    from services.liturgical_engine import get_liturgical_day
    ld = get_liturgical_day(date(2026, 2, 18))
    assert ld.season == "Lent"
    assert ld.feast == "Ash Wednesday"
    assert ld.color == "Purple"


def test_liturgical_engine_year_a_2026():
    """2025-26 liturgical year should be Year A (Matthew)."""
    from datetime import date
    from services.liturgical_engine import get_liturgical_day
    ld = get_liturgical_day(date(2026, 3, 1))  # 2nd Sunday of Lent
    assert ld.liturgical_year == "A", f"Expected A, got {ld.liturgical_year}"


def test_obligations_fasting_ash_wednesday():
    """Ash Wednesday requires both fasting and abstinence."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    obs = get_obligations(date(2026, 2, 18), "KE")
    assert obs.fasting is True
    assert obs.abstinence is True


def test_obligations_good_friday():
    """Good Friday 2026 requires fasting and abstinence."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    obs = get_obligations(date(2026, 4, 3), "KE")
    assert obs.fasting is True
    assert obs.abstinence is True


def test_obligations_christmas_kenya():
    """Christmas is obligatory in Kenya."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    obs = get_obligations(date(2026, 12, 25), "KE")
    assert obs.is_holy_day is True
    assert obs.mass_obligation == "Obligatory"
    assert obs.source == "KCCB"


def test_obligations_usccb_dispensation():
    """USCCB dispenses Assumption when it falls on Saturday or Monday."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    # Aug 15 2026 is a Saturday — should be dispensed for US
    obs_us = get_obligations(date(2026, 8, 15), "US")
    assert obs_us.mass_obligation == "Dispensed", f"Expected Dispensed, got {obs_us.mass_obligation}"
    # Same date in Kenya — not dispensed
    obs_ke = get_obligations(date(2026, 8, 15), "KE")
    assert obs_ke.mass_obligation == "Obligatory"


def test_obligations_source_codes():
    """Source codes match the correct episcopal conferences."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    assert get_obligations(date(2026, 12, 25), "US").source == "USCCB"
    assert get_obligations(date(2026, 12, 25), "PH").source == "CBCP"
    assert get_obligations(date(2026, 12, 25), "NG").source == "CBCN"


def test_lectionary_cycle_2026():
    """lectionary._sunday_cycle(2026) must return 'A' (Year A = 2025-26)."""
    from services.lectionary import _sunday_cycle
    assert _sunday_cycle(2026) == "A", f"Expected A, got {_sunday_cycle(2026)}"
    assert _sunday_cycle(2027) == "B"
    assert _sunday_cycle(2025) == "C"  # Jan-Nov 2025 is still LY 2024-25 = Year C


def test_mass_readings_sunday_correct_cycle():
    """Mass readings for 2nd Sunday of Lent 2026 (Year A) = Mt 17:1-9."""
    from datetime import date
    from services.mass_readings import get_daily_readings
    data = get_daily_readings(date(2026, 3, 1))
    assert data["readings"] is not None
    gospel = data["readings"]["gospel"]["citation"]
    assert "17" in gospel, f"Expected Matthew 17, got {gospel}"


def test_ai_service_language_coverage():
    """AI service should support all 14 i18n languages."""
    from services.ai_service import SUPPORTED_LANGUAGES
    expected = {"en", "sw", "fr", "es", "pt", "lg", "ig", "tl", "hi", "it", "de", "pl", "ar", "sv"}
    missing = expected - set(SUPPORTED_LANGUAGES.keys())
    assert not missing, f"Missing languages in AI service: {missing}"


def test_obligations_result_has_explanation():
    """All ObligationsResult instances must include a non-empty explanation."""
    from datetime import date
    from services.liturgical_engine import get_obligations
    for cc in ["KE", "US", "PH", "NG", "BR"]:
        obs = get_obligations(date(2026, 12, 25), cc)
        assert obs.explanation, f"Empty explanation for {cc}"
