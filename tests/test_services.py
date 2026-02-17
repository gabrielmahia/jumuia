"""
Tests — Catholic Network Tools
Smoke tests + unit tests for all services.
Run: pytest tests/ -v
"""
import os
import sqlite3
import sys
import tempfile
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
        translate_text, homily_helper, generate_parish_insights,
        bot_respond, SUPPORTED_LANGUAGES
    )
    assert "en" in SUPPORTED_LANGUAGES
    assert "sw" in SUPPORTED_LANGUAGES
    assert "fr" in SUPPORTED_LANGUAGES


def test_directory_service_imports():
    from services.directory_service import (
        init_db, search_parishes, get_stats, sync_gcatholic
    )
    assert callable(init_db)


def test_mpesa_service_imports():
    from services.mpesa_service import (
        get_access_token, initiate_stk_push, handle_callback,
        get_giving_summary, live_activation_checklist
    )
    assert callable(initiate_stk_push)


def test_whatsapp_service_imports():
    from services.whatsapp_service import (
        parse_at_inbound, parse_twilio_inbound,
        activation_status, _detect_language_simple
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
    from services.directory_service import init_db, search_parishes, DB_PATH
    import services.directory_service as ds
    import pathlib

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
    import os
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
    import pathlib
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
