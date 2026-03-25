"""Google Trends integration — public attention/concern by country.

Completely free, no API key needed. Shows which countries are paying
attention to each topic, measured by search volume.
"""

import time


# Keywords per topic
TRENDS_KEYWORDS = {
    "Israel": ["Israel war", "Gaza", "Hamas"],
    "US attack on Iran": ["Iran war", "Iran attack", "Iran nuclear"],
}

# Countries we track (ISO codes)
TRACKED_COUNTRIES = {
    "US": "United States", "GB": "United Kingdom", "DE": "Germany",
    "AT": "Austria", "FR": "France", "IL": "Israel", "IR": "Iran",
    "IN": "India", "RU": "Russia", "TR": "Turkey", "CA": "Canada",
    "AU": "Australia", "HU": "Hungary", "CZ": "Czechia",
    "IT": "Italy", "PH": "Philippines", "KR": "South Korea",
    "IE": "Ireland", "ZA": "South Africa", "SA": "Saudi Arabia",
    "JP": "Japan", "SG": "Singapore",
}


def fetch_trends_data(topic_name):
    """Fetch Google Trends interest by country for a topic.

    Returns dict: {
        "by_country": [{"country": "Austria", "interest": 85}, ...],
        "over_time": [{"date": "2026-03-01", "interest": 72}, ...],
        "keyword": "Israel war"
    }
    """
    keywords = TRENDS_KEYWORDS.get(topic_name, [])
    if not keywords:
        return None

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=0, timeout=15, retries=3, backoff_factor=0.5)

        keyword = keywords[0]  # Use primary keyword
        print(f"    Google Trends: '{keyword}'...")

        # Interest by country
        pytrends.build_payload([keyword], timeframe="today 1-m", geo="")
        by_region = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True)
        time.sleep(2)

        # Interest over time
        pytrends.build_payload([keyword], timeframe="today 1-m", geo="")
        over_time = pytrends.interest_over_time()
        time.sleep(2)

        # Parse by-country results
        country_data = []
        for iso, name in TRACKED_COUNTRIES.items():
            if name in by_region.index:
                interest = int(by_region.loc[name, keyword])
                if interest > 0:
                    country_data.append({"country": name, "iso": iso, "interest": interest})
        country_data.sort(key=lambda x: -x["interest"])

        # Parse over-time results
        time_data = []
        if not over_time.empty:
            for date, row in over_time.iterrows():
                time_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "interest": int(row[keyword]),
                })

        print(f"    Google Trends: {len(country_data)} countries, {len(time_data)} time points")
        return {
            "by_country": country_data,
            "over_time": time_data,
            "keyword": keyword,
        }

    except Exception as e:
        print(f"    Google Trends error: {e}")
        return None
