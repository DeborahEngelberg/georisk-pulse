"""Telegram public channel scraper via Apify.

Fetches messages from public Telegram channels covering geopolitics.
Uses web preview (t.me/s/channel) — no Telegram API key needed.
"""

import os

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

TELEGRAM_CHANNELS = {
    "Israel": {
        "bbcnews": {"country": "UK", "label": "BBC News"},
        "caborshama1": {"country": "Palestine", "label": "Palestine Resistance"},
        "rt_com": {"country": "Russia", "label": "RT News"},
    },
    "US attack on Iran": {
        "PressTV": {"country": "Iran", "label": "Press TV"},
        "bbcnews": {"country": "UK", "label": "BBC News"},
        "rt_com": {"country": "Russia", "label": "RT News"},
    },
}


def fetch_telegram_messages(topic_name, max_messages=15):
    """Fetch messages from public Telegram channels."""
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
            print(f"    Telegram: @{channel_id}...")
            try:
                run = client.actor("apify/web-scraper").call(
                    run_input={
                        "startUrls": [{"url": f"https://t.me/s/{channel_id}"}],
                        "pageFunction": """async function pageFunction(context) {
                            const { page, request } = context;
                            await page.waitForSelector('.tgme_widget_message_wrap', { timeout: 10000 });
                            const messages = await page.$$eval('.tgme_widget_message_text', els =>
                                els.map(el => el.innerText).filter(t => t.length > 10)
                            );
                            const views = await page.$$eval('.tgme_widget_message_views', els =>
                                els.map(el => {
                                    const t = el.innerText.trim();
                                    if (t.includes('K')) return parseFloat(t) * 1000;
                                    if (t.includes('M')) return parseFloat(t) * 1000000;
                                    return parseInt(t) || 0;
                                })
                            );
                            return messages.map((text, i) => ({
                                text: text.substring(0, 500),
                                views: views[i] || 0,
                                url: request.url,
                            }));
                        }""",
                    },
                    timeout_secs=60,
                )

                count = 0
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    text = item.get("text", "")
                    if not text or len(text) < 15:
                        continue
                    all_messages.append({
                        "text": text[:500],
                        "views": item.get("views", 0) or 0,
                        "forwards": 0,
                        "channel": info["label"],
                        "channel_id": channel_id,
                        "country": info["country"],
                        "source": "Telegram",
                        "platform": "telegram",
                        "url": f"https://t.me/s/{channel_id}",
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
