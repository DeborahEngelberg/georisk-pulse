"""Scrape Reddit posts and comments for social sentiment analysis.

Primary: Apify Reddit scraper (posts + comments + upvotes)
Fallback: Reddit RSS feeds (post titles only, no comments)

Set APIFY_TOKEN env var to enable Apify. Without it, falls back to RSS.
"""

import os
import re
import time
import feedparser
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

# Country-specific subreddits
SUBREDDIT_MAP = {
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
    "Global": ["worldnews", "geopolitics", "InternationalNews"],
}

SOCIAL_TOPICS = {
    "Israel": {
        "queries": ["israel", "gaza", "IDF", "hamas", "netanyahu"],
        "filter_keywords": ["israel", "israeli", "gaza", "hamas", "idf",
                            "netanyahu", "hezbollah", "west bank", "tel aviv",
                            "jerusalem", "kibbutz", "golan", "zionist"],
    },
    "US attack on Iran": {
        "queries": ["iran war", "iran strike", "US iran"],
        "filter_keywords": ["iran", "iranian", "tehran", "strike", "attack",
                            "war", "bomb", "missile", "centcom", "pentagon"],
    },
}


def _fetch_apify(subreddits, queries, max_posts=15, max_comments=10):
    """Fetch posts + comments via Apify Reddit scraper."""
    if not APIFY_TOKEN:
        return None

    try:
        from apify_client import ApifyClient
        client = ApifyClient(APIFY_TOKEN)
        actor = client.actor("spry_wholemeal/reddit-scraper")

        run_input = {
            "subreddits": subreddits,
            "queries": queries,
            "maxPostsPerSubreddit": max_posts,
            "maxPostsPerQuery": max_posts,
            "commentsLimit": max_comments,
            "sort": "hot",
        }

        print(f"    Apify: fetching r/{', r/'.join(subreddits)} for {queries}...")
        result = actor.call(run_input=run_input, timeout_secs=120)
        dataset = client.dataset(result["defaultDatasetId"])
        items = dataset.list_items().items
        return items
    except Exception as e:
        print(f"    Apify error: {e}")
        return None


def _fetch_rss(subreddit, sort="top"):
    """Fallback: fetch post titles via Reddit RSS."""
    if sort == "top":
        url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t=week"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot/.rss"

    feed = feedparser.parse(url, request_headers={
        "User-Agent": "GeoRiskPulse:v1.0 (by /u/georiskresearch)"
    })
    if feed.get("status") == 429:
        time.sleep(30)
        feed = feedparser.parse(url, request_headers={
            "User-Agent": "GeoRiskPulse:v1.0 (by /u/georiskresearch)"
        })

    posts = []
    for entry in feed.entries:
        title = entry.get("title", "")
        content = ""
        if hasattr(entry, "content") and entry.content:
            content = entry.content[0].get("value", "")
        elif hasattr(entry, "summary"):
            content = entry.get("summary", "")
        content = re.sub(r"<[^>]+>", " ", content).strip()
        content = re.sub(r"\s+", " ", content)[:500]

        posts.append({
            "title": title,
            "text": content,
            "subreddit": subreddit,
            "url": entry.get("link", ""),
            "score": 0,
            "num_comments": 0,
            "type": "post",
        })
    return posts


def fetch_social_data_for_topic(topic_name):
    """Fetch Reddit data for a topic across all country subreddits.

    Uses Apify if APIFY_TOKEN is set (gets posts + comments + upvotes).
    Falls back to RSS (post titles only).
    """
    topic = SOCIAL_TOPICS.get(topic_name)
    if not topic:
        return []

    filter_kw = topic["filter_keywords"]
    all_items = []

    if APIFY_TOKEN:
        # Apify mode: fetch all subreddits at once per country
        for country, subreddits in SUBREDDIT_MAP.items():
            queries = topic.get("queries", [])[:2]
            apify_data = _fetch_apify(subreddits, queries, max_posts=10, max_comments=5)
            if not apify_data:
                continue

            for item in apify_data:
                title = item.get("title", "")
                text = item.get("text", "") or ""
                sub = item.get("subreddit", {})
                sub_name = sub.get("display_name", "") if isinstance(sub, dict) else str(sub)

                # Check relevance
                check = f"{title} {text}".lower()
                if not any(kw in check for kw in filter_kw):
                    continue

                # Add the post
                all_items.append({
                    "country": country,
                    "subreddit": sub_name or subreddits[0],
                    "title": title,
                    "text": text[:500],
                    "score": item.get("score", 0),
                    "num_comments": item.get("num_comments", 0),
                    "type": "post",
                    "url": f"https://reddit.com{item.get('permalink', '')}",
                    "created": item.get("created_utc_iso", ""),
                })

                # Add comments
                for comment in item.get("comments", []):
                    body = comment.get("text", "")
                    if not body or len(body) < 10:
                        continue
                    all_items.append({
                        "country": country,
                        "subreddit": sub_name or subreddits[0],
                        "title": title,
                        "text": body[:500],
                        "score": comment.get("score", 0),
                        "num_comments": 0,
                        "type": "comment",
                        "url": f"https://reddit.com{item.get('permalink', '')}",
                        "created": item.get("created_utc_iso", ""),
                    })

            time.sleep(1)
    else:
        # RSS fallback: post titles only
        print("    No APIFY_TOKEN — using RSS fallback (posts only, no comments)")
        for country, subreddits in SUBREDDIT_MAP.items():
            for sub in subreddits:
                for sort in ["top", "hot"]:
                    posts = _fetch_rss(sub, sort=sort)
                    time.sleep(3)
                    for post in posts:
                        text = f"{post['title']} {post['text']}".lower()
                        if not any(kw in text for kw in filter_kw):
                            continue
                        all_items.append({**post, "country": country, "created": ""})

    # Deduplicate by title
    seen = set()
    unique = []
    for item in all_items:
        key = (item["title"][:80], item["type"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    posts_count = sum(1 for i in unique if i["type"] == "post")
    comments_count = sum(1 for i in unique if i["type"] == "comment")
    print(f"  Total for '{topic_name}': {posts_count} posts + {comments_count} comments = {len(unique)} items")
    return unique
