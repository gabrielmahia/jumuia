"""
OpenStreetMap Parish Importer — Catholic Network Tools
=======================================================
Fetches Catholic places of worship from OpenStreetMap via Overpass API.
FREE, no API key, no auth, open data (ODbL license).

This is the fastest path to 100K+ parishes without GCatholic scraping.

DATA QUALITY vs GCatholic:
  OSM:       ~40-60K Catholic places globally, community-maintained
             Coverage excellent in Europe, Kenya, Philippines, Brazil
             Fields: name, address, lat/lon, website, phone (where contributed)
  GCatholic: ~100K+ with richer liturgical data (Mass times, diocese hierarchy)
             No public API — requires data partnership or scraping (ToS review)

RECOMMENDED STRATEGY:
  Phase 1 (now):   Import OSM → 40K parishes, zero cost, open data ✅
  Phase 2 (later): Merge GCatholic via partnership or manual enrichment
  Phase 3 (later): Community-verified submissions fill the gaps

RUN:
  python scripts/import_osm_parishes.py --country KE     # Kenya only
  python scripts/import_osm_parishes.py --country all    # Global (slow, ~20 min)
  python scripts/import_osm_parishes.py --bbox "-1.5,36.6,-1.1,37.1"  # Bounding box
"""

import os
import sys
import time
import sqlite3
import logging
import argparse
from pathlib import Path
from typing import Optional

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
DB_PATH = Path(os.getenv("CNT_DB_PATH", "data/parishes.db"))

# ISO 3166-1 alpha-2 → Overpass area name mapping for common countries
COUNTRY_AREAS = {
    "KE": "Kenya",
    "UG": "Uganda",
    "TZ": "Tanzania",
    "RW": "Rwanda",
    "ET": "Ethiopia",
    "NG": "Nigeria",
    "GH": "Ghana",
    "PH": "Philippines",
    "BR": "Brazil",
    "MX": "Mexico",
    "IT": "Italy",
    "FR": "France",
    "ES": "Spain",
    "PT": "Portugal",
    "US": "United States",
    "GB": "United Kingdom",
    "AU": "Australia",
    "IN": "India",
    "VN": "Vietnam",
    "PL": "Poland",
}


# ─────────────────────────────────────────────
# OVERPASS QUERY BUILDER
# ─────────────────────────────────────────────

def _build_query_country(country_name: str) -> str:
    """
    Overpass QL query — Catholic places of worship in a country.
    Matches: amenity=place_of_worship + denomination=catholic OR religion=christian+denomination=catholic
    """
    return f"""
[out:json][timeout:120];
area["name"="{country_name}"]["boundary"="administrative"]["admin_level"="2"]->.searchArea;
(
  node["amenity"="place_of_worship"]["denomination"="catholic"](area.searchArea);
  way["amenity"="place_of_worship"]["denomination"="catholic"](area.searchArea);
  node["amenity"="place_of_worship"]["denomination"="Roman Catholic"](area.searchArea);
  way["amenity"="place_of_worship"]["denomination"="Roman Catholic"](area.searchArea);
);
out body center;
"""


def _build_query_bbox(bbox: str) -> str:
    """
    bbox: "south,west,north,east" e.g. "-1.5,36.6,-1.1,37.1" for Nairobi
    """
    return f"""
[out:json][timeout:60];
(
  node["amenity"="place_of_worship"]["denomination"="catholic"]({bbox});
  way["amenity"="place_of_worship"]["denomination"="catholic"]({bbox});
);
out body center;
"""


# ─────────────────────────────────────────────
# FETCH FROM OVERPASS
# ─────────────────────────────────────────────

def fetch_osm_parishes(
    country_code: Optional[str] = None,
    bbox: Optional[str] = None,
    retry: int = 3,
) -> list[dict]:
    """
    Query Overpass API and return raw OSM element list.
    Rate limit: Overpass asks for polite use — add delay between large queries.
    """
    if country_code:
        country_name = COUNTRY_AREAS.get(country_code.upper())
        if not country_name:
            raise ValueError(
                f"Country code {country_code} not in supported list. "
                f"Add it to COUNTRY_AREAS or use --bbox instead."
            )
        query = _build_query_country(country_name)
    elif bbox:
        query = _build_query_bbox(bbox)
    else:
        raise ValueError("Provide either country_code or bbox")

    for attempt in range(retry):
        try:
            logger.info("Querying Overpass API (attempt %d/%d)...", attempt + 1, retry)
            resp = requests.post(
                OVERPASS_URL,
                data={"data": query},
                timeout=150,
                headers={"User-Agent": "CatholicNetworkTools/1.0 contact@aikungfu.dev"},
            )
            resp.raise_for_status()
            data = resp.json()
            elements = data.get("elements", [])
            logger.info("OSM returned %d elements", len(elements))
            return elements
        except requests.exceptions.Timeout:
            logger.warning("Overpass timeout on attempt %d", attempt + 1)
            time.sleep(10 * (attempt + 1))
        except Exception as e:
            logger.error("Overpass error: %s", e)
            if attempt == retry - 1:
                raise
            time.sleep(5)

    return []


# ─────────────────────────────────────────────
# PARSE OSM → PARISH DICT
# ─────────────────────────────────────────────

def _parse_element(el: dict) -> Optional[dict]:
    """Convert OSM element to parish dict matching our SQLite schema."""
    tags = el.get("tags", {})

    # Get coordinates — nodes have lat/lon directly, ways have center
    if el["type"] == "node":
        lat = el.get("lat")
        lon = el.get("lon")
    else:
        center = el.get("center", {})
        lat = center.get("lat")
        lon = center.get("lon")

    name = tags.get("name") or tags.get("name:en") or tags.get("alt_name")
    if not name:
        return None  # Skip unnamed entries

    # Build address from OSM address tags
    addr_parts = []
    for key in ["addr:housenumber", "addr:street", "addr:suburb", "addr:city"]:
        val = tags.get(key)
        if val:
            addr_parts.append(val)
    address = ", ".join(addr_parts) if addr_parts else ""

    return {
        "name": name[:255],
        "country": tags.get("addr:country", ""),
        "region": tags.get("addr:state") or tags.get("addr:region") or "",
        "city": tags.get("addr:city") or tags.get("addr:town") or tags.get("addr:village") or "",
        "diocese": "",  # OSM rarely has diocese data — enrich from GCatholic later
        "address": address,
        "latitude": lat,
        "longitude": lon,
        "phone": tags.get("phone") or tags.get("contact:phone") or "",
        "email": tags.get("email") or tags.get("contact:email") or "",
        "website": tags.get("website") or tags.get("contact:website") or "",
        "mass_times": tags.get("opening_hours") or "",  # OSM uses opening_hours for service times
        "languages": "",
        "source": "openstreetmap",
        "verified": 0,
    }


# ─────────────────────────────────────────────
# IMPORT INTO SQLITE
# ─────────────────────────────────────────────

def import_to_db(
    parishes: list[dict],
    dry_run: bool = False,
) -> dict:
    """
    Insert parsed parishes into the SQLite database.
    Skips duplicates based on name + approximate coordinates (0.001° ~ 100m).

    Returns: {"added": int, "skipped": int, "errors": int}
    """
    if not parishes:
        return {"added": 0, "skipped": 0, "errors": 0}

    if dry_run:
        logger.info("DRY RUN — %d parishes would be imported", len(parishes))
        for p in parishes[:5]:
            logger.info("  Sample: %s, %s", p["name"], p["city"])
        return {"added": 0, "skipped": len(parishes), "errors": 0, "dry_run": True}

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # Ensure table exists (init_db may not have run)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS parishes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            country     TEXT, region TEXT, city TEXT, diocese TEXT,
            address     TEXT, latitude REAL, longitude REAL,
            phone TEXT, email TEXT, website TEXT, mass_times TEXT,
            languages TEXT, source TEXT DEFAULT 'openstreetmap',
            verified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    added = skipped = errors = 0

    for p in parishes:
        try:
            # Deduplicate: skip if name + coordinates already exist (within ~100m)
            lat, lon = p.get("latitude"), p.get("longitude")
            if lat and lon:
                existing = conn.execute("""
                    SELECT id FROM parishes
                    WHERE name = ?
                    AND ABS(COALESCE(latitude,999) - ?) < 0.001
                    AND ABS(COALESCE(longitude,999) - ?) < 0.001
                """, (p["name"], lat, lon)).fetchone()
            else:
                existing = conn.execute(
                    "SELECT id FROM parishes WHERE name = ? AND city = ?",
                    (p["name"], p.get("city", ""))
                ).fetchone()

            if existing:
                skipped += 1
                continue

            conn.execute("""
                INSERT INTO parishes
                (name, country, region, city, diocese, address,
                 latitude, longitude, phone, email, website,
                 mass_times, languages, source, verified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                p["name"], p["country"], p["region"], p["city"],
                p["diocese"], p["address"], p["latitude"], p["longitude"],
                p["phone"], p["email"], p["website"],
                p["mass_times"], p["languages"], p["source"], p["verified"],
            ))
            added += 1

        except Exception as e:
            logger.warning("Insert error for '%s': %s", p.get("name", "?"), e)
            errors += 1

    conn.commit()

    # Log the sync
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gcatholic_sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            synced_at TEXT DEFAULT (datetime('now')),
            records_added INTEGER DEFAULT 0,
            records_updated INTEGER DEFAULT 0,
            status TEXT, notes TEXT
        )
    """)
    conn.execute(
        "INSERT INTO gcatholic_sync_log (records_added, status, notes) VALUES (?,?,?)",
        (added, "COMPLETE", f"OSM import: +{added} added, {skipped} skipped, {errors} errors")
    )
    conn.commit()
    conn.close()

    logger.info("Import complete: +%d added, %d skipped, %d errors", added, skipped, errors)
    return {"added": added, "skipped": skipped, "errors": errors}


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Import Catholic parishes from OpenStreetMap into CNT database"
    )
    parser.add_argument(
        "--country", "-c",
        help="ISO country code (e.g. KE, UG, TZ, PH). Use 'all' for all supported countries.",
        default=None,
    )
    parser.add_argument(
        "--bbox",
        help='Bounding box "south,west,north,east" e.g. "-1.5,36.6,-1.1,37.1"',
        default=None,
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Parse and count without writing to database",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Override database path",
    )
    args = parser.parse_args()

    if args.db:
        global DB_PATH
        DB_PATH = Path(args.db)

    if not args.country and not args.bbox:
        parser.print_help()
        print("\nExamples:")
        print("  python scripts/import_osm_parishes.py --country KE")
        print("  python scripts/import_osm_parishes.py --country KE --dry-run")
        print("  python scripts/import_osm_parishes.py --bbox '-1.5,36.6,-1.1,37.1'")
        sys.exit(1)

    if args.country and args.country.lower() == "all":
        total = {"added": 0, "skipped": 0, "errors": 0}
        for code in COUNTRY_AREAS:
            logger.info("=== Processing %s ===", code)
            try:
                elements = fetch_osm_parishes(country_code=code)
                parishes = [p for el in elements if (p := _parse_element(el))]
                result = import_to_db(parishes, dry_run=args.dry_run)
                for k in total:
                    total[k] += result.get(k, 0)
                time.sleep(2)  # Be polite to Overpass
            except Exception as e:
                logger.error("Failed for %s: %s", code, e)
        logger.info("TOTAL: %s", total)
    elif args.country:
        elements = fetch_osm_parishes(country_code=args.country.upper())
        parishes = [p for el in elements if (p := _parse_element(el))]
        logger.info("Parsed %d parishes from %d OSM elements", len(parishes), len(elements))
        result = import_to_db(parishes, dry_run=args.dry_run)
        print(f"\nResult: {result}")
    elif args.bbox:
        elements = fetch_osm_parishes(bbox=args.bbox)
        parishes = [p for el in elements if (p := _parse_element(el))]
        logger.info("Parsed %d parishes from %d OSM elements", len(parishes), len(elements))
        result = import_to_db(parishes, dry_run=args.dry_run)
        print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
