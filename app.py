import os
import json
from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from database import (
    init_db, get_scores_last_n_days, get_latest_scores, get_top_movers,
    get_sentiment_by_group, get_sentiment_headlines_sample,
    get_sentiment_trend, get_sentiment_divergence,
    get_social_by_group, get_social_trend, get_social_posts_sample,
    get_media_public_gap, get_region_stats, get_sparkline_data,
)
from economic_context import (
    ECONOMIC_EXPOSURE, HISTORICAL_BENCHMARKS, EU_AUSTRIA_EXPOSURE,
    ECONOMIC_EXPOSURE_DE, HISTORICAL_BENCHMARKS_DE, EU_AUSTRIA_EXPOSURE_DE,
    REGION_NAMES_DE,
)
from scheduler import run_daily_pipeline, run_sentiment_pipeline, run_social_pipeline

app = Flask(__name__)
init_db()

sched = BackgroundScheduler(daemon=True)
sched.add_job(run_daily_pipeline, "cron", hour=6, minute=0, id="daily_pipeline")
sched.add_job(run_sentiment_pipeline, "cron", hour=6, minute=15, id="sentiment_pipeline")
sched.add_job(run_social_pipeline, "cron", hour=6, minute=30, id="social_pipeline")
sched.start()


def _build_executive_context(lang="en"):
    """Build full context for the risk scores page."""
    scores = get_scores_last_n_days(30)
    latest = get_latest_scores()
    movers = get_top_movers(4)
    movers_map = {m["region"]: m for m in movers}

    enriched = []
    sparklines = {}
    for s in latest:
        region = s["region"]
        stats = get_region_stats(region)
        spark = get_sparkline_data(region, 7)
        sparklines[region] = spark
        enriched.append({**s, **stats, "change": movers_map.get(region, {}).get("change", 0)})

    # Generate brief
    brief_lines = []
    def _rn(region):
        """Translate region name."""
        return REGION_NAMES_DE.get(region, region) if lang == "de" else region

    if enriched:
        top = enriched[0]
        if lang == "de":
            brief_lines.append(
                f"{_rn(top['region'])}-Risiko bei {top['score']:.0f} — "
                f"{'über' if top['score'] > top.get('avg_30d', 50) else 'nahe'} dem 30-Tage-Durchschnitt von {top.get('avg_30d', 0):.0f}."
            )
        else:
            brief_lines.append(
                f"{top['region']} risk at {top['score']:.0f} — "
                f"{'above' if top['score'] > top.get('avg_30d', 50) else 'near'} 30-day average of {top.get('avg_30d', 0):.0f}."
            )
    high_count = sum(1 for s in enriched if s["score"] >= 60)
    if high_count:
        if lang == "de":
            brief_lines.append(f"{high_count} Region{'en' if high_count > 1 else ''} im Hochrisikobereich (über 60).")
        else:
            brief_lines.append(f"{high_count} region{'s' if high_count > 1 else ''} in high-risk band (>60).")
    for m in movers[:2]:
        if abs(m.get("change", 0)) > 3:
            if lang == "de":
                direction = "gestiegen" if m["change"] > 0 else "gesunken"
                brief_lines.append(f"{_rn(m['region'])} um {abs(m['change']):.0f} Punkte {direction} gegenüber Vortag.")
            else:
                direction = "up" if m["change"] > 0 else "down"
                brief_lines.append(f"{m['region']} {direction} {abs(m['change']):.0f} from prior session.")

    # Translate region names for display
    if lang == "de":
        for s in enriched:
            s["display_name"] = REGION_NAMES_DE.get(s["region"], s["region"])
    else:
        for s in enriched:
            s["display_name"] = s["region"]

    return {
        "scores_json": json.dumps(scores),
        "latest": enriched,
        "sparklines_json": json.dumps(sparklines),
        "brief_lines": brief_lines,
        "economic": ECONOMIC_EXPOSURE_DE if lang == "de" else ECONOMIC_EXPOSURE,
        "eu_austria": EU_AUSTRIA_EXPOSURE_DE if lang == "de" else EU_AUSTRIA_EXPOSURE,
        "benchmarks": HISTORICAL_BENCHMARKS_DE if lang == "de" else HISTORICAL_BENCHMARKS,
        "active_tab": "risk",
        "lang": lang,
    }


@app.route("/")
def index():
    lang = request.args.get("lang", "en")
    return render_template("index.html", **_build_executive_context(lang))


@app.route("/sentiment")
def sentiment_page():
    lang = request.args.get("lang", "en")
    return render_template("sentiment.html", active_tab="sentiment", lang=lang)


@app.route("/social")
def social_page():
    lang = request.args.get("lang", "en")
    return render_template("social.html", active_tab="social", lang=lang)


# --- Risk API ---
@app.route("/api/scores")
def api_scores():
    return jsonify(get_scores_last_n_days(int(os.environ.get("GEORISK_CHART_DAYS", 30))))

@app.route("/api/latest")
def api_latest():
    return jsonify(get_latest_scores())


# --- Media Sentiment API ---
@app.route("/api/sentiment/outlets")
def api_sentiment_outlets():
    return jsonify(get_sentiment_by_group(request.args.get("topic", "Israel"), "outlet"))

@app.route("/api/sentiment/countries")
def api_sentiment_countries():
    return jsonify(get_sentiment_by_group(request.args.get("topic", "Israel"), "country"))

@app.route("/api/sentiment/trend")
def api_sentiment_trend():
    return jsonify(get_sentiment_trend(
        request.args.get("topic", "Israel"),
        request.args.get("group", "country"),
        int(request.args.get("days", 28)),
    ))

@app.route("/api/sentiment/headlines")
def api_sentiment_headlines():
    return jsonify(get_sentiment_headlines_sample(
        request.args.get("topic", "Israel"),
        request.args.get("source"),
        int(request.args.get("limit", 20)),
    ))

@app.route("/api/sentiment/divergence")
def api_sentiment_divergence():
    return jsonify(get_sentiment_divergence(request.args.get("topic", "Israel")))


# --- Social API ---
@app.route("/api/social/countries")
def api_social_countries():
    return jsonify(get_social_by_group(request.args.get("topic", "Israel"), "country"))

@app.route("/api/social/subreddits")
def api_social_subreddits():
    return jsonify(get_social_by_group(request.args.get("topic", "Israel"), "subreddit"))

@app.route("/api/social/trend")
def api_social_trend():
    return jsonify(get_social_trend(
        request.args.get("topic", "Israel"),
        request.args.get("group", "country"),
        int(request.args.get("days", 28)),
    ))

@app.route("/api/social/posts")
def api_social_posts():
    return jsonify(get_social_posts_sample(
        request.args.get("topic", "Israel"),
        request.args.get("country"),
        int(request.args.get("limit", 25)),
    ))

@app.route("/api/social/media_gap")
def api_social_media_gap():
    return jsonify(get_media_public_gap(request.args.get("topic", "Israel")))


# --- Pipeline triggers ---
@app.route("/run", methods=["POST"])
def trigger_run():
    run_daily_pipeline()
    run_sentiment_pipeline()
    return jsonify({"status": "ok"})

@app.route("/run/sentiment", methods=["POST"])
def trigger_sentiment():
    run_sentiment_pipeline()
    return jsonify({"status": "ok"})

@app.route("/run/social", methods=["POST"])
def trigger_social():
    run_social_pipeline()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    if not get_scores_last_n_days(1):
        run_daily_pipeline()
    if not get_sentiment_by_group("Israel", "outlet"):
        run_sentiment_pipeline()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
