"""Scheduled jobs: scrape feeds, score headlines, store results, send digest."""

from datetime import datetime, timezone
from scraper import fetch_all_feeds, match_headlines_to_regions, DEFAULT_REGIONS
from scorer import compute_daily_score
from database import store_headlines, store_daily_score, init_db
from emailer import send_daily_digest


def run_daily_pipeline(regions=None):
    """Run the full scrape -> score -> store -> email pipeline."""
    if regions is None:
        regions = DEFAULT_REGIONS

    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting daily pipeline...")

    # 1. Fetch feeds
    entries = fetch_all_feeds()
    print(f"  Fetched {len(entries)} total entries")

    # 2. Match to regions
    matched = match_headlines_to_regions(entries, regions)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 3. Score and store per region
    for region, headlines in matched.items():
        score, scored_headlines = compute_daily_score(headlines)
        print(f"  {region}: {len(headlines)} headlines, score={score}")

        if scored_headlines:
            store_headlines([{**h, "region": region} for h in scored_headlines])
        store_daily_score(region, today, score, len(headlines))

    # 4. Send digest
    send_daily_digest()

    print("Pipeline complete.")


def run_sentiment_pipeline():
    """Run the sentiment analysis pipeline for all topics."""
    from sentiment_scraper import fetch_sentiment_feeds, filter_by_topic, SENTIMENT_TOPICS
    from sentiment import analyze_batch, aggregate_by_outlet, aggregate_by_country
    from database import store_sentiment_headlines, store_sentiment_aggregates

    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting sentiment pipeline...")

    entries = fetch_sentiment_feeds()
    print(f"  Fetched {len(entries)} entries from international feeds")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for topic_name in SENTIMENT_TOPICS:
        relevant = filter_by_topic(entries, topic_name)
        print(f"  {topic_name}: {len(relevant)} matching headlines")

        if not relevant:
            continue

        scored = analyze_batch(relevant)
        store_sentiment_headlines([{**h, "topic": topic_name} for h in scored])

        outlet_agg = aggregate_by_outlet(scored)
        country_agg = aggregate_by_country(scored)
        store_sentiment_aggregates(topic_name, "outlet", outlet_agg, today)
        store_sentiment_aggregates(topic_name, "country", country_agg, today)

        for name, data in sorted(outlet_agg.items(), key=lambda x: x[1]["avg_polarity"]):
            bar_len = int((data["avg_polarity"] + 1) * 20)  # -1..+1 mapped to 0..40
            bar = "#" * bar_len
            print(f"    {name:20s}  polarity={data['avg_polarity']:+.3f}  ({data['headline_count']} headlines)  {bar}")

    print("Sentiment pipeline complete.")


def run_social_pipeline():
    """Run the social media sentiment pipeline."""
    from social_scraper import fetch_social_data_for_topic, SOCIAL_TOPICS
    from sentiment import analyze_headline
    from database import store_social_posts, store_social_aggregates
    from collections import defaultdict

    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting social pipeline...")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for topic_name in SOCIAL_TOPICS:
        print(f"\n  Fetching Reddit data for '{topic_name}'...")
        items = fetch_social_data_for_topic(topic_name)

        if not items:
            print(f"  No social data for {topic_name}")
            continue

        # Score each item
        scored = []
        for item in items:
            sent = analyze_headline(item["title"], item.get("text", ""))
            scored.append({**item, **sent, "topic": topic_name})

        store_social_posts(scored)

        # Aggregate by country
        by_country = defaultdict(list)
        for s in scored:
            by_country[s["country"]].append(s)

        country_agg = {}
        for country, posts in by_country.items():
            pols = [p["polarity"] for p in posts]
            subs = [p["subjectivity"] for p in posts]
            reddit_scores = [p["score"] for p in posts]
            country_agg[country] = {
                "avg_polarity": round(sum(pols) / len(pols), 3),
                "avg_subjectivity": round(sum(subs) / len(subs), 3),
                "post_count": len(posts),
                "avg_reddit_score": round(sum(reddit_scores) / len(reddit_scores), 1),
            }
        store_social_aggregates(topic_name, "country", country_agg, today)

        # Aggregate by subreddit
        by_sub = defaultdict(list)
        for s in scored:
            by_sub[s["subreddit"]].append(s)

        sub_agg = {}
        for sub, posts in by_sub.items():
            pols = [p["polarity"] for p in posts]
            subs_list = [p["subjectivity"] for p in posts]
            reddit_scores = [p["score"] for p in posts]
            sub_agg[sub] = {
                "avg_polarity": round(sum(pols) / len(pols), 3),
                "avg_subjectivity": round(sum(subs_list) / len(subs_list), 3),
                "post_count": len(posts),
                "avg_reddit_score": round(sum(reddit_scores) / len(reddit_scores), 1),
            }
        store_social_aggregates(topic_name, "subreddit", sub_agg, today)

        print(f"\n  {topic_name} — by country:")
        for name, data in sorted(country_agg.items(), key=lambda x: x[1]["avg_polarity"]):
            print(f"    {name:18s}  {data['avg_polarity']:+.3f}  ({data['post_count']:3d} posts, avg score {data['avg_reddit_score']:.0f})")

    print("\nSocial pipeline complete.")


if __name__ == "__main__":
    init_db()
    run_daily_pipeline()
    run_sentiment_pipeline()
    run_social_pipeline()
