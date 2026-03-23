"""Scrape Reddit posts from country-specific subreddits via RSS feeds.

Reddit RSS feeds are public and don't require API keys or authentication.
Each subreddit's top/hot posts are available at /r/{sub}/.rss and /r/{sub}/top/.rss
"""

import re
import time
import feedparser
from datetime import datetime

# Country-specific subreddits mapped to their country
SUBREDDIT_MAP = {
    # Country subs
    "US": ["politics", "AmericanPolitics", "news"],
    "UK": ["unitedkingdom", "ukpolitics"],
    "Israel": ["Israel", "IsraelPalestine"],
    "Iran": ["iran", "Iranian"],
    "India": ["india", "IndiaSpeaks", "indianews"],
    "Germany": ["germany"],
    "Austria": ["Austria", "wien"],
    "Czech Republic": ["czech", "Prague"],
    "Hungary": ["hungary", "budapest"],
    "France": ["france"],
    "Russia": ["russia"],
    "Turkey": ["Turkey"],
    "Canada": ["canada", "CanadaPolitics"],
    "Australia": ["australia"],
    "Ireland": ["ireland"],
    "South Africa": ["southafrica"],
    "Saudi Arabia": ["saudiarabia"],
    # Global
    "Global": ["worldnews", "geopolitics", "InternationalNews"],
}

SOCIAL_TOPICS = {
    "Israel": {
        "filter_keywords": ["israel", "israeli", "gaza", "hamas", "idf",
                            "netanyahu", "hezbollah", "west bank", "tel aviv",
                            "jerusalem", "kibbutz", "golan", "zionist"],
    },
    "US attack on Iran": {
        "filter_keywords": ["iran", "iranian", "tehran", "strike iran",
                            "attack iran", "bomb iran", "us iran", "war iran",
                            "centcom", "pentagon iran", "trump iran",
                            "natanz", "isfahan"],
    },
}


def fetch_subreddit_rss(subreddit, sort="top", time_filter="week"):
    """Fetch posts from a subreddit via RSS feed."""
    if sort == "top":
        url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t={time_filter}"
    elif sort == "hot":
        url = f"https://www.reddit.com/r/{subreddit}/hot/.rss"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/.rss"

    feed = feedparser.parse(url, request_headers={
        "User-Agent": "GeoRiskPulse:v1.0 (by /u/georiskresearch)"
    })
    if feed.get("status") == 429:
        print(f"      Rate limited on r/{subreddit}, waiting 30s...")
        time.sleep(30)
        feed = feedparser.parse(url, request_headers={
            "User-Agent": "GeoRiskPulse:v1.0 (by /u/georiskresearch)"
        })
    posts = []
    for entry in feed.entries:
        title = entry.get("title", "")
        # RSS entries have content in HTML
        content = ""
        if hasattr(entry, "content") and entry.content:
            content = entry.content[0].get("value", "")
        elif hasattr(entry, "summary"):
            content = entry.get("summary", "")
        # Strip HTML
        content = re.sub(r"<[^>]+>", " ", content).strip()
        content = re.sub(r"\s+", " ", content)[:500]

        published = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            published = datetime(*entry.updated_parsed[:6]).isoformat()

        posts.append({
            "title": title,
            "text": content,
            "subreddit": subreddit,
            "url": entry.get("link", ""),
            "published": published,
        })
    return posts


def fetch_social_data_for_topic(topic_name):
    """Fetch Reddit posts for a topic across all country subreddits.

    Returns list of dicts with: country, subreddit, title, text, score, type, url
    """
    topic = SOCIAL_TOPICS.get(topic_name)
    if not topic:
        return []

    filter_kw = topic["filter_keywords"]
    all_items = []

    for country, subreddits in SUBREDDIT_MAP.items():
        for sub in subreddits:
            # Fetch top posts from the week and hot posts
            for sort in ["top", "hot"]:
                print(f"    r/{sub}/{sort}...")
                posts = fetch_subreddit_rss(sub, sort=sort)
                time.sleep(3)  # rate limit — Reddit needs >2s between requests

                for post in posts:
                    text = f"{post['title']} {post['text']}".lower()
                    if not any(kw in text for kw in filter_kw):
                        continue

                    all_items.append({
                        "country": country,
                        "subreddit": sub,
                        "title": post["title"],
                        "text": post["text"],
                        "score": 0,  # RSS doesn't include score
                        "num_comments": 0,
                        "type": "post",
                        "url": post["url"],
                        "created": post.get("published", ""),
                    })

    # Deduplicate by title
    seen = set()
    unique = []
    for item in all_items:
        key = item["title"][:100]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    print(f"  Total unique social items for '{topic_name}': {len(unique)}")
    return unique
