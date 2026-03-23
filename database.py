import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.environ.get("GEORISK_DB", "georisk.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            link TEXT,
            published TEXT,
            score REAL DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS daily_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            date TEXT NOT NULL,
            score REAL NOT NULL,
            headline_count INTEGER DEFAULT 0,
            UNIQUE(region, date)
        );
        CREATE INDEX IF NOT EXISTS idx_daily_region_date ON daily_scores(region, date);
        CREATE INDEX IF NOT EXISTS idx_headlines_region ON headlines(region, created_at);

        CREATE TABLE IF NOT EXISTS sentiment_headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            link TEXT,
            published TEXT,
            polarity REAL DEFAULT 0,
            subjectivity REAL DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS sentiment_aggregates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            group_type TEXT NOT NULL,
            group_name TEXT NOT NULL,
            date TEXT NOT NULL,
            avg_polarity REAL NOT NULL,
            avg_subjectivity REAL DEFAULT 0,
            headline_count INTEGER DEFAULT 0,
            UNIQUE(topic, group_type, group_name, date)
        );
        CREATE INDEX IF NOT EXISTS idx_sent_topic ON sentiment_headlines(topic, created_at);
        CREATE INDEX IF NOT EXISTS idx_sent_agg ON sentiment_aggregates(topic, group_type, date);

        CREATE TABLE IF NOT EXISTS social_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            country TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            title TEXT NOT NULL,
            text TEXT,
            polarity REAL DEFAULT 0,
            subjectivity REAL DEFAULT 0,
            reddit_score INTEGER DEFAULT 0,
            post_type TEXT DEFAULT 'post',
            url TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS social_aggregates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            group_type TEXT NOT NULL,
            group_name TEXT NOT NULL,
            date TEXT NOT NULL,
            avg_polarity REAL NOT NULL,
            avg_subjectivity REAL DEFAULT 0,
            post_count INTEGER DEFAULT 0,
            avg_reddit_score REAL DEFAULT 0,
            UNIQUE(topic, group_type, group_name, date)
        );
        CREATE INDEX IF NOT EXISTS idx_social_topic ON social_posts(topic, country);
        CREATE INDEX IF NOT EXISTS idx_social_agg ON social_aggregates(topic, group_type, date);
    """)
    conn.commit()
    conn.close()


def get_region_stats(region):
    """Return 7d/30d/90d averages and peak for a region."""
    conn = get_conn()
    stats = {}
    for label, days in [("7d", 7), ("30d", 30), ("90d", 90)]:
        cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        row = conn.execute(
            "SELECT AVG(score) as avg FROM daily_scores WHERE region = ? AND date >= ?",
            (region, cutoff),
        ).fetchone()
        stats[f"avg_{label}"] = round(row["avg"], 1) if row["avg"] else 0
    peak = conn.execute(
        "SELECT score, date FROM daily_scores WHERE region = ? ORDER BY score DESC LIMIT 1",
        (region,),
    ).fetchone()
    stats["peak_score"] = round(peak["score"], 1) if peak else 0
    stats["peak_date"] = peak["date"] if peak else ""
    conn.close()
    return stats


def get_sparkline_data(region, days=7):
    """Return last N days of scores for sparkline rendering."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = get_conn()
    rows = conn.execute(
        "SELECT date, score FROM daily_scores WHERE region = ? AND date >= ? ORDER BY date",
        (region, cutoff),
    ).fetchall()
    conn.close()
    return [row["score"] for row in rows]


def get_sentiment_divergence(topic):
    """Compute narrative divergence: spread between outlet extremes."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT sa.group_name, sa.avg_polarity, sa.headline_count
        FROM sentiment_aggregates sa
        INNER JOIN (
            SELECT group_name, MAX(date) as max_date
            FROM sentiment_aggregates WHERE topic = ? AND group_type = 'outlet'
            GROUP BY group_name
        ) latest ON sa.group_name = latest.group_name AND sa.date = latest.max_date
        WHERE sa.topic = ? AND sa.group_type = 'outlet'
        ORDER BY sa.avg_polarity
    """, (topic, topic)).fetchall()
    conn.close()
    if len(rows) < 2:
        return {}
    rows = [dict(r) for r in rows]
    most_neg = rows[0]
    most_pos = rows[-1]
    return {
        "divergence": round(most_pos["avg_polarity"] - most_neg["avg_polarity"], 3),
        "most_negative": {"outlet": most_neg["group_name"], "polarity": most_neg["avg_polarity"]},
        "most_positive": {"outlet": most_pos["group_name"], "polarity": most_pos["avg_polarity"]},
        "outlet_count": len(rows),
    }


def get_media_public_gap(topic):
    """Per-country gap between media and Reddit sentiment."""
    media = {r["group_name"]: r["avg_polarity"] for r in get_sentiment_by_group(topic, "country")}
    social = {r["group_name"]: r["avg_polarity"] for r in get_social_by_group(topic, "country")}
    gaps = []
    for country in set(media.keys()) & set(social.keys()):
        m, s = media[country], social[country]
        gaps.append({
            "country": country,
            "media_polarity": m,
            "public_polarity": s,
            "gap": round(abs(m - s), 3),
            "direction": "Public more critical" if s < m else "Public more favorable",
        })
    gaps.sort(key=lambda x: -x["gap"])
    return gaps


def store_headlines(headlines):
    """Store a list of headline dicts: {region, title, source, link, published, score}."""
    conn = get_conn()
    conn.executemany(
        "INSERT INTO headlines (region, title, source, link, published, score) VALUES (?, ?, ?, ?, ?, ?)",
        [(h["region"], h["title"], h["source"], h["link"], h["published"], h["score"]) for h in headlines],
    )
    conn.commit()
    conn.close()


def store_daily_score(region, date_str, score, headline_count):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO daily_scores (region, date, score, headline_count) VALUES (?, ?, ?, ?)",
        (region, date_str, score, headline_count),
    )
    conn.commit()
    conn.close()


def get_scores_last_n_days(n=30):
    """Return daily scores for all regions over the last n days."""
    cutoff = (datetime.utcnow() - timedelta(days=n)).strftime("%Y-%m-%d")
    conn = get_conn()
    rows = conn.execute(
        "SELECT region, date, score FROM daily_scores WHERE date >= ? ORDER BY date",
        (cutoff,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_scores():
    """Return the most recent score per region."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT ds.region, ds.date, ds.score, ds.headline_count
        FROM daily_scores ds
        INNER JOIN (SELECT region, MAX(date) as max_date FROM daily_scores GROUP BY region) latest
        ON ds.region = latest.region AND ds.date = latest.max_date
        ORDER BY ds.score DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_top_movers(n=3):
    """Return regions with biggest score change vs previous day."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT a.region, a.score as current_score, b.score as prev_score,
               (a.score - COALESCE(b.score, 0)) as change
        FROM daily_scores a
        LEFT JOIN daily_scores b ON a.region = b.region AND b.date = date(a.date, '-1 day')
        WHERE a.date = (SELECT MAX(date) FROM daily_scores)
        ORDER BY ABS(a.score - COALESCE(b.score, 0)) DESC
        LIMIT ?
    """, (n,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Sentiment tables ---

def store_sentiment_headlines(headlines):
    conn = get_conn()
    conn.executemany(
        """INSERT INTO sentiment_headlines
           (topic, title, source, country, region, link, published, polarity, subjectivity)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(h["topic"], h["title"], h["source"], h["country"], h["region"],
          h.get("link", ""), h.get("published", ""), h["polarity"], h["subjectivity"])
         for h in headlines],
    )
    conn.commit()
    conn.close()


def store_sentiment_aggregates(topic, group_type, agg_dict, date_str):
    conn = get_conn()
    for name, data in agg_dict.items():
        conn.execute(
            """INSERT OR REPLACE INTO sentiment_aggregates
               (topic, group_type, group_name, date, avg_polarity, avg_subjectivity, headline_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (topic, group_type, name, date_str,
             data["avg_polarity"], data["avg_subjectivity"], data["headline_count"]),
        )
    conn.commit()
    conn.close()


def get_sentiment_by_group(topic, group_type):
    """Get latest sentiment aggregates for a topic grouped by outlet or country."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT sa.group_name, sa.avg_polarity, sa.avg_subjectivity, sa.headline_count, sa.date
        FROM sentiment_aggregates sa
        INNER JOIN (
            SELECT group_name, MAX(date) as max_date
            FROM sentiment_aggregates
            WHERE topic = ? AND group_type = ?
            GROUP BY group_name
        ) latest ON sa.group_name = latest.group_name AND sa.date = latest.max_date
        WHERE sa.topic = ? AND sa.group_type = ?
        ORDER BY sa.avg_polarity ASC
    """, (topic, group_type, topic, group_type)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_sentiment_trend(topic, group_type, days=28):
    """Get sentiment over time for all groups of a given type."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = get_conn()
    rows = conn.execute("""
        SELECT group_name, date, avg_polarity, headline_count
        FROM sentiment_aggregates
        WHERE topic = ? AND group_type = ? AND date >= ?
        ORDER BY date
    """, (topic, group_type, cutoff)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_sentiment_headlines_sample(topic, source=None, limit=10):
    """Get sample headlines with sentiment scores for a topic."""
    conn = get_conn()
    if source:
        rows = conn.execute("""
            SELECT title, source, country, polarity, subjectivity, link
            FROM sentiment_headlines
            WHERE topic = ? AND source = ?
            ORDER BY created_at DESC LIMIT ?
        """, (topic, source, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT title, source, country, polarity, subjectivity, link
            FROM sentiment_headlines WHERE topic = ?
            ORDER BY created_at DESC LIMIT ?
        """, (topic, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Social sentiment tables ---

def store_social_posts(posts):
    conn = get_conn()
    conn.executemany(
        """INSERT INTO social_posts
           (topic, country, subreddit, title, text, polarity, subjectivity, reddit_score, post_type, url)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(p["topic"], p["country"], p["subreddit"], p["title"],
          p.get("text", "")[:500], p["polarity"], p["subjectivity"],
          p.get("score", 0), p.get("type", "post"), p.get("url", ""))
         for p in posts],
    )
    conn.commit()
    conn.close()


def store_social_aggregates(topic, group_type, agg_dict, date_str):
    conn = get_conn()
    for name, data in agg_dict.items():
        conn.execute(
            """INSERT OR REPLACE INTO social_aggregates
               (topic, group_type, group_name, date, avg_polarity, avg_subjectivity, post_count, avg_reddit_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (topic, group_type, name, date_str,
             data["avg_polarity"], data["avg_subjectivity"],
             data["post_count"], data.get("avg_reddit_score", 0)),
        )
    conn.commit()
    conn.close()


def get_social_by_group(topic, group_type):
    """Get latest social sentiment aggregates."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT sa.group_name, sa.avg_polarity, sa.avg_subjectivity, sa.post_count,
               sa.avg_reddit_score, sa.date
        FROM social_aggregates sa
        INNER JOIN (
            SELECT group_name, MAX(date) as max_date
            FROM social_aggregates WHERE topic = ? AND group_type = ?
            GROUP BY group_name
        ) latest ON sa.group_name = latest.group_name AND sa.date = latest.max_date
        WHERE sa.topic = ? AND sa.group_type = ?
        ORDER BY sa.avg_polarity ASC
    """, (topic, group_type, topic, group_type)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_social_trend(topic, group_type, days=28):
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = get_conn()
    rows = conn.execute("""
        SELECT group_name, date, avg_polarity, post_count
        FROM social_aggregates WHERE topic = ? AND group_type = ? AND date >= ?
        ORDER BY date
    """, (topic, group_type, cutoff)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_social_posts_sample(topic, country=None, limit=20):
    conn = get_conn()
    if country:
        rows = conn.execute("""
            SELECT title, text, country, subreddit, polarity, reddit_score, post_type, url
            FROM social_posts WHERE topic = ? AND country = ?
            ORDER BY reddit_score DESC LIMIT ?
        """, (topic, country, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT title, text, country, subreddit, polarity, reddit_score, post_type, url
            FROM social_posts WHERE topic = ?
            ORDER BY reddit_score DESC LIMIT ?
        """, (topic, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
