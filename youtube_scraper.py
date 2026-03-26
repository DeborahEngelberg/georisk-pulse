"""YouTube video data scraper via Apify.

Fetches video titles and metadata from YouTube search results
about geopolitical topics. Uses the proven apify/youtube-scraper actor.
"""

import os


YOUTUBE_QUERIES = {
    "Israel": ["israel gaza war", "israel iran strikes", "IDF hamas 2026"],
    "US attack on Iran": ["US iran war", "trump iran strike", "iran nuclear attack 2026"],
}


def fetch_youtube_comments(topic_name, max_videos=10):
    """Fetch YouTube video data via Apify."""
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print("    No APIFY_TOKEN — skipping YouTube")
        return []

    queries = YOUTUBE_QUERIES.get(topic_name, [])
    if not queries:
        return []

    try:
        from apify_client import ApifyClient
        client = ApifyClient(token)

        all_items = []
        for query in queries[:2]:
            print(f"    YouTube: searching '{query}'...")
            try:
                run = client.actor("apidojo/youtube-scraper").call(
                    run_input={
                        "searchKeywords": query,
                        "maxResults": max_videos,
                    },
                    timeout_secs=90,
                )
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    title = item.get("title", "")
                    if not title:
                        continue
                    all_items.append({
                        "text": title,
                        "likes": item.get("likes", 0) or item.get("numberOfLikes", 0) or 0,
                        "author": item.get("channelName", ""),
                        "video_title": title,
                        "source": "YouTube",
                        "platform": "youtube",
                        "url": item.get("url", ""),
                    })
            except Exception as e:
                print(f"    YouTube query error for '{query}': {e}")
                continue

        print(f"    YouTube total: {len(all_items)} items")
        return all_items

    except Exception as e:
        print(f"    YouTube error: {e}")
        return []
