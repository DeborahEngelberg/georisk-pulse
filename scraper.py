import feedparser
from datetime import datetime

RSS_FEEDS = {
    "Reuters": "https://feeds.reuters.com/reuters/worldNews",
    "AP": "https://rsshub.app/apnews/topics/world-news",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}

# Fallback feeds if primary ones fail
FALLBACK_FEEDS = {
    "Reuters": "https://news.google.com/rss/search?q=site:reuters.com+world&hl=en",
    "AP": "https://news.google.com/rss/search?q=site:apnews.com+world&hl=en",
    "Al Jazeera": "https://news.google.com/rss/search?q=site:aljazeera.com&hl=en",
}

DEFAULT_REGIONS = ["Iran", "Russia", "Israel", "Taiwan"]

# Keywords and aliases to match headlines to regions
REGION_KEYWORDS = {
    "Iran": ["iran", "iranian", "tehran", "persian gulf", "khamenei", "irgc",
             "natanz", "isfahan", "strait of hormuz", "quds force", "basij"],
    "Russia": ["russia", "russian", "moscow", "kremlin", "putin", "ukraine",
               "donbas", "crimea", "zelensky", "kyiv", "kherson", "wagner"],
    "Israel": ["israel", "israeli", "gaza", "hamas", "netanyahu", "west bank",
               "tel aviv", "hezbollah", "idf", "iron dome", "beirut",
               "golan", "kibbutz", "shin bet", "mossad"],
    "Taiwan": ["taiwan", "taiwanese", "taipei", "china strait", "tsmc",
               "people's liberation army", "pla navy"],
}

# Headlines mentioning these terms alongside a region get counted for that region too.
# Captures US military involvement in regional conflicts.
CROSS_REGION_KEYWORDS = {
    "Iran": ["us-israel", "us-iranian", "american strike", "pentagon iran",
             "trump iran", "centcom"],
    "Israel": ["us-israel", "american strike", "pentagon israel",
               "trump israel", "centcom"],
}


def fetch_all_feeds():
    """Fetch and parse all RSS feeds. Returns list of raw entries."""
    all_entries = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        entries = feed.entries
        if not entries:
            fallback = FALLBACK_FEEDS.get(source)
            if fallback:
                feed = feedparser.parse(fallback)
                entries = feed.entries
        for entry in entries:
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            all_entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "source": source,
                "published": published,
            })
    return all_entries


def match_headlines_to_regions(entries, regions=None):
    """Filter entries by region relevance. Returns dict: {region: [entries]}."""
    if regions is None:
        regions = DEFAULT_REGIONS
    matched = {r: [] for r in regions}
    for entry in entries:
        title_lower = entry["title"].lower()
        for region in regions:
            keywords = REGION_KEYWORDS.get(region, [region.lower()])
            cross_keywords = CROSS_REGION_KEYWORDS.get(region, [])
            if any(kw in title_lower for kw in keywords):
                matched[region].append(entry)
            elif any(kw in title_lower for kw in cross_keywords):
                matched[region].append(entry)
    return matched
