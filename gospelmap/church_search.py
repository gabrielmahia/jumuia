"""
GospelMap Church Search
Standalone OSM-based search (no external deps).
Multi-strategy: area-based → radius → name-based fallback.
"""

import requests
from dataclasses import dataclass
from typing import List, Optional, Tuple
import math

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


@dataclass
class Church:
    name: str
    latitude: float
    longitude: float
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    distance_km: Optional[float] = None
    osm_id: Optional[str] = None


def _overpass(query: str, timeout: int = 35) -> dict:
    for url in OVERPASS_ENDPOINTS:
        try:
            r = requests.post(url, data={"data": query}, timeout=timeout,
                              headers={"User-Agent": "GospelMap/1.0 (contact@aikungfu.dev)"})
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Overpass {url}: {e}")
    return {"elements": []}


def _geocode(location: str) -> Optional[Tuple[float, float]]:
    try:
        r = requests.get(NOMINATIM_URL, params={"q": location, "format": "json", "limit": 1},
                         headers={"User-Agent": "GospelMap/1.0 (contact@aikungfu.dev)"}, timeout=10)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None


def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def _parse_element(elem, ref_lat=None, ref_lon=None) -> Optional[Church]:
    tags = elem.get("tags", {})
    name = tags.get("name", "")
    if not name:
        return None

    # Skip if clearly not Catholic (but allow unnamed/ambiguous)
    denom = tags.get("denomination", "").lower()
    if denom and denom not in ("catholic", "roman_catholic", ""):
        religion = tags.get("religion", "").lower()
        if religion == "christian" and not any(k in name.lower() for k in
                                               ("catholic","st.","saint","holy","immaculate","assumption","parish","basilica")):
            return None

    if elem["type"] == "node":
        lat, lon = elem.get("lat", 0), elem.get("lon", 0)
    else:
        c = elem.get("center", {})
        lat, lon = c.get("lat", 0), c.get("lon", 0)

    if not lat or not lon:
        return None

    dist = None
    if ref_lat is not None:
        dist = _haversine(ref_lat, ref_lon, lat, lon)

    addr_parts = [
        tags.get("addr:housenumber",""),
        tags.get("addr:street",""),
        tags.get("addr:city",""),
    ]
    address = " ".join(p for p in addr_parts if p) or None

    return Church(
        name=name,
        latitude=lat,
        longitude=lon,
        city=tags.get("addr:city") or tags.get("addr:suburb"),
        country=tags.get("addr:country"),
        address=address,
        phone=tags.get("phone") or tags.get("contact:phone"),
        website=tags.get("website") or tags.get("contact:website"),
        distance_km=round(dist, 2) if dist else None,
        osm_id=str(elem.get("id")),
    )


def search_by_city(city: str, country: Optional[str] = None, limit: int = 15) -> List[Church]:
    """Search for Catholic churches in a city. Multi-strategy with failover."""
    # Strategy 1: OSM area-based (best for African/Asian cities)
    area_results = _area_search(city, country, limit)
    if len(area_results) >= 3:
        return sorted(area_results, key=lambda c: c.distance_km or 999)[:limit]

    # Strategy 2: Geocode + radius fallback
    location = f"{city}, {country}" if country else city
    coords = _geocode(location)
    if coords:
        radius_results = _radius_search(coords[0], coords[1], radius_km=40, limit=limit, ref_lat=coords[0], ref_lon=coords[1])
        seen = {c.name.lower() for c in area_results}
        for c in radius_results:
            if c.name.lower() not in seen:
                area_results.append(c)
                seen.add(c.name.lower())
        if c.city is None and city:
            c.city = city.title()

    return sorted(area_results, key=lambda c: c.distance_km or 999)[:limit]


def _area_search(city: str, country: Optional[str], limit: int) -> List[Church]:
    query = f"""
    [out:json][timeout:35];
    area["name"~"{city}",i]["admin_level"~"4|5|6|7|8"]->.searchArea;
    (
      node["amenity"="place_of_worship"]["denomination"="catholic"](area.searchArea);
      way["amenity"="place_of_worship"]["denomination"="catholic"](area.searchArea);
      node["amenity"="place_of_worship"]["denomination"="roman_catholic"](area.searchArea);
      way["amenity"="place_of_worship"]["denomination"="roman_catholic"](area.searchArea);
      node["amenity"="place_of_worship"]["religion"="christian"]["name"~"catholic|st\\.|saint|holy|immaculate|assumption|parish|basilica",i](area.searchArea);
      way["amenity"="place_of_worship"]["religion"="christian"]["name"~"catholic|st\\.|saint|holy|immaculate|assumption|parish|basilica",i](area.searchArea);
    );
    out center {limit};
    """
    data = _overpass(query, timeout=40)
    churches = []
    for elem in data.get("elements", []):
        c = _parse_element(elem)
        if c:
            c.city = c.city or city.title()
            if country:
                c.country = c.country or country.title()
            churches.append(c)
    return churches


def _radius_search(lat, lon, radius_km=40, limit=15, ref_lat=None, ref_lon=None) -> List[Church]:
    radius_m = int(radius_km * 1000)
    queries = [
        f"""[out:json][timeout:30];
        (
          node["amenity"="place_of_worship"]["denomination"="catholic"](around:{radius_m},{lat},{lon});
          way["amenity"="place_of_worship"]["denomination"="catholic"](around:{radius_m},{lat},{lon});
          node["amenity"="place_of_worship"]["denomination"="roman_catholic"](around:{radius_m},{lat},{lon});
          way["amenity"="place_of_worship"]["denomination"="roman_catholic"](around:{radius_m},{lat},{lon});
        );
        out center {limit};""",
        f"""[out:json][timeout:30];
        (
          node["amenity"="place_of_worship"]["religion"="christian"]["name"~"catholic|st\\.|saint|holy|immaculate|parish|basilica",i](around:{radius_m},{lat},{lon});
          way["amenity"="place_of_worship"]["religion"="christian"]["name"~"catholic|st\\.|saint|holy|immaculate|parish|basilica",i](around:{radius_m},{lat},{lon});
        );
        out center {limit};""",
    ]
    churches = []
    seen = set()
    for q in queries:
        data = _overpass(q, timeout=35)
        for elem in data.get("elements", []):
            c = _parse_element(elem, ref_lat, ref_lon)
            if c and c.name.lower() not in seen:
                churches.append(c)
                seen.add(c.name.lower())
        if len(churches) >= 3:
            break
    return churches

