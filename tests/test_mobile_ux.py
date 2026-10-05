"""services/mobile_ux.py was added in one commit and never compiled: a block of CSS sat above the module docstring (IndentationError), and every caller wrapped the import
in `except Exception: pass`, so the mobile CSS and the Data Saver toggle silently never appeared. These tests make a broken file fail loudly instead."""
import ast
import importlib
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_every_tracked_python_file_compiles():
    files = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    bad = []
    for f in files:
        try:
            ast.parse((ROOT / f).read_text(encoding="utf-8"), filename=f)
        except SyntaxError as exc:
            bad.append(f"{f}:{exc.lineno} {exc.msg}")
    assert not bad, "files that cannot be compiled: " + "; ".join(bad)


def _load_with_fake_streamlit(monkeypatch):
    calls = []
    fake = types.ModuleType("streamlit")
    fake.markdown = lambda *a, **k: calls.append((a, k))
    fake.session_state = {}
    monkeypatch.setitem(sys.modules, "streamlit", fake)
    sys.modules.pop("services.mobile_ux", None)
    return importlib.import_module("services.mobile_ux"), calls


def test_mobile_ux_imports_and_exposes_its_api(monkeypatch):
    mod, _ = _load_with_fake_streamlit(monkeypatch)
    for name in ("inject_mobile_css", "data_saver_banner", "is_data_saver", "MOBILE_CSS"):
        assert hasattr(mod, name)


def test_css_is_one_well_formed_style_block_including_the_dark_mode_metric_rules(monkeypatch):
    mod, _ = _load_with_fake_streamlit(monkeypatch)
    css = mod.MOBILE_CSS.strip()
    assert css.startswith("<style>") and css.endswith("</style>") and css.count("<style>") == 1 and css.count("</style>") == 1
    assert "prefers-color-scheme: dark" in css and "stMetricLabel" in css and "#aaaaaa" in css


def test_inject_mobile_css_writes_the_css_as_html(monkeypatch):
    mod, calls = _load_with_fake_streamlit(monkeypatch)
    mod.inject_mobile_css()
    (args, kwargs), = calls
    assert args[0] == mod.MOBILE_CSS and kwargs == {"unsafe_allow_html": True}


def test_data_saver_defaults_to_off(monkeypatch):
    mod, _ = _load_with_fake_streamlit(monkeypatch)
    assert mod.is_data_saver() is False
