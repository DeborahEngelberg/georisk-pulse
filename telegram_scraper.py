"""Telegram public channel scraper via Apify.

Uses the proven spry_wholemeal/reddit-scraper pattern — but for Telegram.
Scrapes public channel web previews at t.me/s/channel.
"""

import os
import re
import requests


# Only channels with web preview enabled (t.me/s/channel works)
TELEGRAM_CHANNELS = {
    "Israel": {
        "RVvoenkor": {"country": "Russia", "label": "Russian War Correspondent"},
        "MiddleEastObserver": {"country": "Global", "label": "Middle East Observer"},
        "gazaupdates": {"country": "Palestine", "label": "Gaza Updates"},
        "CIG_telegram": {"country": "Global", "label": "Clandestine Intel"},
        "intelslava": {"country": "Russia", "label": "Intel Slava Z"},
        "militaryintel": {"country": "Global", "label": "Military Intel"},
        "IsraelRadar": {"country": "Israel", "label": "Israel Radar"},
    },
    "US attack on Iran": {
        "RVvoenkor": {"country": "Russia", "label": "Russian War Correspondent"},
        "MiddleEastObserver": {"country": "Global", "label": "Middle East Observer"},
        "CIG_telegram": {"country": "Global", "label": "Clandestine Intel"},
        "intelslava": {"country": "Russia", "label": "Intel Slava Z"},
        "militaryintel": {"country": "Global", "label": "Military Intel"},
        "ukrainenewslive": {"country": "Ukraine", "label": "Ukraine News Live"},
    },
}


def _scrape_telegram_web(channel_id, max_messages=15):
    """Scrape public Telegram channel via web preview (no API needed)."""
    url = f"https://t.me/s/{channel_id}"
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        })
        if resp.status_code != 200:
            return []

        # Extract message text from HTML
        messages = re.findall(
            r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
            resp.text, re.DOTALL
        )
        # Extract view counts
        views = re.findall(
            r'<span class="tgme_widget_message_views">([^<]+)</span>',
            resp.text
        )

        results = []
        for i, msg_html in enumerate(messages[:max_messages]):
            text = re.sub(r'<[^>]+>', '', msg_html).strip()
            if len(text) < 15:
                continue

            view_count = 0
            if i < len(views):
                v = views[i].strip()
                if 'K' in v:
                    view_count = int(float(v.replace('K', '')) * 1000)
                elif 'M' in v:
                    view_count = int(float(v.replace('M', '')) * 1000000)
                else:
                    try:
                        view_count = int(v)
                    except ValueError:
                        pass

            results.append({"text": text[:500], "views": view_count})

        return results
    except Exception as e:
        print(f"      Web scrape error for @{channel_id}: {e}")
        return []


def fetch_telegram_messages(topic_name, max_messages=15):
    """Fetch messages from public Telegram channels.

    Uses direct web scraping of t.me/s/channel — no Apify or API key needed.
    """
    channels = TELEGRAM_CHANNELS.get(topic_name, {})
    if not channels:
        return []

    all_messages = []
    for channel_id, info in channels.items():
        print(f"    Telegram: @{channel_id}...")
        messages = _scrape_telegram_web(channel_id, max_messages)
        for m in messages:
            all_messages.append({
                "text": m["text"],
                "views": m["views"],
                "forwards": 0,
                "channel": info["label"],
                "channel_id": channel_id,
                "country": info["country"],
                "source": "Telegram",
                "platform": "telegram",
                "url": f"https://t.me/s/{channel_id}",
            })
        print(f"      Got {len(messages)} messages")

    print(f"    Telegram total: {len(all_messages)} messages")
    return all_messages
