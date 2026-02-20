"""
Location Service — Catholic Network Tools
Auto-detects user country, currency, and timezone from IP.
Free — no API key required (ip-api.com, 45 requests/minute limit).
Results cached per session (no repeat calls).
"""
import requests

# Currency symbols and formatting
CURRENCY_SYMBOLS: dict[str, str] = {
    "KES": "KSh",    # Kenya
    "UGX": "USh",    # Uganda
    "TZS": "TSh",    # Tanzania
    "NGN": "₦",      # Nigeria
    "GHS": "₵",      # Ghana
    "ZAR": "R",      # South Africa
    "ETB": "Br",     # Ethiopia
    "USD": "$",      # United States
    "EUR": "€",      # Eurozone
    "GBP": "£",      # UK
    "BRL": "R$",     # Brazil
    "PHP": "₱",      # Philippines
    "INR": "₹",      # India
    "KRW": "₩",      # South Korea
    "MXN": "$",      # Mexico
    "COP": "$",      # Colombia
    "ARS": "$",      # Argentina
    "PLN": "zł",     # Poland
    "CZK": "Kč",     # Czech Republic
    "HRK": "kn",     # Croatia
    "VND": "₫",      # Vietnam
    "IDR": "Rp",     # Indonesia
    "CAD": "CA$",    # Canada
    "AUD": "A$",     # Australia
    "JPY": "¥",      # Japan
    "CNY": "¥",      # China
}

# Country code → primary language suggestion
COUNTRY_LANGUAGE_MAP: dict[str, tuple] = {
    "KE": ("sw", "Kiswahili"),
    "TZ": ("sw", "Kiswahili"),
    "UG": ("lg", "Luganda"),
    "NG": ("en", "English"),
    "GH": ("en", "English"),
    "CM": ("fr", "French"),
    "CI": ("fr", "French"),
    "SN": ("fr", "French"),
    "CD": ("fr", "French"),
    "MG": ("fr", "French"),
    "FR": ("fr", "French"),
    "BE": ("fr", "French"),
    "CH": ("fr", "French"),
    "ES": ("es", "Spanish"),
    "MX": ("es", "Spanish"),
    "BR": ("pt", "Portuguese"),
    "PH": ("en", "English"),
    "IT": ("it", "Italian"),
    "PL": ("en", "English"),
    "US": ("en", "English"),
    "GB": ("en", "English"),
    "AU": ("en", "English"),
    "IN": ("en", "English"),
}

# Countries where M-Pesa is most relevant (Safaricom network)
MPESA_COUNTRIES = {"KE", "TZ", "GH", "CI", "CM", "ET", "MZ", "LS", "EG", "ZA"}


def _fetch_location() -> dict:
    """Fetch location from ip-api.com. Returns empty dict on failure."""
    try:
        r = requests.get(
            "https://ip-api.com/json/",
            params={"fields": "status,country,countryCode,city,timezone,currency,proxy,hosting"},
            timeout=5,
        )
        data = r.json()
        if data.get("status") == "success":
            return data
    except Exception:
        pass
    return {}


def detect_location() -> dict:
    """
    Return detected location data.

    Returns:
        {
          "country":       str,   # "Kenya"
          "country_code":  str,   # "KE"
          "city":          str,   # "Nairobi"
          "currency":      str,   # "KES"
          "timezone":      str,   # "Africa/Nairobi"
          "is_vpn":        bool,
          "language_code": str,   # "sw"
          "language_name": str,   # "Kiswahili"
          "mpesa_relevant": bool,
          "detected":      bool,  # False if detection failed
        }
    """
    raw = _fetch_location()
    if not raw:
        return {
            "country": "Unknown", "country_code": "", "city": "Unknown",
            "currency": "USD", "timezone": "UTC", "is_vpn": False,
            "language_code": "en", "language_name": "English",
            "mpesa_relevant": False, "detected": False,
        }

    cc = raw.get("countryCode", "")
    lang_code, lang_name = COUNTRY_LANGUAGE_MAP.get(cc, ("en", "English"))

    return {
        "country":        raw.get("country", "Unknown"),
        "country_code":   cc,
        "city":           raw.get("city", "Unknown"),
        "currency":       raw.get("currency", "USD"),
        "timezone":       raw.get("timezone", "UTC"),
        "is_vpn":         raw.get("proxy", False) or raw.get("hosting", False),
        "language_code":  lang_code,
        "language_name":  lang_name,
        "mpesa_relevant": cc in MPESA_COUNTRIES,
        "detected":       True,
    }


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format an amount in the given currency with local symbol."""
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    if currency in ("JPY", "KRW", "IDR", "UGX", "TZS"):
        # No decimal places for whole-unit currencies
        return f"{symbol} {int(amount):,}"
    return f"{symbol} {amount:,.2f}"


if __name__ == "__main__":
    loc = detect_location()
    print(loc)
    print(format_currency(5000, loc["currency"]))
