# ✝️ Jumuia — Parish Community

**Low-cost Catholic parish coordination for East Africa and the global diaspora.**

[![CI](https://github.com/gabrielmahia/jumuia/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielmahia/jumuia/actions/workflows/ci.yml)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Live](https://img.shields.io/badge/live-jumuia.streamlit.app-gold)](https://jumuia.streamlit.app)

**[→ Open the live platform](https://jumuia.streamlit.app)**

---

## What it is

A unified platform for parishioners, parish coordinators, catechists, priests, and administrators.
Built for communities across East Africa and globally — including those with basic phones
and limited internet connectivity.

Follows Catholic principles of **subsidiarity** (decisions at the lowest appropriate level)
and **synodality** (coordination with transparency).

---

## Three public entry points

| Entry | Who | What |
|-------|-----|------|
| 🗺️ **Find a Church** | Everyone | 40,000+ Catholic churches via OpenStreetMap |
| 📖 **Daily Prayers** | Everyone | Rosary, Divine Mercy, Stations, Mass readings |
| 🤖 **AI Assistant** | Everyone | 14 languages · liturgically aware · Gemini-powered |

---

## Platform map

| Page | Role | What it does |
|------|------|--------------|
| 🏠 Home | All | Simple public front door — three actions only |
| 🗺️ Find a Church | Parishioners | OSM search + manual submission + community verification |
| 📖 Daily Prayers | Parishioners | Rosary, Divine Mercy, Stations, liturgical calendar |
| 🤖 AI Assistant | All | Chat + translation (14 languages) + homily prep |
| ⛪ Sacraments | Coordinators | Baptism, Confirmation, Eucharist, Marriage, Anointing records |
| 👥 Small Communities | Coordinators | SCC roster, meeting records, attendance (Jumuia model) |
| 📚 Catechists | Coordinators | Certification tracking, training records |
| 🫶 Pastoral Care | Coordinators | Visitation, hospital, grief, care records |
| 📘 Formation | Coordinators | RCIA stages, Faith Formation tracking |
| 💰 Parish Giving | Coordinators | M-Pesa + manual giving records |
| 📋 Liturgy | All | Liturgical calendar, Mass planner |
| 📊 Parish Health | Admins | Sacramental and community metrics |
| ⚖️ Justice & Care | All | Local outreach and community action |
| 📋 Transparency | Admins | Parish accountability dashboard |
| 🌏 Diaspora | All | Global Catholic community connections |
| 📱 USSD Setup | Admins | Configure USSD access for feature-phone parishioners |
| ⚙️ Settings | All | Accessibility, language, data preferences |
| 📁 Admin & Data | Admins | Export, import, Google Sheets connection |

---

## Infrastructure

```
Streamlit Cloud (web app — free tier)
  ↕  Google Sheets (data persistence — Apps Script)
  ↕  Gemini (AI — free tier + fallback cascade)
  ↕  OpenStreetMap (maps — free, open)

Google Cloud Run (USSD webhook — free tier)
  ↕  Africa's Talking (USSD/SMS — pay per use)
  ↕  Shared data via Google Sheets
```

**Cost target: $0–10/month** until real parish usage validates scaling.

---

## USSD Access (Africa's Talking)

Feature-phone parishioners in rural Kenya can dial your registered shortcode:

```
*XXX#
1. Find Parish
2. Mass Times
3. Give via M-Pesa
4. Today's Reading
5. Emergency Contacts
```

USSD webhook deploys to Cloud Run separately from the Streamlit app.
See `docs/CLOUD_RUN_DEPLOY.md` for instructions.

---

## Configuration (Streamlit Secrets)

Add to `.streamlit/secrets.toml` (local) or Streamlit Cloud → Settings → Secrets:

```toml
GOOGLE_API_KEY = "AIza..."              # Gemini AI
SHEETS_ENDPOINT = "https://script..."   # Google Sheets Apps Script URL
AFRICASTALKING_USERNAME = "sandbox"     # Africa's Talking
AFRICASTALKING_API_KEY = "atsk_..."
```

See `.env.example` for all variables.
See `docs/SHEETS_SETUP.md` for Google Sheets setup.
See `docs/CLOUD_RUN_DEPLOY.md` for USSD deployment.

---

## Admin Diagnostics

To see AI/Sheets status without exposing it to the public:

`https://jumuia.streamlit.app/AI_Assistant?admin=true`

Shows: API key status, active model, SHEETS_ENDPOINT configured, last error.

---

## Running locally

```bash
git clone https://github.com/gabrielmahia/jumuia
cd jumuia
cp .env.example .env   # fill in GOOGLE_API_KEY + SHEETS_ENDPOINT
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```bash
pytest tests/ -v
ruff check app.py pages/ services/
```

---

## Architectural lineage

```
GospelMap (2024–2025)
  ↓  prototype: church finder, justice network, accountability
Catholic Network Tools (2025)
  ↓  full platform: liturgy, AI, sacraments, SCCs, USSD
Jumuia (2025–present)
  ↓  production: AMECEA SCC model + USSD + M-Pesa + diaspora
```

Named after the AMECEA tradition of Small Christian Communities (SCCs).

---

## License

**CC BY-NC-ND 4.0** — Non-commercial. No derivatives. Attribution required.  
Contact: contact@aikungfu.dev  
© 2026 Gabriel Mahia / MNG ONLINE LLC
