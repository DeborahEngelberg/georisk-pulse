"""Telegram public channel scraper via Apify.

Fetches messages from public Telegram channels covering geopolitics.
Critical for Middle East, Russia, Iran perspective — platforms where
those populations actually communicate.
"""

import os

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

# Public Telegram channels by region/perspective
TELEGRAM_CHANNELS = {
    "Israel": {
        # Israeli channels
        "IsraelHayomEN": {"country": "Israel", "label": "Israel Hayom (EN)"},
        "timesofisrael": {"country": "Israel", "label": "Times of Israel"},
        # Palestinian / Arab channels
        "AlJazeeraChannel": {"country": "Qatar", "label": "Al Jazeera"},
        "aborshama1": {"country": "Palestine", "label": "Palestine News"},
        # International
        "bbcnews": {"country": "UK", "label": "BBC News"},
        "rt_com": {"country": "Russia", "label": "RT"},
        "CNN": {"country": "US", "label": "CNN"},
    },
    "US attack on Iran": {
        # Iranian channels
        "PressTV": {"country": "Iran", "label": "Press TV"},
        "IranIntl_En": {"country": "Iran (opposition)", "label": "Iran Intl"},
        "tasikinenglish": {"country": "Iran", "label": "Tasnim News"},
        # US / Western
        "CNN": {"country": "US", "label": "CNN"},
        "bbcnews": {"country": "UK", "label": "BBC News"},
        # Russian perspective
        "rt_com": {"country": "Russia", "label": "RT"},
        "taborworld": {"country": "Turkey", "label": "TRT World"},
    },
}


def fetch_telegram_messages(topic_name, max_messages=30):
    """Fetch messages from public Telegram channels for a topic.

    Returns list of dicts: {text, views, forwards, channel, country, source}
    """
    if not APIFY_TOKEN:
        print("    No APIFY_TOKEN — skipping Telegram")
        return []

    channels = TELEGRAM_CHANNELS.get(topic_name, {})
    if not channels:
        return []

    try:
        from apify_client import ApifyClient
        client = ApifyClient(APIFY_TOKEN)

        all_messages = []
        for channel_id, info in channels.items():
            print(f"    Telegram: fetching {info['label']} (@{channel_id})...")
            try:
                run = client.actor("tri_angle/telegram-scraper").call(
                    run_input={
                        "profiles": [channel_id],
                        "collectMessages": True,
                    },
                    timeout_secs=60,
                )

                count = 0
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    # Messages are in the messages array or as individual items
                    text = item.get("text", "") or item.get("message", "") or ""
                    if not text or len(text) < 15:
                        continue

                    all_messages.append({
                        "text": text[:500],
                        "views": item.get("views", 0) or 0,
                        "forwards": item.get("forwards", 0) or 0,
                        "channel": info["label"],
                        "channel_id": channel_id,
                        "country": info["country"],
                        "source": "Telegram",
                        "platform": "telegram",
                    })
                    count += 1
                    if count >= max_messages:
                        break

                print(f"      Got {count} messages")
            except Exception as e:
                print(f"      Error on @{channel_id}: {e}")
                continue

        print(f"    Telegram total: {len(all_messages)} messages")
        return all_messages

    except Exception as e:
        print(f"    Telegram error: {e}")
        return []
