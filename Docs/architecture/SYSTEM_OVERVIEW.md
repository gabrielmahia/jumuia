# Catholic Spiritual OS — System Overview

## Vision

A **personal formation platform for the global Catholic Church** that respects the nested nature of Church life: individual disciples nested within parishes, parishes within dioceses, dioceses within the universal Church.

Like Google Maps, users can "zoom in" to their personal spiritual life or "zoom out" to see parish, diocesan, or global Church networks.

---

## Five-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  E (RESILIENCE) — Crisis Response & Faith+Civic Action  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  C (GLOBAL) — Universal Church Network            │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  B (DIOCESE) — Multi-Parish Governance       │  │  │
│  │  │  ┌───────────────────────────────────────┐   │  │  │
│  │  │  │  A (PARISH) — Community Coordination  │   │  │  │
│  │  │  │  ┌─────────────────────────────────┐  │   │  │  │
│  │  │  │  │  D (PERSONAL) — Your Rule of    │  │   │  │  │
│  │  │  │  │              Life & Formation    │  │   │  │  │
│  │  │  │  └─────────────────────────────────┘  │   │  │  │
│  │  │  └───────────────────────────────────────┘   │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### D — Personal (Individual Disciple)
**Status**: Core features implemented (v0.1)

**Features**:
- Rule of Life builder (daily/weekly spiritual practices)
- Sacramental milestone tracking
- Journaling (Examen, Lectio Divina)
- Liturgical calendar integration
- Personal formation goals

**Privacy**: Full control over data sharing with parish/diocese

### A — Parish (Local Community)
**Status**: Framework implemented, expanding features

**Features**:
- Small Christian Communities (SCCs) management
- Parish bulletin and events
- Catechist certification tracking
- Volunteer coordination
- Giving and stewardship
- Aggregated metrics (respects individual privacy)

**Privacy**: Aggregated data only, no individual tracking without consent

### B — Diocese (Regional Church)
**Status**: Roadmap phase

**Features**:
- Multi-parish governance view
- Diocesan-level sacramental records
- Clergy assignments
- Statistical reporting
- Policy compliance
- Resource allocation

**Privacy**: Aggregate statistics only, strict access controls

### C — Global (Universal Church)
**Status**: Research phase

**Features**:
- Federated coordination across dioceses
- Global Catholic network
- Mission opportunities (GospelMap integration)
- Vocations tracking
- International solidarity projects

**Privacy**: Opt-in federation, encrypted data sharing

### E — Resilience (Crisis Response)
**Status**: Framework exists, needs expansion

**Features**:
- Faith + civic response coordination
- Disaster preparedness
- Conflict resolution and peacebuilding
- Youth unemployment programs (Kenya context)
- Mission hospital coordination

**Context**: Addresses real challenges in Kenya and Africa

---

## Technical Architecture

### Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.11+
- **Database**: SQLite (demo), PostgreSQL (production roadmap)
- **Deployment**: Streamlit Cloud (GitHub integration)
- **APIs**: Church Calendar API, GospelMap (future)

### Key Modules

#### Core Domain (`src/spiritual_os/`)
- `models.py` — User, Parish, Diocese data models
- `aggregation.py` — Privacy-preserving aggregation engine
- `auth.py` — Role-based access control
- `database.py` — Data persistence layer
- `liturgical_calendar.py` — Catholic liturgical calendar integration

#### Domain Modules (`src/spiritual_os/domain/`)
- `parish.py` — Parish management
- `diocese.py` — Diocesan structures
- `liturgy.py` — Liturgical data
- `sacraments.py` — Sacramental records
- `scc.py` — Small Christian Communities
- `catechist.py` — Catechist certification
- `journal.py` — Spiritual journaling
- `rule_of_life.py` — Personal formation plans

#### UI Pages (`app/pages/`)
1. Home
2. Sacraments
3. Pastoral Care
4. Justice & Social Action
5. Formation
6. Stewardship
7. Admin
8. Global Network
9. **Liturgy of the Day** (NEW)
10. **Small Christian Communities** (NEW)
11. **Catechist Certification** (NEW)

---

## Data Governance

### Demo vs Real

**Current Status: DEMO MODE**
- All data is synthetic
- Demo accounts (password: "demo")
- Safe for testing and exploration

**Production Roadmap**:
- Real parish database with privacy controls
- Encryption at rest and in transit
- Audit trails for all data changes
- Parish data ownership and portability

### Privacy Principles

1. **Personal Control**: Individuals opt-in to parish/diocese aggregation
2. **Aggregate Only**: Higher levels see statistics, never individual records
3. **Data Ownership**: Parishes own their data
4. **No Surveillance**: Tool authors cannot access parish data
5. **Portability**: Export in standard formats (CSV, JSON)

---

## User Roles

| Role | Description | Access Level |
|------|-------------|--------------|
| **Individual** | Regular parishioner | Personal data only |
| **Parish Coordinator** | Parish staff/volunteer coordinator | Parish aggregated data |
| **Catechist** | Religious education teacher | Assigned students only |
| **Diocesan Leader** | Bishop, vicar, chancellor | Diocese aggregate statistics |
| **Global Coordinator** | International mission coordinator | Global opt-in data |
| **Crisis Responder** | Emergency response coordinator | Crisis-related data |

---

## Kenya/Africa Context

### Why This Matters for Kenya

1. **Small Christian Communities (SCCs)**
   - 45,000+ SCCs in Kenya alone
   - Primary pastoral structure
   - Need coordination tools

2. **Vocations Crisis**
   - Only 17 diocesan priests in some dioceses
   - Heavy reliance on missionaries
   - Need vocations tracking

3. **Youth Unemployment**
   - Church-led skills training
   - Job placement coordination
   - Social enterprise support

4. **Mission Hospitals**
   - 94-year-old hospitals closing (e.g., Mumias)
   - Need coordination and financial management
   - Integration with parish stewardship

5. **Ethnic Reconciliation**
   - Post-election violence healing
   - Peacebuilding through SCCs
   - Cross-ethnic parish solidarity

---

## Roadmap

### Phase 1: Demo Validation (Current)
✅ Core personal features (Rule of Life, journaling, sacraments)  
✅ Parish framework  
✅ Liturgical calendar integration  
✅ SCC management module  
✅ Catechist certification framework  
✅ Trust transparency (DEMO vs REAL labeling)

### Phase 2: Production Database (Q2 2026)
⏳ SQLite → PostgreSQL migration  
⏳ Real parish member CRUD  
⏳ Giving and stewardship backend  
⏳ Volunteer scheduling system  
⏳ Background check tracking

### Phase 3: Diocese Integration (Q3 2026)
⏳ Multi-parish aggregation  
⏳ Diocesan reporting dashboards  
⏳ Clergy assignment tracking  
⏳ Statistical compliance

### Phase 4: Global Federation (Q4 2026)
⏳ Opt-in global network  
⏳ GospelMap full integration  
⏳ International solidarity projects  
⏳ Vocations sharing across dioceses

---

## Deployment

### Current: Streamlit Cloud

**URL**: https://catholicparishsteward.streamlit.app/

**Pipeline**: GitHub push → Streamlit Cloud auto-deploy

**Requirements**:
- Python 3.11+
- See `requirements.txt`

### Local Development

```bash
git clone https://github.com/gabrielmahia/catholic-network-tools
cd catholic-network-tools
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Production Considerations (Future)

- **Database**: PostgreSQL with replication
- **Hosting**: AWS/GCP for data residency requirements
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Backup**: Daily encrypted backups, 7-year retention
- **Audit**: Immutable audit logs
- **Compliance**: GDPR, data localization laws

---

## Success Metrics

### Individual Impact
- Users with active Rule of Life: % daily practice consistency
- Sacramental milestone tracking: % completion rate
- Spiritual journal entries: frequency and depth

### Parish Impact
- SCC participation rate
- Catechist certification rate
- Volunteer retention
- Giving consistency

### Diocesan Impact
- Cross-parish resource sharing
- Vocations pipeline growth
- Statistical reporting accuracy

### Global Impact
- Parishes connected globally
- Mission opportunities filled
- Solidarity projects funded

---

## Governance

**License**: CC BY-NC-ND 4.0  
**Owner**: Gabriel Mahia  
**Stewardship**: Community-owned for Catholic parishes

**Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md)  
**Security**: See [SECURITY.md](../SECURITY.md)  
**IP Policy**: See [IP_POLICY.md](IP_POLICY.md)

---

## Support

📖 **Documentation**: `Docs/`  
🐛 **Issues**: https://github.com/gabrielmahia/catholic-network-tools/issues  
💬 **Discussions**: https://github.com/gabrielmahia/catholic-network-tools/discussions  
✉️ **Security**: contact@aikungfu.dev (private)

---

**Version**: v0.1.0  
**Last Updated**: February 2026  
**Status**: Demo / Early Development
