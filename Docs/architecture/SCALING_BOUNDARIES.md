# Scaling Boundaries — Catholic Spiritual OS

## Current Limits (Demo Mode)

### Technical Constraints

**Storage**:
- **Type**: In-memory (Streamlit session state)
- **Persistence**: None (resets on page refresh)
- **Capacity**: Limited by server RAM (~100MB per session)
- **Implication**: Not suitable for production use

**Concurrency**:
- **Users**: ~50 simultaneous users (Streamlit Cloud free tier)
- **Response Time**: 2-5 seconds under light load
- **Breaking Point**: Degrades significantly above 50 users

**Data Volume**:
- **Parish Members**: Demo shows ~85 members (hard-coded)
- **Real Limit**: Would max out around 500 members in current architecture
- **SCCs**: Demo shows 8 SCCs, could handle ~50 before performance issues

**API Dependencies**:
- **Church Calendar API**: Public, rate-limited (unknown exact limits)
- **Fallback**: Implemented for offline scenarios
- **Risk**: External dependency for critical liturgical data

---

## Phase 2: Production Parish (Single Parish Scale)

### Target: 500-2,000 Members

**Database**:
- **Engine**: PostgreSQL 13+
- **Storage**: 10GB allocated
- **Backup**: Daily, 7-day retention
- **Expected Growth**: ~1GB per year

**Hosting**:
- **Platform**: Digital Ocean / AWS / GCP
- **Instance**: 2 vCPU, 4GB RAM
- **Cost**: ~$50/month

**Performance**:
- **Response Time**: <1 second for typical queries
- **Concurrent Users**: 100-200
- **Batch Operations**: Parish reports in <10 seconds

**Features Unlocked**:
- Real parish member database
- Sacramental records
- Giving history (5 years)
- Volunteer scheduling
- SCC coordination at scale

**Scaling Strategy**:
- Read replicas for reporting
- CDN for static assets
- Caching for liturgical calendar (refresh daily)

---

## Phase 3: Diocesan Scale (50-200 Parishes)

### Target: 25,000-200,000 Members

**Database**:
- **Engine**: PostgreSQL with partitioning
- **Storage**: 500GB allocated
- **Architecture**: Multi-tenant (one database, parish-scoped queries)
- **Backup**: Continuous archiving, 30-day point-in-time recovery

**Hosting**:
- **Platform**: AWS/GCP with multi-AZ
- **Instance**: 8 vCPU, 32GB RAM
- **CDN**: Cloudflare for global distribution
- **Cost**: ~$500-1,000/month

**Performance**:
- **Response Time**: <2 seconds for complex aggregations
- **Concurrent Users**: 500-1,000
- **Batch Reporting**: Diocesan reports in <60 seconds

**Features Unlocked**:
- Diocese-wide statistics
- Cross-parish resource sharing
- Clergy assignment tracking
- Multi-parish event coordination
- Diocesan catechist certification management

**Scaling Challenges**:
- **Aggregation Complexity**: Sum across 200 parishes = slow queries
- **Solution**: Pre-computed materialized views, refresh nightly
- **Data Privacy**: Strict row-level security, audit all diocese-level queries
- **Customization**: Each diocese has unique requirements (custom fields, workflows)

---

## Phase 4: National/Global Scale (Multiple Dioceses)

### Target: 1M+ Members, 500-5,000 Parishes

**Database**:
- **Engine**: PostgreSQL with Citus (distributed)
- **Architecture**: Sharded by diocese/country
- **Storage**: 5TB+ distributed
- **Backup**: Geo-replicated

**Hosting**:
- **Platform**: AWS/GCP multi-region
- **Instances**: 20+ servers across regions
- **Load Balancing**: Global traffic manager
- **Cost**: $5,000-20,000/month

**Performance**:
- **Response Time**: <3 seconds globally
- **Concurrent Users**: 10,000+
- **Batch Reporting**: National reports in <10 minutes

**Features Unlocked**:
- Global Catholic network
- Cross-diocese vocations sharing
- International mission coordination
- Federated authentication (SSO with diocese systems)
- Multi-language support (English, Spanish, French, Swahili, Portuguese)

**Scaling Challenges**:
- **Data Sovereignty**: Some countries require data stored locally
- **Solution**: Regional deployments, federation protocol
- **Heterogeneity**: Different dioceses use different software
- **Solution**: API integrations, not replacing existing systems
- **Cost Management**: $20k/month unsustainable for Church budgets
- **Solution**: Hybrid model (core features free, premium features paid)

---

## Specific Limits by Feature

### Small Christian Communities (SCCs)

| Scale | SCCs | Performance | Notes |
|-------|------|-------------|-------|
| **Demo** | 8 | Instant | Hard-coded data |
| **Single Parish** | 50-100 | <1s | Direct PostgreSQL queries |
| **Diocese** | 5,000 | <5s | Indexed queries, caching |
| **National** | 50,000 | <10s | Distributed queries, materialized views |

**Breaking Point**: ~100,000 SCCs without horizontal scaling

### Catechist Certification

| Scale | Catechists | Performance | Notes |
|-------|------------|-------------|-------|
| **Demo** | 1 | Instant | Hard-coded |
| **Single Parish** | 20-50 | <1s | Simple queries |
| **Diocese** | 500-1,000 | <3s | Need indexing on certification_status |
| **National** | 10,000+ | <10s | Materialized views for renewal reporting |

**Breaking Point**: ~50,000 active certifications without sharding

### Liturgical Calendar

| Scale | Requests/Day | Performance | Notes |
|-------|--------------|-------------|-------|
| **Demo** | 100 | 2-5s | Direct API call |
| **Production** | 10,000 | <500ms | Cached (refresh daily) |
| **Diocese** | 100,000 | <100ms | CDN + cache |
| **National** | 1M+ | <50ms | Edge caching, pre-generate |

**Strategy**: Cache all liturgical data for current year, serve from CDN

---

## Offline-First Considerations

### Why Offline Matters (Kenya Context)

- **Internet Penetration**: 88% in urban areas, <40% in rural areas
- **Connectivity**: Intermittent in rural parishes
- **Cost**: Data expensive for low-income users
- **Resilience**: Must work during network outages

### Offline Strategy (Phase 2+)

**Service Workers**:
- Cache app shell (HTML/CSS/JS)
- Cache liturgical calendar (30 days ahead)
- Cache parish data (last sync)

**IndexedDB**:
- Store parish member records locally
- Queue transactions (create/update/delete)
- Sync when connection available

**Sync Protocol**:
- Last-write-wins for simple edits
- Conflict resolution UI for complex changes
- Background sync for non-critical updates

**Performance**:
- Initial load: 5MB download (app + data)
- Subsequent loads: <100KB (delta sync)
- Works fully offline after first load

---

## Cost Projection

### Phase 2: Single Parish ($50-100/month)
- Hosting: $50
- Database backups: $10
- SSL certificate: Free (Let's Encrypt)
- Monitoring: Free (basic tier)

### Phase 3: Diocesan ($500-1,500/month)
- Hosting: $500
- Database (managed PostgreSQL): $200
- CDN: $100
- Monitoring & logging: $100
- Backups & archiving: $200
- Support & maintenance: $400

### Phase 4: National ($5,000-20,000/month)
- Multi-region hosting: $3,000
- Distributed database: $2,000
- CDN & edge compute: $1,000
- Security & compliance: $1,000
- 24/7 monitoring: $500
- Backups & disaster recovery: $1,000
- Engineering support: $11,500

**Sustainability Model**:
- Core features: Free (personal, small parishes)
- Premium features: Paid (diocesan analytics, integrations)
- Large dioceses: Subscription ($1,000-5,000/year)
- Grants: Catholic funding organizations

---

## Non-Functional Requirements

### Security

**Authentication**:
- Phase 2: Username/password (bcrypt)
- Phase 3: OAuth 2.0 / SAML (diocese SSO)
- Phase 4: Federated authentication

**Encryption**:
- At rest: AES-256
- In transit: TLS 1.3
- Backups: Encrypted before upload

**Audit**:
- All data changes logged
- Immutable audit trail
- Retained for 7 years

### Compliance

**GDPR** (European parishes):
- Right to access: Export all personal data
- Right to deletion: Hard delete on request
- Consent management: Opt-in for all processing

**Data Localization** (various countries):
- Store data in-country when required
- Regional deployments
- Cross-border data transfer agreements

---

## When to Stop Scaling

**Upper Bound**: ~10 million active users globally

**Why Stop There**:
- Beyond this scale, diocese software fragmentation is too high
- Better to integrate with existing systems (ParishSOFT, etc.) than replace
- Catholic Church has ~1.3 billion members, but only ~200 million actively engaged
- 10M = 5% of active Catholics = realistic TAM

**Exit Strategy**:
- Open-source the code (already CC BY-NC-ND)
- Publish integration APIs
- Allow self-hosting by large dioceses
- Transfer stewardship to Catholic tech consortium

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Next Review**: Q3 2026 (after Phase 2 launch)
