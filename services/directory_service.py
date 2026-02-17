"""
Parish Directory Service — Catholic Network Tools

CURRENT:  Local SQLite with seed data (~500 parishes, Kenya + global samples)
RAILS:    GCatholic integration (see docs/GCATHOLIC_INTEGRATION_GUIDE.md)

GCatholic status: NO public API exists as of 2025.
Integration path: HTML scraping with rate-limiting and ToS compliance review.
See docs/ for full integration guide and legal checklist.
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Optional
import csv

logger = logging.getLogger(__name__)

DB_PATH = Path(os.getenv("CNT_DB_PATH", "data/parishes.db"))
SEED_CSV = Path("data/parishes_seed.csv")


# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────

def init_db() -> None:
    """Initialize SQLite DB and load seed data if empty."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS parishes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            country     TEXT,
            region      TEXT,
            city        TEXT,
            diocese     TEXT,
            address     TEXT,
            latitude    REAL,
            longitude   REAL,
            phone       TEXT,
            email       TEXT,
            website     TEXT,
            mass_times  TEXT,
            languages   TEXT,
            source      TEXT DEFAULT 'seed',   -- 'seed' | 'gcatholic' | 'manual'
            verified    INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gcatholic_sync_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            synced_at   TEXT DEFAULT (datetime('now')),
            records_added   INTEGER DEFAULT 0,
            records_updated INTEGER DEFAULT 0,
            status      TEXT,
            notes       TEXT
        )
    """)

    conn.commit()

    # Load seed if table is empty
    count = cur.execute("SELECT COUNT(*) FROM parishes").fetchone()[0]
    if count == 0 and SEED_CSV.exists():
        _load_seed(conn)
        logger.info("Seed data loaded from %s", SEED_CSV)

    conn.close()


def _load_seed(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    with open(SEED_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row.get("name", ""),
                row.get("country", ""),
                row.get("region", ""),
                row.get("city", ""),
                row.get("diocese", ""),
                row.get("address", ""),
                row.get("latitude"),
                row.get("longitude"),
                row.get("phone", ""),
                row.get("email", ""),
                row.get("website", ""),
                row.get("mass_times", ""),
                row.get("languages", ""),
                "seed",
                0,
            )
            for row in reader
        ]
    cur.executemany(
        """INSERT INTO parishes
           (name, country, region, city, diocese, address,
            latitude, longitude, phone, email, website,
            mass_times, languages, source, verified)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )
    conn.commit()


# ─────────────────────────────────────────────
# SEARCH
# ─────────────────────────────────────────────

def search_parishes(
    query: str = "",
    country: str = "",
    diocese: str = "",
    city: str = "",
    limit: int = 20,
) -> list[dict]:
    """
    Full-text parish search across name, city, diocese, address.
    Returns list of parish dicts.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    conditions = []
    params = []

    if query:
        conditions.append(
            "(name LIKE ? OR city LIKE ? OR diocese LIKE ? OR address LIKE ?)"
        )
        q = f"%{query}%"
        params.extend([q, q, q, q])

    if country:
        conditions.append("country = ?")
        params.append(country)

    if diocese:
        conditions.append("diocese LIKE ?")
        params.append(f"%{diocese}%")

    if city:
        conditions.append("city LIKE ?")
        params.append(f"%{city}%")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
        SELECT * FROM parishes
        {where}
        ORDER BY verified DESC, name ASC
        LIMIT ?
    """
    params.append(limit)
    rows = cur.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_parish_by_id(parish_id: int) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM parishes WHERE id = ?", (parish_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM parishes").fetchone()[0]
    by_country = cur.execute(
        "SELECT country, COUNT(*) as cnt FROM parishes GROUP BY country ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    verified = cur.execute("SELECT COUNT(*) FROM parishes WHERE verified = 1").fetchone()[0]
    conn.close()
    return {
        "total": total,
        "verified": verified,
        "top_countries": [{"country": r[0], "count": r[1]} for r in by_country],
    }


# ─────────────────────────────────────────────
# GCATHOLIC RAILS — NOT ACTIVE
# ─────────────────────────────────────────────
# Status: FRAMEWORK ONLY — NOT OPERATIONAL
#
# GCatholic (gcatholic.org) does not expose a public API.
# Reaching 100K+ parishes requires either:
#   A) A formal data partnership with GCatholic
#   B) Responsible HTML scraping (ToS review required)
#   C) OpenStreetMap catholic places + Wikipedia categories (open data)
#   D) The Catholic Directory (thecatholicdirectory.com) — partial US coverage
#
# The functions below are the INTEGRATION INTERFACE.
# Activate by setting GCATHOLIC_ENABLED=true and implementing _fetch_gcatholic_page().
# Full guide: docs/GCATHOLIC_INTEGRATION_GUIDE.md
# ─────────────────────────────────────────────

GCATHOLIC_ENABLED = os.getenv("GCATHOLIC_ENABLED", "false").lower() == "true"


def sync_gcatholic(dry_run: bool = True) -> dict:
    """
    Rails entry point for GCatholic sync.
    Currently returns a status report explaining the path to activation.
    """
    if not GCATHOLIC_ENABLED:
        return {
            "status": "RAILS_ONLY",
            "message": (
                "GCatholic integration is not yet active. "
                "Set GCATHOLIC_ENABLED=true after completing the steps in "
                "docs/GCATHOLIC_INTEGRATION_GUIDE.md"
            ),
            "records_added": 0,
            "next_steps": [
                "1. Review GCatholic ToS at gcatholic.org",
                "2. Evaluate OpenStreetMap as open-data alternative",
                "3. Implement _fetch_gcatholic_page() below",
                "4. Set GCATHOLIC_ENABLED=true in .env",
                "5. Run sync_gcatholic(dry_run=True) to validate",
            ],
        }

    # IMPLEMENTATION STUB — activate after completing ToS review
    # from services._gcatholic_scraper import fetch_page, parse_parishes
    # parishes = fetch_page(...)
    # ...
    return {"status": "NOT_IMPLEMENTED", "message": "Implement scraper first."}
