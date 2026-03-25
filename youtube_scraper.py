"""YouTube comments scraper via Apify.

Fetches comments from news channel videos about geopolitical topics.
Includes like counts as agreement signal.
"""

import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

# News channels to search — covers major international outlets
YOUTUBE_CHANNELS = {
    "BBC News": "https://www.youtube.com/@BBCNews",
    "Al Jazeera": "https://www.youtube.com/@AlJazeeraEnglish",
    "CNN": "https://www.youtube.com/@CNN",
    "Fox News": "https://www.youtube.com/@FoxNews",
    "DW News": "https://www.youtube.com/@DWNews",
    "France 24": "https://www.youtube.com/@FRANCE24English",
    "Sky News": "https://www.youtube.com/@SkyNews",
    "WION": "https://www.youtube.com/@WIONews",
    "TRT World": "https://www.youtube.com/@taborworld",
    "Times of Israel": "https://www.youtube.com/@TimesofIsrael",
}

# Search queries per topic
YOUTUBE_QUERIES = {
    "Israel": ["israel gaza", "israel war", "IDF hamas", "netanyahu"],
    "US attack on Iran": ["iran war", "US iran strike", "iran nuclear", "trump iran"],
}


def fetch_youtube_comments(topic_name, max_videos=8, max_comments=20):
    """Fetch YouTube comments for a topic via Apify.

    Returns list of dicts: {text, likes, author, video_title, channel, source}
    """
    if not APIFY_TOKEN:
        print("    No APIFY_TOKEN — skipping YouTube")
        return []

    queries = YOUTUBE_QUERIES.get(topic_name, [])
    if not queries:
        return []

    try:
        from apify_client import ApifyClient
        client = ApifyClient(APIFY_TOKEN)

        # Search YouTube for relevant videos
        search_urls = [f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}" for q in queries[:3]]

        print(f"    YouTube: searching for {queries[:3]}...")
        run_input = {
            "startUrls": [{"url": u} for u in search_urls],
            "maxResults": max_videos,
            "maxResultsShorts": 0,
        }

        # First get video URLs via YouTube search scraper
        search_run = client.actor("bernardo/youtube-scraper").call(
            run_input=run_input, timeout_secs=90
        )
        videos = list(client.dataset(search_run["defaultDatasetId"]).iterate_items())

        video_urls = []
        for v in videos[:max_videos]:
            url = v.get("url", "")
            if url and "watch" in url:
                video_urls.append(url)

        if not video_urls:
            print("    YouTube: no videos found")
            return []

        print(f"    YouTube: fetching comments from {len(video_urls)} videos...")
        # Now get comments
        comment_run = client.actor("streamers/youtube-comments-scraper").call(
            run_input={
                "videosUrls": video_urls,
                "maxComments": max_comments,
                "orderBy": "top",
            },
            timeout_secs=120,
        )

        all_comments = []
        for item in client.dataset(comment_run["defaultDatasetId"]).iterate_items():
            all_comments.append({
                "text": item.get("text", "")[:500],
                "likes": item.get("likes", 0) or 0,
                "author": item.get("author", ""),
                "video_title": item.get("videoTitle", ""),
                "source": "YouTube",
                "platform": "youtube",
            })

        print(f"    YouTube: {len(all_comments)} comments collected")
        return all_comments

    except Exception as e:
        print(f"    YouTube error: {e}")
        return []
