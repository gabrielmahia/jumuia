-e # ✝️ Catholic Network Tools

**Decision support infrastructure for the global Catholic Church.**

[![CI](https://github.com/gabrielmahia/catholic-network-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielmahia/catholic-network-tools/actions/workflows/ci.yml)
[![Live Data](https://img.shields.io/badge/Live%20Data-open.er-api.com%20%C2%B7%20Safaricom%20ping-00b4d8)](#catholic-network-tools)
[![Tests](https://img.shields.io/badge/tests-56%20passing-brightgreen)](#testing)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Live](https://img.shields.io/badge/live-catholicparishsteward.streamlit.app-gold)](https://jumuia.streamlit.app)

**[→ Open the live platform](https://jumuia.streamlit.app)**

---

## What it is

A unified platform serving parishioners, parish coordinators, catechists, priests, and diocesan administrators. Built for communities across East Africa and globally — including those with basic phones and limited internet connectivity.

The platform follows Catholic principles of **subsidiarity** (decisions at the lowest appropriate level) and **synodality** (coordination across levels with transparency). Privacy-first design: individuals control data visibility; coordinators see aggregated data voluntarily shared upward.

---

## Platform map

| Page | Role | What it does |
|------|------|--------------|
| 🏠 Home | All | Parish identity, SMS access number, language selector |
| 🔍 Find a Church | Parishioners | OpenStreetMap search — any city globally, real-time |
| 🙏 Daily Prayers | Parishioners | Rosary, Divine Mercy, Stations, liturgical readings |
| 🤖 AI Assistant | All | Chat, translation (14 languages), homily prep, parish insights |
| ⛪ Sacraments | Coordinators | Baptism, Confirmation, Eucharist, Marriage, Anointing records |
| 👥 Small Communities | Coordinators | SCC roster, meeting records, attendance tracking |
| 📚 Catechists | Coordinators | Certification tracking, training records |
| 🫶 Pastoral Care | Coordinators | Homebound visits, grief support, mentoring, new members |
| 📖 Formation & RCIA | Coordinators | RCIA cohorts, formation tracks |
| 💝 Parish Giving | All | Contribution tracking, campaign management |
| 📅 Liturgy & Calendar | All | Liturgical engine: season, readings, fasting rules by country |
| 🏥 Parish Health | Coordinators | Pastoral Crisis Index, health metrics |
| ⚖️ Justice & Care | All | Social justice campaigns, advocacy coordination |
| 🌍 Global Diaspora | All | Community connection across diaspora networks |
| 🔍 Transparency | Diocese | Accountability dashboard |
| ⚙️ Admin & Data | Admin | Export, governance, data management |
| 📱 Set Up USSD | Admin | SMS/USSD configuration for basic phone access |

---

## Technical highlights

**Liturgical engine** — Correct Sunday cycle (A/B/C), season detection, colour, fasting and abstinence rules per episcopal conference (US, Kenya, Philippines, Nigeria, and others). Fixes the common bug of hardcoding Year A regardless of actual cycle.

**AI assistant with real-time search grounding** — Gemini 2.0 Flash with Google Search grounding enabled. The model searches Google in real-time when questions need current information (current pope, today's readings, recent Vatican news). Falls back to Gemini 1.5 with dynamic retrieval threshold, then to demo responses. Maintains a `_current_catholic_facts()` context block so the model is always grounded in the actual present.

**Role-based access** — Five roles (parishioner → coordinator → catechist → priest → diocese). Role gates use `require_role()` via `services/roles.py`. A fixed vulnerability: the original gates wrapped `st.stop()` in broad `except Exception` clauses, silently swallowing the stop signal. All 5 gated pages now use narrow `ImportError`-only guards.

**Multilingual** — 14 languages: English, Kiswahili, French, Spanish, Portuguese, Luganda, Igbo, Tagalog, Polish, Italian, German, Arabic, Hindi, Swedish. AI translation covers all 14.

**SMS / USSD** — Africa's Talking integration for basic phone access. Parish data synced; alert thresholds configurable per diocese.

**Parish directory** — Dual-source: OpenStreetMap Overpass API (global, real-time) + community-verified local database. 3-tier deduplication: OSM element ID → coordinate rounding (±11m) → name+address prefix.

---

## Architecture

```
pages/                    ← 17 Streamlit pages (named to control sidebar order)
  home.py
  _01_Find_Church.py      ← OSM Overpass + Nominatim, 3-tier dedup
  06_AI_Assistant.py      ← Gemini + Google Search grounding, 14 languages
  07_Parish_Directory.py
  10_Sacraments.py        ← Role-gated (coordinator+)
  _00_Liturgy.py          ← Liturgical engine UI
  ...

services/
  ai_service.py           ← Gemini API, model discovery, quota cascade
  lectionary.py           ← Sunday cycle (A/B/C), mass readings
  liturgical_engine.py    ← Season, colour, fasting by episcopal conference
  roles.py                ← Role definitions and enforcement
  privacy.py              ← Privacy-first data visibility controls
  i18n.py                 ← 14-language translation strings
  sheets.py               ← Google Sheets sync
  magisterial.py          ← Query classification, sensitive topic logging
  ...

gospelmap/
  church_search.py        ← Overpass API multi-strategy search with failover
  lectionary.py

tests/
  test_services.py        ← 56 tests: liturgy, lectionary, AI, roles, privacy

.github/
  workflows/ci.yml        ← Ruff lint + pytest on push/PR
```

---

## Quick start

```bash
git clone https://github.com/gabrielmahia/catholic-network-tools
cd catholic-network-tools
pip install -r requirements.txt
streamlit run home.py
```

The app runs at `http://localhost:8501`. AI features require a `GOOGLE_API_KEY` (Gemini) in Streamlit secrets or environment.

**Streamlit secrets (`.streamlit/secrets.toml`):**
```toml
GOOGLE_API_KEY = "your-gemini-key"
GOOGLE_SHEETS_KEY = "your-sheets-key"  # optional
AFRICAS_TALKING_KEY = "your-at-key"    # optional, for SMS
```

---

## Testing

```bash
pytest tests/ -v
# 56 tests: liturgical cycle, lectionary readings, AI language coverage,
#           role enforcement, privacy controls, magisterial classification
```

---

## Governance

- **License:** CC BY-NC-ND 4.0 — study and fork permitted; commercial use and redistribution of modified versions require written permission
- **Security:** See [SECURITY.md](SECURITY.md) — report via email, not public issues
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **IP policy:** See [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md)
- **Contact:** contact@aikungfu.dev

---

*Built with subsidiarity and synodality as design principles.*
*Serving 1.3 billion Catholics — one parish at a time.*
---

## Portfolio

Part of a suite of civic and community tools built by [Gabriel Mahia](https://github.com/gabrielmahia):

| App | What it does |
|-----|-------------|
| [🌊 Mafuriko](https://floodwatch-kenya.streamlit.app) | Flood risk & policy enforcement tracker — Kenya |
| [💧 WapiMaji](https://wapimaji.streamlit.app) | Water stress & drought intelligence — 47 counties |
| [🏛️ Macho ya Wananchi](https://macho-ya-wananchi.streamlit.app) | MP voting records, CDF spending, bill tracker |
| [🌾 JuaMazao](https://juamazao.streamlit.app) | Live food price intelligence for smallholders |
| [🏦 ChaguaSacco](https://chaguasacco.streamlit.app) | Compare Kenya SACCOs on dividends & loan rates |
| [🛡️ Hesabu](https://hesabu.streamlit.app) | County budget absorption tracker |
| [🗺️ Hifadhi](https://hifadhi.streamlit.app) | Riparian encroachment & Water Act compliance map |
| [💰 Hela](https://helaismoney.streamlit.app) | Chama management for the 21st century |
| [💸 Peleka](https://tumapesa.streamlit.app) | True cost remittance comparison — diaspora to Kenya |
| [📊 Msimamo](https://easystocktrader.streamlit.app) | Macro risk & trade intelligence terminal |
| [🦁 Dagoretti](https://dagoretti-high-school-community-app.streamlit.app) | Alumni atlas & community hub for Dagoretti High |
| [⛪ Jumuia](https://jumuia.streamlit.app) | Catholic parish tools — church finder, pastoral care |

