"""YouTube comments scraper via Apify.

Fetches comments from news videos about geopolitical topics.
Uses a single actor call with search URLs.
"""

import os

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

YOUTUBE_QUERIES = {
    "Israel": ["israel gaza war 2026", "israel iran strikes", "IDF hamas"],
    "US attack on Iran": ["US iran war 2026", "trump iran strike", "iran nuclear attack"],
}


def fetch_youtube_comments(topic_name, max_comments=20):
    """Fetch YouTube comments via Apify."""
    if not APIFY_TOKEN:
        print("    No APIFY_TOKEN — skipping YouTube")
        return []

    queries = YOUTUBE_QUERIES.get(topic_name, [])
    if not queries:
        return []

    try:
        from apify_client import ApifyClient
        client = ApifyClient(APIFY_TOKEN)

        # Use the dedicated comments scraper with search URLs
        search_urls = [
            f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}"
            for q in queries[:2]
        ]

        print(f"    YouTube: searching {queries[:2]}...")

        # Try the comments scraper directly with video search
        run = client.actor("apidojo/youtube-scraper").call(
            run_input={
                "startUrls": [{"url": u} for u in search_urls],
                "maxResults": 5,
                "maxResultsShorts": 0,
                "subtitlesLanguage": "en",
            },
            timeout_secs=120,
        )

        all_comments = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            title = item.get("title", "")
            # The scraper returns videos — extract title as a data point
            all_comments.append({
                "text": title,
                "likes": item.get("numberOfLikes", 0) or 0,
                "author": item.get("channelName", ""),
                "video_title": title,
                "source": "YouTube",
                "platform": "youtube",
                "url": item.get("url", ""),
            })

        print(f"    YouTube: {len(all_comments)} items collected")
        return all_comments

    except Exception as e:
        print(f"    YouTube error: {e}")
        return []
