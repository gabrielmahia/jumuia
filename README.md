# Catholic Network Tools 🙏

**Global community coordination platform for every aspect of parish life—from sacraments to social justice.**

Powered by **GitHub + Streamlit**. No servers. No fees. 100% community-owned.

Supporting parishes across **Africa, Latin America, Asia, North America, and beyond**—including Consolata Shrine (Westlands, Nairobi), All Saints Catholic Church (Virginia), and 100+ parishes worldwide.

**Status:** Alpha. Real parish data from 3 continents. Ready for your community to contribute.

---

## Overview

Catholic Network Tools provides offline-capable coordination, stewardship tracking, and resilience infrastructure for parishes across Kenya's diverse economic and geographic contexts—from Westlands' urban connectivity to Marallal's resource constraints.

### Core Capabilities

- **Coordination**: Attendance, events, volunteer scheduling
- **Stewardship**: Donation tracking, resource allocation with financial transparency
- **Resilience**: Offline-first data sync, SMS fallback for critical updates
- **Formation**: Sermon/teaching library, sacramental records (baptism, marriage, funeral)
- **Accessibility**: Works on basic Android, SMS-native interfaces

---

## ⚠️ TRUST & TRANSPARENCY

### DEMO vs REAL

This repository contains **real community infrastructure** and **demo/training components**. Clear separation:

- **REAL DATA ZONES** (audit trail required):
  - Attendance records
  - Donation/stewardship logs
  - Volunteer hours
  - Financial summaries
  - Sacramental records

- **DEMO/TRAINING ZONES** (synthetic, for UI testing):
  - Sample parish data
  - Fake volunteer profiles
  - Synthetic donation amounts

**Rule:** Real and demo data are in **separate environments**. UI/exports clearly label mode.

### Financial Disclaimer

Donation tracking and stewardship reports are operational tools, **not replacement for formal parish accounting**. Diocese retains canonical and legal authority over all financial records. This tool aids coordination; does not replace sacramental authority or financial reconciliation.

### AS-IS Statement

This tool is provided **as-is** for community coordination. No warranty of fitness for operational deployment without parish and diocesan review. All deployments require local data governance approval.

### Ownership & Attribution

**Ownership**: Catholic Network Tools belongs to the community of parishes using it. Code is governed under CC BY-NC-ND 4.0 to prevent commercial extraction.

**Contributors**: See CONTRIBUTORS.md. Contributions require a Contributor License Agreement (CLA) to protect community stewardship while retaining contributor rights.

**Attribution**: All parish data, volunteer records, and financial tracking must be attributed to contributing parishes.

---

## Quick Start

### For Parish Coordinators (Westlands / Urban)

```bash
git clone https://github.com/gabrielmahia/catholic-network-tools.git
cd catholic-network-tools
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make dev
```

Then open http://localhost:8000

### For Field Chaplains (Marallal / Remote)

1. **Install offline mode:**
   ```bash
   pip install -e .[offline]
   ```

2. **Initialize local parish database:**
   ```bash
   make init-parish --parish="Marallal St. Mary"
   ```

3. **SMS gateway setup:** See `Docs/guides/SMS_SETUP.md`

---

## Architecture

- **Offline-first**: Works 7+ days disconnected, syncs on reconnect
- **CRDT-based conflict resolution**: No data loss on simultaneous edits
- **Event-sourced audit trail**: Every change logged for transparency
- **Multi-mode UI**: Web (Svelte), SMS (Africa's Talking), API (FastAPI)

See `Docs/architecture/DESIGN.md` for full architecture.

---

## IP & Collaboration

This repository is protected under **CC BY-NC-ND 4.0** to preserve community control and prevent commercial extraction.

- **Community use**: Unlimited within Catholic institutions
- **Forks**: Permitted only under same CC BY-NC-ND license
- **Commercial use**: Not permitted without explicit CLA amendment
- **Modifications**: Permitted, must remain under CC BY-NC-ND

All contributors must sign the **Contributor License Agreement** (CLA) before merge. See `CONTRIBUTING.md`.

---

## Security & Vulnerability Reporting

**DO NOT open public issues for security concerns.**

If you discover a vulnerability:

1. **DO NOT** create a public issue or PR
2. **Email directly** to: `contact@aikungfu.dev`
3. Include: description, steps to reproduce, impact assessment
4. Allow 48 hours for response

See `SECURITY.md` for full policy.

---

## License

This work is licensed under the **Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International** (CC BY-NC-ND 4.0).

- You may share and copy the material under these terms
- You must give appropriate credit
- You may not use it for commercial purposes
- You may not distribute modified versions

See `LICENSE` file for full terms.

---

## Community

- **Contributing**: See `CONTRIBUTING.md`
- **Code of Conduct**: See `CODE_OF_CONDUCT.md`
- **Issues**: Report bugs via GitHub Issues or email contact@aikungfu.dev
- **Discussions**: GitHub Discussions for feature ideas and architecture debate

---

## GitHub About (Recommended)

**Description:**  
Community toolkit for Catholic parish coordination, stewardship, and resilience across Kenya. Offline-capable, SMS-integrated, open-licensed.

**Website:**  
(To be added when live deployment available)

**Topics:**  
`catholic` `community-infrastructure` `parish-coordination` `kenya` `offline-first` `stewardship` `resilience` `open-source` `crdt` `event-sourcing` `civic-tech` `faith-tech` `volunteer-management` `sacramental-records`

---

## Acknowledgments

This tool is built in service to Catholic communities across Kenya, with deep respect for diocesan authority, canonical governance, and the spiritual mission of the Church.
