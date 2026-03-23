"""Expanded international RSS feeds with country/region metadata for sentiment analysis."""

import re
import feedparser
from datetime import datetime

SENTIMENT_FEEDS = {
    # --- US ---
    "CNN": {"url": "http://rss.cnn.com/rss/edition_world.rss", "country": "US"},
    "Fox News": {"url": "https://moxie.foxnews.com/google-publisher/world.xml", "country": "US"},
    "NPR": {"url": "https://feeds.npr.org/1004/rss.xml", "country": "US"},
    "AP": {"url": "https://rsshub.app/apnews/topics/world-news", "country": "US"},
    "CBS News": {"url": "https://www.cbsnews.com/latest/rss/world", "country": "US"},
    "ABC News": {"url": "https://abcnews.go.com/abcnews/internationalheadlines", "country": "US"},
    "PBS NewsHour": {"url": "https://www.pbs.org/newshour/feeds/rss/world", "country": "US"},
    "NY Times": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "country": "US"},
    "Washington Post": {"url": "https://feeds.washingtonpost.com/rss/world", "country": "US"},

    # --- UK ---
    "BBC": {"url": "http://feeds.bbci.co.uk/news/world/rss.xml", "country": "UK"},
    "The Guardian": {"url": "https://www.theguardian.com/world/rss", "country": "UK"},
    "Sky News": {"url": "https://feeds.skynews.com/feeds/rss/world.xml", "country": "UK"},
    "Reuters": {"url": "https://feeds.reuters.com/reuters/worldNews", "country": "UK"},
    "The Telegraph": {"url": "https://www.telegraph.co.uk/news/world/rss.xml", "country": "UK"},
    "The Independent": {"url": "https://www.independent.co.uk/news/world/rss", "country": "UK"},

    # --- Middle East ---
    "Al Jazeera": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "country": "Qatar"},
    "Times of Israel": {"url": "https://www.timesofisrael.com/feed/", "country": "Israel"},
    "Haaretz": {"url": "https://www.haaretz.com/srv/haaretz-latest-rss", "country": "Israel"},
    "Jerusalem Post": {"url": "https://www.jpost.com/rss/rssfeedsfrontpage.aspx", "country": "Israel"},
    "Al Arabiya": {"url": "https://english.alarabiya.net/tools/rss", "country": "Saudi Arabia"},
    "Middle East Eye": {"url": "https://www.middleeasteye.net/rss", "country": "UK (ME focus)"},
    "Iran Intl": {"url": "https://www.iranintl.com/en/feed", "country": "Iran"},
    "Press TV": {"url": "https://www.presstv.ir/RSS", "country": "Iran"},

    # --- Europe ---
    "DW": {"url": "https://rss.dw.com/rss/en/all/rss-en-all", "country": "Germany"},
    "France 24": {"url": "https://www.france24.com/en/rss", "country": "France"},
    "Euronews": {"url": "https://www.euronews.com/rss", "country": "France"},
    "Der Standard": {"url": "https://www.derstandard.at/rss", "country": "Austria"},
    "ORF": {"url": "https://rss.orf.at/news.xml", "country": "Austria"},
    "RT": {"url": "https://www.rt.com/rss/news/", "country": "Russia"},
    "TASS": {"url": "https://tass.com/rss/v2.xml", "country": "Russia"},
    "Irish Times": {"url": "https://www.irishtimes.com/cmlink/news-1.1319192", "country": "Ireland"},
    "El Pais": {"url": "https://feeds.elpais.com/mrss-s/pages/ep/site/english.elpais.com/portada", "country": "Spain"},
    # Czech Republic — historically one of most pro-Israel EU states
    "Prague Morning": {"url": "https://www.praguemorning.cz/feed/", "country": "Czech Republic"},
    "Czech Radio": {"url": "https://english.radio.cz/rss", "country": "Czech Republic"},
    # Hungary — Orbán government explicitly pro-Israel
    "Hungary Today": {"url": "https://hungarytoday.hu/feed/", "country": "Hungary"},
    "Daily News Hungary": {"url": "https://dailynewshungary.com/feed/", "country": "Hungary"},
    # Italy — Meloni government supportive of Israel
    "ANSA English": {"url": "https://www.ansa.it/english/news/rss.xml", "country": "Italy"},
    # Philippines — generally positive toward Israel
    "Manila Bulletin": {"url": "https://mb.com.ph/feed", "country": "Philippines"},
    "Inquirer": {"url": "https://newsinfo.inquirer.net/feed", "country": "Philippines"},
    # South Korea
    "Korea Herald": {"url": "https://www.koreaherald.com/rss/020200000000.xml", "country": "South Korea"},

    # --- Asia ---
    "Times of India": {"url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "country": "India"},
    "NDTV": {"url": "https://feeds.feedburner.com/ndtvnews-world-news", "country": "India"},
    "Hindustan Times": {"url": "https://www.hindustantimes.com/feeds/rss/world-news/rssfeed.xml", "country": "India"},
    "NHK World": {"url": "https://www3.nhk.or.jp/rss/news/cat0.xml", "country": "Japan"},
    "SCMP": {"url": "https://www.scmp.com/rss/91/feed", "country": "China (HK)"},
    "Global Times": {"url": "https://www.globaltimes.cn/rss/outbrain.xml", "country": "China"},
    "Straits Times": {"url": "https://www.straitstimes.com/news/world/rss.xml", "country": "Singapore"},
    "ABC Australia": {"url": "https://www.abc.net.au/news/feed/2942460/rss.xml", "country": "Australia"},

    # --- Africa ---
    "News24 (SA)": {"url": "https://feeds.news24.com/articles/news24/World/rss", "country": "South Africa"},

    # --- Latin America ---
    "Buenos Aires Herald": {"url": "https://buenosairesherald.com/feed/", "country": "Argentina"},
}

# Google News fallbacks for outlets whose feeds often fail
FALLBACK_FEEDS = {
    "CNN": "https://news.google.com/rss/search?q=site:cnn.com+world&hl=en",
    "Fox News": "https://news.google.com/rss/search?q=site:foxnews.com+world&hl=en",
    "NPR": "https://news.google.com/rss/search?q=site:npr.org+world&hl=en",
    "BBC": "https://news.google.com/rss/search?q=site:bbc.com+world&hl=en",
    "The Guardian": "https://news.google.com/rss/search?q=site:theguardian.com+world&hl=en",
    "Sky News": "https://news.google.com/rss/search?q=site:news.sky.com+world&hl=en",
    "DW": "https://news.google.com/rss/search?q=site:dw.com+world&hl=en",
    "France 24": "https://news.google.com/rss/search?q=site:france24.com+world&hl=en",
    "Times of India": "https://news.google.com/rss/search?q=site:timesofindia.indiatimes.com+world&hl=en",
    "NHK World": "https://news.google.com/rss/search?q=site:nhk.or.jp+world&hl=en",
    "CBS News": "https://news.google.com/rss/search?q=site:cbsnews.com+world&hl=en",
    "ABC News": "https://news.google.com/rss/search?q=site:abcnews.go.com+world&hl=en",
    "NY Times": "https://news.google.com/rss/search?q=site:nytimes.com+world&hl=en",
    "Washington Post": "https://news.google.com/rss/search?q=site:washingtonpost.com+world&hl=en",
    "Haaretz": "https://news.google.com/rss/search?q=site:haaretz.com&hl=en",
    "Jerusalem Post": "https://news.google.com/rss/search?q=site:jpost.com&hl=en",
    "Al Arabiya": "https://news.google.com/rss/search?q=site:alarabiya.net&hl=en",
    "Middle East Eye": "https://news.google.com/rss/search?q=site:middleeasteye.net&hl=en",
    "Der Standard": "https://news.google.com/rss/search?q=österreich+OR+austria+israel+OR+iran+OR+nahost&hl=de",
    "ORF": "https://news.google.com/rss/search?q=site:orf.at+israel+OR+iran+OR+nahost+OR+gaza&hl=de",
    "RT": "https://news.google.com/rss/search?q=site:rt.com+world&hl=en",
    "SCMP": "https://news.google.com/rss/search?q=site:scmp.com+world&hl=en",
    "Global Times": "https://news.google.com/rss/search?q=site:globaltimes.cn&hl=en",
    "ABC Australia": "https://news.google.com/rss/search?q=site:abc.net.au+world&hl=en",
    "Euronews": "https://news.google.com/rss/search?q=site:euronews.com+world&hl=en",
    "NDTV": "https://news.google.com/rss/search?q=site:ndtv.com+world&hl=en",
    "Iran Intl": "https://news.google.com/rss/search?q=site:iranintl.com&hl=en",
    "Press TV": "https://news.google.com/rss/search?q=site:presstv.ir&hl=en",
    "Prague Morning": "https://news.google.com/rss/search?q=czech+OR+czechia+israel+OR+iran+OR+gaza&hl=en",
    "Czech Radio": "https://news.google.com/rss/search?q=czech+OR+prague+israel+OR+iran+OR+hamas&hl=en",
    "Hungary Today": "https://news.google.com/rss/search?q=hungary+OR+orban+israel+OR+iran+OR+gaza&hl=en",
    "Daily News Hungary": "https://news.google.com/rss/search?q=hungary+OR+budapest+israel+OR+iran+OR+netanyahu&hl=en",
    "ANSA English": "https://news.google.com/rss/search?q=italy+OR+meloni+israel+OR+iran+OR+gaza&hl=en",
    "Manila Bulletin": "https://news.google.com/rss/search?q=philippines+israel+OR+iran&hl=en",
    "Inquirer": "https://news.google.com/rss/search?q=site:inquirer.net+israel+OR+iran&hl=en",
    "Korea Herald": "https://news.google.com/rss/search?q=south+korea+israel+OR+iran&hl=en",
}

COUNTRY_TO_REGION = {
    "US": "North America",
    "UK": "Europe",
    "UK (ME focus)": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "Ireland": "Europe",
    "Spain": "Europe",
    "Austria": "Europe",
    "Czech Republic": "Europe",
    "Hungary": "Europe",
    "Italy": "Europe",
    "Philippines": "Southeast Asia",
    "South Korea": "East Asia",
    "Russia": "Europe",
    "Qatar": "Middle East",
    "Israel": "Middle East",
    "Saudi Arabia": "Middle East",
    "Iran": "Middle East",
    "India": "South Asia",
    "Japan": "East Asia",
    "China (HK)": "East Asia",
    "China": "East Asia",
    "Singapore": "East Asia",
    "Australia": "Oceania",
    "South Africa": "Africa",
    "Argentina": "Latin America",
}

# Topic keyword sets — a headline matches if ANY keyword is found
# Includes German keywords for Austrian/German-language outlets
SENTIMENT_TOPICS = {
    "Israel": [
        "israel", "israeli", "gaza", "hamas", "netanyahu", "west bank",
        "tel aviv", "hezbollah", "idf", "jerusalem", "kibbutz", "golan",
        # German / Czech / Hungarian
        "israelisch", "nahost", "gazastreifen", "westjordanland",
        "nahostkonflikt", "libanon", "hisbollah",
        "izrael", "gáza", "hamász", "pásmo gazy",
    ],
    "US attack on Iran": [
        "us iran", "us strike", "us attack", "american strike",
        "pentagon iran", "centcom", "us bomb", "trump iran",
        "us retali", "us military iran", "us war iran", "us-israel",
        "us-iranian", "us strikes iran", "american attack iran",
        # German
        "iran-krieg", "iran angriff", "usa iran", "iranisch",
        "iran-konflikt", "teheran", "persischer golf",
    ],
}


# Outlets where the primary feed is mostly local news — always also fetch
# the Google News fallback (which searches specifically for geopolitical topics)
ALWAYS_SUPPLEMENT = {
    "ORF", "Der Standard", "Hungary Today", "Daily News Hungary",
    "Czech Radio", "Czech News Agency", "ANSA English", "Korea Herald",
    "Manila Bulletin", "Inquirer",
}


def fetch_sentiment_feeds():
    """Fetch all international RSS feeds. Returns list of entries with source/country/region."""
    all_entries = []
    for source, info in SENTIMENT_FEEDS.items():
        feed = feedparser.parse(info["url"])
        entries = list(feed.entries)
        fallback = FALLBACK_FEEDS.get(source)

        # If primary returned nothing, use fallback exclusively
        if not entries and fallback:
            feed = feedparser.parse(fallback)
            entries = list(feed.entries)
        # If primary is mostly local, ALSO fetch fallback to supplement
        elif source in ALWAYS_SUPPLEMENT and fallback:
            fb_feed = feedparser.parse(fallback)
            entries.extend(fb_feed.entries)

        country = info["country"]
        region = COUNTRY_TO_REGION.get(country, "Other")
        for entry in entries:
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            summary = entry.get("summary", entry.get("description", ""))
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            all_entries.append({
                "title": entry.get("title", ""),
                "summary": summary[:500],
                "link": entry.get("link", ""),
                "source": source,
                "country": country,
                "region": region,
                "published": published,
            })
        if entries:
            print(f"    {source}: {len(entries)} entries")
    return all_entries


def filter_by_topic(entries, topic_name):
    """Filter entries matching a topic's keywords."""
    keywords = SENTIMENT_TOPICS.get(topic_name, [])
    matched = []
    for entry in entries:
        text = (entry["title"] + " " + entry.get("summary", "")).lower()
        if topic_name == "US attack on Iran":
            has_us = any(w in text for w in ["us ", "u.s.", "american", "pentagon", "centcom", "trump", "us-"])
            has_iran = "iran" in text
            has_military = any(w in text for w in [
                "strike", "attack", "bomb", "military", "war", "retali",
                "offensive", "troops", "missile",
            ])
            if (has_us and has_iran and has_military) or any(kw in text for kw in keywords):
                matched.append(entry)
        else:
            if any(kw in text for kw in keywords):
                matched.append(entry)
    return matched
