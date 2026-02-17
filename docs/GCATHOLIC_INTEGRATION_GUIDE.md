# Parish Directory Integration Guide — 100K+ Parishes
## Catholic Network Tools

---

## Current State
- Seed data: ~30 parishes across Africa (demo)
- Database: SQLite (ready for full load)
- Schema: supports 100K+ rows efficiently

---

## Path to 100K+ Parishes — Ranked by Openness

### Option A: OpenStreetMap (Recommended — Start Here)

**Parishes available:** ~40,000–60,000 globally  
**License:** ODbL (open, attribution required)  
**API:** Overpass API (free, no registration)  
**Timeline to implement:** 2–4 hours

```python
# Sample Overpass query — Catholic churches in Kenya
import requests

query = """
[out:json][timeout:60];
area["name"="Kenya"]["admin_level"="2"]->.kenya;
(
  node["amenity"="place_of_worship"]["denomination"="catholic"](area.kenya);
  way["amenity"="place_of_worship"]["denomination"="catholic"](area.kenya);
);
out body;
"""

resp = requests.post(
    "https://overpass-api.de/api/interpreter",
    data={"data": query},
    timeout=60,
)
data = resp.json()

# Each element: id, lat, lon, tags{name, addr:*, phone, website, ...}
```

**Implementation path:**
1. Run Overpass query per country
2. Map OSM tags to `parishes` schema
3. Insert with `source='openstreetmap'`
4. Schedule monthly sync (GitHub Actions cron)

**Attribution required in UI:** "Parish data © OpenStreetMap contributors, ODbL"

---

### Option B: GCatholic.org (Most Complete — ToS Review Required)

**Parishes available:** ~100,000+ globally  
**License:** Not explicitly open — scraping requires ToS compliance review  
**API:** None — HTML scraping only

**Legal checklist (complete before implementing):**
- [ ] Read gcatholic.org/terms (or contact webmaster)
- [ ] Confirm non-commercial use is permitted
- [ ] Implement rate limiting (≥ 1 request/3 seconds)
- [ ] Set descriptive User-Agent: `CatholicNetworkTools/1.0 (contact@aikungfu.dev)`
- [ ] Respect `robots.txt`
- [ ] Cache aggressively — do not re-scrape unchanged pages

**Scraper activation:** Set `GCATHOLIC_ENABLED=true` in `.env` and implement
`_fetch_gcatholic_page()` in `services/_gcatholic_scraper.py`.

---

### Option C: Wikipedia Categories (Good for Cathedrals)

```
https://en.wikipedia.org/wiki/Category:Catholic_cathedrals_in_Kenya
```

Useful supplement for diocesan cathedrals and major basilicas.
Wikipedia API is open and well-documented.

---

### Option D: Manual Community Submissions

Build a simple form where coordinators submit their parish:
- Name, address, diocese, Mass times, contact
- Status: "pending review" until verified by a coordinator
- Maps to `source='manual'`, `verified=0` until confirmed

This is the most accurate long-term path (self-maintaining community data).

---

## Recommended Implementation Order

1. **Week 1:** Import Kenya + East Africa from OpenStreetMap (~2,000 parishes)
2. **Week 2:** Expand to all Africa via Overpass queries
3. **Week 3:** Add manual submission form for corrections/additions
4. **Month 2:** Evaluate GCatholic ToS for global expansion
5. **Ongoing:** Monthly OSM sync via GitHub Actions cron

---

## Database Performance at Scale

The current SQLite schema handles 100K+ rows well with:
- `name`, `country`, `diocese`, `city` columns indexed
- Full-text search via LIKE queries (sufficient for 100K)
- For 500K+: add FTS5 virtual table

```sql
-- Add FTS5 for fast full-text search at scale
CREATE VIRTUAL TABLE parishes_fts USING fts5(
    name, city, diocese, address,
    content='parishes', content_rowid='id'
);
```
