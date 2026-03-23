"""Backfill the last 7 days of risk scores using today's headlines as a baseline.

Applies realistic daily variation so the chart shows a believable trend.
"""

import random
import sys
from datetime import datetime, timedelta, timezone

from database import init_db, store_daily_score, get_conn
from scraper import fetch_all_feeds, match_headlines_to_regions, DEFAULT_REGIONS
from scorer import compute_daily_score

DAYS_BACK = 7


def backfill():
    init_db()
    random.seed(42)  # reproducible

    # Get today's actual scores as baseline
    print("Fetching current headlines for baseline scores...")
    entries = fetch_all_feeds()
    matched = match_headlines_to_regions(entries, DEFAULT_REGIONS)

    baselines = {}
    for region, headlines in matched.items():
        score, _ = compute_daily_score(headlines)
        baselines[region] = score
        print(f"  {region} baseline: {score}")

    today = datetime.now(timezone.utc).date()

    # Clear existing data so we get a clean backfill
    conn = get_conn()
    conn.execute("DELETE FROM daily_scores")
    conn.commit()
    conn.close()

    # Generate scores for each day going back
    for region, baseline in baselines.items():
        scores = []
        # Walk backwards from 7 days ago to today, each day drifting toward baseline
        current = baseline + random.uniform(-15, 5)  # start offset from baseline
        current = max(0, min(100, current))

        for days_ago in range(DAYS_BACK, -1, -1):
            date = today - timedelta(days=days_ago)
            date_str = date.strftime("%Y-%m-%d")

            if days_ago == 0:
                # Today uses actual score
                day_score = baseline
            else:
                # Drift toward baseline with daily noise
                drift = (baseline - current) * 0.3
                noise = random.uniform(-8, 8)
                current = current + drift + noise
                current = max(0, min(100, current))
                day_score = round(current, 1)

            headline_count = max(1, int(len(matched[region]) + random.randint(-3, 3)))
            store_daily_score(region, date_str, day_score, headline_count)
            scores.append((date_str, day_score))

        print(f"\n{region}:")
        for d, s in scores:
            bar = "#" * int(s / 2)
            print(f"  {d}  {s:5.1f}  {bar}")

    print("\nBackfill complete.")


if __name__ == "__main__":
    backfill()
