"""Google Trends integration — public attention/concern by country.

Uses direct HTTP requests to Google Trends (no pytrends dependency).
Completely free, no API key needed.
"""

import json
import time
import requests

TRENDS_KEYWORDS = {
    "Israel": "Israel war",
    "US attack on Iran": "Iran war",
}

TRACKED_COUNTRIES = {
    "US": "United States", "GB": "United Kingdom", "DE": "Germany",
    "AT": "Austria", "FR": "France", "IL": "Israel", "IR": "Iran",
    "IN": "India", "RU": "Russia", "TR": "Turkey", "CA": "Canada",
    "AU": "Australia", "HU": "Hungary", "CZ": "Czechia",
    "IT": "Italy", "PH": "Philippines", "KR": "South Korea",
    "IE": "Ireland", "ZA": "South Africa", "SA": "Saudi Arabia",
    "JP": "Japan", "SG": "Singapore",
}

# Reverse lookup
COUNTRY_NAME_TO_ISO = {v: k for k, v in TRACKED_COUNTRIES.items()}


def fetch_trends_data(topic_name):
    """Fetch Google Trends interest by country using direct API call."""
    keyword = TRENDS_KEYWORDS.get(topic_name)
    if not keyword:
        return None

    print(f"    Google Trends: '{keyword}'...")

    try:
        # Google Trends has a public JSON endpoint
        # This is what pytrends uses internally
        encoded = requests.utils.quote(keyword)
        url = f"https://trends.google.com/trends/api/widgetdata/comparedgeo"

        # First get the token from the explore page
        explore_url = "https://trends.google.com/trends/api/explore"
        params = {
            "hl": "en-US",
            "tz": "0",
            "req": json.dumps({
                "comparisonItem": [{"keyword": keyword, "geo": "", "time": "today 1-m"}],
                "category": 0,
                "property": "",
            }),
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
        }

        resp = requests.get(explore_url, params=params, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"    Google Trends: explore returned {resp.status_code}")
            return None

        # Response starts with ")]}',\n" which we need to strip
        text = resp.text
        if text.startswith(")]}'"):
            text = text[5:]

        data = json.loads(text)
        widgets = data.get("widgets", [])

        # Find the geo widget
        geo_widget = None
        for w in widgets:
            if w.get("id", "").startswith("GEO_MAP"):
                geo_widget = w
                break

        if not geo_widget:
            print("    Google Trends: no geo widget found")
            return None

        # Now fetch the geo data using the token
        token = geo_widget.get("token", "")
        req_data = geo_widget.get("request", {})

        geo_url = "https://trends.google.com/trends/api/widgetdata/comparedgeo"
        geo_params = {
            "hl": "en-US",
            "tz": "0",
            "req": json.dumps(req_data),
            "token": token,
        }

        time.sleep(1)
        geo_resp = requests.get(geo_url, params=geo_params, headers=headers, timeout=15)
        if geo_resp.status_code != 200:
            print(f"    Google Trends: geo returned {geo_resp.status_code}")
            return None

        geo_text = geo_resp.text
        if geo_text.startswith(")]}'"):
            geo_text = geo_text[5:]

        geo_data = json.loads(geo_text)

        # Parse results
        country_data = []
        for entry in geo_data.get("default", {}).get("geoMapData", []):
            name = entry.get("geoName", "")
            values = entry.get("value", [])
            interest = values[0] if values else 0

            if name in COUNTRY_NAME_TO_ISO and interest > 0:
                country_data.append({
                    "country": name,
                    "iso": COUNTRY_NAME_TO_ISO[name],
                    "interest": interest,
                })

        country_data.sort(key=lambda x: -x["interest"])
        print(f"    Google Trends: {len(country_data)} tracked countries with data")
        return {
            "by_country": country_data,
            "over_time": [],
            "keyword": keyword,
        }

    except Exception as e:
        print(f"    Google Trends error: {e}")
        return None
