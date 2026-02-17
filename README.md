# ✝️ Catholic Network Tools

Decision support infrastructure for the global Catholic Church.

[![CI](https://github.com/your-org/catholic-network-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/catholic-network-tools/actions)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)

---

## What This Is

A Streamlit platform serving parishes, coordinators, priests, and diocesan leaders with:

| Module | Status | Description |
|--------|--------|-------------|
| 🤖 **AI Assistant** | ✅ Active | Translation, homily prep, insights, chat bot |
| 🗺️ **Parish Directory** | ✅ Active (seed) | Search 30+ seeded parishes; GCatholic rails ready |
| 🤝 **M-Pesa Giving** | 🧪 Sandbox | STK push giving; live activation in docs/ |
| 💬 **WhatsApp Bot** | 🔧 Framework | Full bot logic ready; webhook deployment required |

**Trust integrity:** All sandbox/demo data is clearly labeled. No simulated data is presented as real.

---

## Quick Start

```bash
git clone https://github.com/your-org/catholic-network-tools
cd catholic-network-tools

pip install -r requirements.txt

cp .env.example .env
# Add ANTHROPIC_API_KEY to .env

streamlit run app.py
```

The app runs at `http://localhost:8501`. AI features activate immediately with a valid API key.

---

## Feature Details

### AI Assistant (4 tools)
Built on Claude (Anthropic). Model tier per task:

| Tool | Model | Cost tier | What it does |
|------|-------|-----------|--------------|
| Translation | Haiku | Low | 6 languages, preserves liturgical terms |
| Homily Helper | Sonnet | Medium | Preparation notes — not finished homilies |
| Parish Insights | Haiku | Low | Plain-language summary from parish data |
| Chat Bot | Haiku | Low | Multilingual parish assistant |

### Parish Directory
- Local SQLite with seed data (Africa-focused sample)
- Schema supports 100K+ rows
- GCatholic integration: rails only — see `docs/GCATHOLIC_INTEGRATION_GUIDE.md`
- Fastest open-data path: OpenStreetMap via Overpass API (~40K parishes, free)

### M-Pesa Giving
- Safaricom Daraja API — sandbox active immediately
- STK Push (Lipa na M-Pesa prompt on customer phone)
- Transaction log with sandbox/live separation
- Live activation: 3–10 day Safaricom approval — see `docs/MPESA_INTEGRATION_GUIDE.md`

### WhatsApp Bot
- Full AI pipeline implemented (language detect → Claude Haiku → send reply)
- 6-language support with keyword-based language detection
- Multi-turn conversation store (SQLite)
- **Activation required:** Deploy FastAPI webhook companion service
- Full guide: `docs/WHATSAPP_BOT_GUIDE.md`
- Estimated time to sandbox-live: ~1 hour

---

## Languages Supported

English · Kiswahili · French · Spanish · Portuguese · Luganda

---

## Architecture

```
app.py  (Streamlit entry)
│
├── pages/
│   ├── 01_AI_Assistant.py     ← Chat, translation, homily, insights
│   ├── 02_Parish_Directory.py ← Search + GCatholic status
│   ├── 03_Giving.py           ← M-Pesa STK push
│   └── 04_Bot_Setup.py        ← WhatsApp activation guide
│
├── services/
│   ├── ai_service.py          ← Claude API (Haiku + Sonnet)
│   ├── directory_service.py   ← SQLite + GCatholic rails
│   ├── mpesa_service.py       ← Daraja API
│   └── whatsapp_service.py    ← AT/Twilio bot pipeline
│
├── data/
│   ├── parishes.db            ← SQLite (gitignored)
│   └── parishes_seed.csv      ← 30-parish seed (Africa)
│
└── docs/
    ├── WHATSAPP_BOT_GUIDE.md
    ├── MPESA_INTEGRATION_GUIDE.md
    └── GCATHOLIC_INTEGRATION_GUIDE.md
```

---

## Environment Variables

See `.env.example` for all required variables. Minimum to run:
```
ANTHROPIC_API_KEY=your_key
```

For M-Pesa sandbox:
```
MPESA_CONSUMER_KEY=...
MPESA_CONSUMER_SECRET=...
MPESA_PASSKEY=...
MPESA_ENV=sandbox
```

---

## Development

```bash
# Lint
ruff check services/ pages/ app.py --ignore E501,E402

# Test
pytest tests/ -v --cov=services

# Run
streamlit run app.py
```

---

## IP & Collaboration

This project is licensed under **CC BY-NC-ND 4.0**.
Commercial use and derivative works are not permitted without explicit written permission.

For licensing inquiries or partnership: contact@aikungfu.dev

See `docs/architecture/IP_POLICY.md` for full IP policy.

---

## Security

See [SECURITY.md](SECURITY.md). Do not open public issues for vulnerabilities.

---

*Built with institutional leverage and subsidiarity as design principles.*
*Serving 1.3 billion Catholics — one parish at a time.*
