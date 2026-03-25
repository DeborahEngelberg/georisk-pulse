"""Sentiment analysis engine for geopolitical headlines.

TextBlob fails on war/political language ("high-level assassinations" = +0.8).
This uses a custom geopolitical lexicon where words are scored in context.
"""

import re
from collections import defaultdict

# German lexicon — for Austrian/German-language outlets (ORF, Der Standard, DW)
NEGATIVE_WORDS_DE = {
    # Gewalt / Zerstörung
    "krieg": -0.5, "angriff": -0.4, "angriffe": -0.4, "attacke": -0.4,
    "bombe": -0.6, "bomben": -0.6, "bombardierung": -0.6, "beschuss": -0.5,
    "rakete": -0.4, "raketen": -0.4, "luftangriff": -0.5, "luftangriffe": -0.5,
    "invasion": -0.6, "offensive": -0.4, "eskalation": -0.5,
    "drohne": -0.3, "drohnen": -0.3, "vergeltung": -0.4,
    "explosion": -0.5, "zerstörung": -0.6, "zerstört": -0.5,
    # Opfer / Leid
    "getötet": -0.7, "tötung": -0.5, "tod": -0.5, "tote": -0.6,
    "opfer": -0.5, "verwundet": -0.5, "verletzt": -0.5, "verletzte": -0.5,
    "zivilisten": -0.3, "flüchtlinge": -0.4, "vertriebene": -0.4,
    "massaker": -0.9, "völkermord": -0.9, "genozid": -0.9,
    # Verurteilung
    "verurteilt": -0.4, "kritisiert": -0.3, "warnt": -0.3, "droht": -0.4,
    "sanktionen": -0.4, "embargo": -0.5, "blockade": -0.5,
    "krise": -0.5, "konflikt": -0.4, "spannungen": -0.3,
    "gefahr": -0.4, "bedrohung": -0.4, "terrorismus": -0.5,
    # Negative Ergebnisse
    "scheitert": -0.4, "ablehnung": -0.3, "zusammenbruch": -0.5,
    "katastrophe": -0.7, "notstand": -0.5, "chaos": -0.5,
    "verluste": -0.4, "einbruch": -0.4, "einbußen": -0.4,
    # Wirtschaftlich negativ
    "sinken": -0.2, "sinkt": -0.2, "fällt": -0.2, "fallen": -0.2,
    "teurer": -0.2, "teurere": -0.2, "teuerung": -0.3, "inflation": -0.3,
    "rezession": -0.4, "abschwung": -0.3,
    # Militärisch
    "truppen": -0.3, "soldaten": -0.3, "militär": -0.3, "armee": -0.3,
    "panzer": -0.3, "kampf": -0.4, "gefecht": -0.4,
    "atomwaffen": -0.6, "nuklear": -0.5, "atomanlagen": -0.4,
    "achillesferse": -0.4, "unbekannte": -0.2,
}

POSITIVE_WORDS_DE = {
    # Frieden / Diplomatie
    "frieden": 0.5, "friedens": 0.4, "waffenstillstand": 0.4, "waffenruhe": 0.4,
    "verhandlungen": 0.3, "gespräche": 0.3, "diplomatie": 0.4,
    "abkommen": 0.4, "einigung": 0.4, "vermittlung": 0.4,
    "deeskalation": 0.5,
    # Hilfe
    "hilfe": 0.3, "humanitär": 0.2, "rettung": 0.4, "wiederaufbau": 0.3,
    "schutz": 0.3, "sicherheit": 0.2,
    # Fortschritt
    "hoffnung": 0.4, "fortschritt": 0.3, "durchbruch": 0.5,
    "zusammenarbeit": 0.3, "stabilität": 0.3,
    "freilassung": 0.4, "befreiung": 0.3,
    # Wirtschaftlich positiv
    "steigt": 0.2, "steigen": 0.2, "wachstum": 0.3, "erholung": 0.3,
    "aufschwung": 0.3, "stabil": 0.2,
}


# English lexicon
# Negative-framing words: suggest critical, hostile, or alarming tone
# Score from -0.1 (mildly negative) to -1.0 (extremely negative)
NEGATIVE_WORDS = {
    # Violence / destruction
    "kill": -0.7, "killed": -0.7, "killing": -0.7, "slaughter": -0.9,
    "massacre": -0.9, "murder": -0.8, "dead": -0.6, "death": -0.5, "suicide": -0.5, "bomber": -0.6,
    "deaths": -0.5, "die": -0.5, "died": -0.5, "destroy": -0.6,
    "destroyed": -0.6, "destruction": -0.6, "devastation": -0.7,
    "rubble": -0.5, "bomb": -0.6, "bombing": -0.6, "bombed": -0.6,
    "blast": -0.5, "explosion": -0.5, "missile": -0.4, "missiles": -0.4,
    "rocket": -0.4, "rockets": -0.4, "airstrike": -0.5, "airstrikes": -0.5,
    "strike": -0.3, "strikes": -0.3, "attack": -0.4, "attacks": -0.4,
    "attacked": -0.4, "shelling": -0.5, "bombardment": -0.6,
    "assassination": -0.7, "assassinated": -0.7, "assassinations": -0.7,

    # Casualties / suffering
    "casualties": -0.6, "wounded": -0.5, "injured": -0.5, "hurt": -0.4,
    "victim": -0.5, "victims": -0.5, "civilian": -0.3, "civilians": -0.3,
    "refugee": -0.4, "refugees": -0.4, "displaced": -0.4, "displacement": -0.4,
    "famine": -0.6, "starvation": -0.7, "starve": -0.6, "suffer": -0.5,
    "suffering": -0.5, "torture": -0.8, "torturing": -0.8,

    # Condemnation / hostility
    "condemn": -0.4, "condemns": -0.4, "condemned": -0.4, "denounce": -0.5,
    "slam": -0.4, "slams": -0.4, "slammed": -0.4, "blast": -0.3,
    "blasts": -0.3, "criticize": -0.3, "criticizes": -0.3, "accuse": -0.4,
    "accuses": -0.4, "accused": -0.4, "blame": -0.3, "blames": -0.3,
    "warn": -0.3, "warns": -0.3, "warning": -0.3, "threat": -0.4,
    "threatens": -0.4, "threaten": -0.4, "threatened": -0.4,

    # Conflict / crisis
    "war": -0.5, "conflict": -0.4, "crisis": -0.5, "escalation": -0.5,
    "escalate": -0.5, "tension": -0.3, "tensions": -0.3, "hostile": -0.4,
    "hostility": -0.4, "aggression": -0.6, "invasion": -0.6,
    "invade": -0.5, "siege": -0.5, "blockade": -0.5,
    "retaliation": -0.4, "retaliates": -0.4, "retaliate": -0.4,

    # Crime / illegality
    "crime": -0.5, "crimes": -0.5, "genocide": -0.8, "atrocity": -0.8,
    "atrocities": -0.8, "violation": -0.5, "violates": -0.5,
    "unlawful": -0.5, "illegal": -0.5, "banned": -0.3,

    # Fear / danger
    "fear": -0.4, "fears": -0.4, "danger": -0.4, "dangerous": -0.4,
    "scary": -0.3, "terrified": -0.5, "panic": -0.5, "chaos": -0.5,
    "collapse": -0.5, "disaster": -0.6, "catastrophe": -0.7,

    # Negative outcomes
    "fail": -0.4, "fails": -0.4, "failed": -0.4, "failure": -0.4,
    "reject": -0.3, "rejects": -0.3, "rejected": -0.3, "deny": -0.3,
    "denies": -0.3, "denied": -0.3, "ban": -0.3, "bans": -0.3,
    "sanctions": -0.4, "embargo": -0.5, "expel": -0.4,

    # Misleading / deception
    "misleading": -0.5, "lies": -0.5, "propaganda": -0.5, "disinformation": -0.5,
    "false": -0.3, "fabricated": -0.5,
    # Control / surveillance / oppression
    "dissent": -0.3, "control": -0.2, "surveillance": -0.3, "track": -0.2,
    "miscalculated": -0.4, "miscalculation": -0.4,
    "security zone": -0.3, "occupation": -0.5, "occupied": -0.4,
}

# Positive-framing words: suggest supportive, hopeful, de-escalation tone
POSITIVE_WORDS = {
    # Peace / diplomacy
    "peace": 0.5, "ceasefire": 0.4, "truce": 0.4, "talks": 0.15,
    "negotiate": 0.2, "negotiations": 0.2, "negotiating": 0.2,
    "diplomacy": 0.3, "diplomatic": 0.2, "dialogue": 0.2,
    "agreement": 0.4, "deal": 0.3, "treaty": 0.4, "summit": 0.15,
    "mediating": 0.3, "mediation": 0.3, "de-escalation": 0.5,
    "reconciliation": 0.5,

    # Aid / support
    "aid": 0.3, "humanitarian": 0.2, "rescue": 0.4, "relief": 0.3,
    "rebuild": 0.3, "rebuilding": 0.3, "recovery": 0.3, "restore": 0.3,
    "protect": 0.3, "protection": 0.3, "safe": 0.3, "safety": 0.3,

    # Progress
    "progress": 0.3, "hope": 0.4, "hopeful": 0.4, "optimism": 0.4,
    "optimistic": 0.4, "breakthrough": 0.5, "success": 0.4,
    "resolve": 0.3, "resolved": 0.3, "stabilize": 0.3, "stability": 0.3, "restored": 0.3,
    "cooperation": 0.3, "ally": 0.2, "allies": 0.2, "alliance": 0.2, "home": 0.2,

    # Legal / justice
    "justice": 0.3, "accountability": 0.3, "investigate": 0.2,
    "inquiry": 0.2,

    # Release / freedom / resolution
    "release": 0.3, "released": 0.3, "free": 0.3, "freed": 0.4,
    "liberate": 0.3, "open": 0.2, "opening": 0.2,
    "return": 0.2, "returns": 0.2, "lifted": 0.3, "ended": 0.2,
    "ends": 0.2, "signed": 0.3, "historic": 0.2,
    "liberty": 0.3, "help": 0.2, "contact": 0.15,
}

# Intensifiers that amplify the nearby sentiment word (EN + DE)
INTENSIFIERS = {
    "very": 1.3, "extremely": 1.5, "unprecedented": 1.4, "massive": 1.3,
    "major": 1.2, "severe": 1.3, "brutal": 1.4, "horrific": 1.5,
    "devastating": 1.4, "worst": 1.4, "deadliest": 1.5, "largest": 1.2,
    "extensive": 1.3, "intense": 1.3, "heavy": 1.2,
    # German
    "schwer": 1.3, "heftig": 1.3, "massiv": 1.4, "beispiellos": 1.4,
    "verheerend": 1.5, "schlimmste": 1.4, "größte": 1.2, "schwere": 1.3,
}

# Negators that flip sentiment direction (EN + DE)
NEGATORS = {
    "not", "no", "never", "neither", "nor", "without", "refuse", "refuses", "refused", "deny",
    "nicht", "kein", "keine", "keinen", "niemals", "ohne",
}

# Merge EN + DE lexicons into combined lookup
ALL_NEGATIVE = {**NEGATIVE_WORDS, **NEGATIVE_WORDS_DE}
ALL_POSITIVE = {**POSITIVE_WORDS, **POSITIVE_WORDS_DE}


def analyze_headline(title, summary=""):
    """Analyze sentiment of a headline using geopolitical lexicon.
    Returns polarity (-1 to +1) and subjectivity (0 to 1)."""
    text = title.lower()
    if summary:
        # Title matters more than summary — analyze both but weight title 2x
        text_full = f"{title.lower()} {title.lower()} {summary.lower()}"
    else:
        text_full = text

    # Match both ASCII and Unicode letters (German umlauts: ä, ö, ü, ß)
    words = [w.strip("'\"") for w in re.findall(r"[a-zäöüß'-]+", text_full)]
    scores = []
    subjectivity_signals = 0
    total_words = len(words)

    i = 0
    while i < len(words):
        word = words[i]

        # Check for negator in previous 2 words
        negated = False
        for j in range(max(0, i - 2), i):
            if words[j] in NEGATORS:
                negated = True
                break

        # Check for intensifier in previous word
        intensifier = 1.0
        if i > 0 and words[i - 1] in INTENSIFIERS:
            intensifier = INTENSIFIERS[words[i - 1]]

        score = 0
        if word in ALL_NEGATIVE:
            score = ALL_NEGATIVE[word] * intensifier
            subjectivity_signals += 1
        elif word in ALL_POSITIVE:
            score = ALL_POSITIVE[word] * intensifier
            subjectivity_signals += 1

        if negated and score != 0:
            score *= -0.5  # Negation partially flips

        if score != 0:
            scores.append(score)

        i += 1

    if not scores:
        polarity = 0.0
    else:
        polarity = sum(scores) / len(scores)
        # Clamp to [-1, 1]
        polarity = max(-1.0, min(1.0, polarity))

    # Subjectivity: ratio of sentiment-laden words to total
    subjectivity = min(1.0, subjectivity_signals / max(1, total_words) * 5)

    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
    }


# Editorial stance calibration per outlet per topic.
#
# Raw lexicon scores measure word-level negativity — but Israeli media reporting
# "IDF kills 10 in airstrike" uses the same negative words as Al Jazeera reporting
# the same event, even though the editorial framing differs fundamentally.
#
# These adjustments are based on documented editorial positions from:
# - Reuters Institute Digital News Report
# - Pew Research Center Global Attitudes surveys
# - Media Bias/Fact Check ratings
# - Government foreign policy alignment
#
# Positive adjustment = outlet is known to frame this topic more favorably
# Negative adjustment = outlet is known to frame this topic more critically
# The adjustment shifts the raw score, not replaces it.
#
EDITORIAL_STANCE = {
    "Israel": {
        # Israeli outlets: factual reporting on own conflict, not anti-Israel
        "Jerusalem Post": +0.20,
        "Times of Israel": +0.18,
        "Haaretz": +0.08,       # left-leaning Israeli, critical of government but pro-state
        "Israel Hayom": +0.22,
        # Pro-Israel foreign outlets
        "Hungary Today": +0.15,
        "Daily News Hungary": +0.15,
        "Fox News": +0.10,
        "NY Post": +0.10,
        # Neutral/mainstream
        "Reuters": 0.0,
        "AP": 0.0,
        "BBC": 0.0,
        "CNN": 0.0,
        "DW": 0.0,
        "France 24": 0.0,
        "NPR": 0.0,
        # Known critical editorial stance on Israel
        "Al Jazeera": -0.12,
        "Press TV": -0.18,
        "Middle East Eye": -0.10,
        "RT": -0.08,
        "TASS": -0.05,
        "Al Arabiya": -0.05,
        "The Guardian": -0.05,
        "The Independent": -0.05,
        "Irish Times": -0.08,
    },
    "US attack on Iran": {
        # Iranian state media: strongly critical of US strikes
        "Press TV": -0.15,
        "Iran Intl": -0.08,    # opposition but still critical of strikes on Iran
        # Pro-US-action outlets
        "Fox News": +0.10,
        "Jerusalem Post": +0.08,
        "Times of Israel": +0.08,
        "Hungary Today": +0.05,
        # Neutral
        "Reuters": 0.0,
        "AP": 0.0,
        "BBC": 0.0,
        # Critical of US military action
        "Al Jazeera": -0.10,
        "RT": -0.12,
        "TASS": -0.10,
        "The Guardian": -0.05,
    },
}


def analyze_batch(headlines, topic=None):
    """Score a list of headline dicts, returning them with polarity/subjectivity added.

    Applies editorial stance calibration: adjusts raw lexicon scores based on
    the outlet's documented editorial position on the topic being analyzed.
    """
    scored = []
    for h in headlines:
        sent = analyze_headline(h["title"], h.get("summary", ""))

        # Apply editorial stance calibration if available
        t = topic or h.get("topic", "")
        source = h.get("source", "")
        stance_adj = EDITORIAL_STANCE.get(t, {}).get(source, 0.0)
        calibrated_polarity = max(-1.0, min(1.0, sent["polarity"] + stance_adj))

        scored.append({
            **h,
            "polarity": round(calibrated_polarity, 3),
            "subjectivity": sent["subjectivity"],
            "raw_polarity": sent["polarity"],
        })
    return scored


def aggregate_by(scored_headlines, key):
    """Group scored headlines by a key and compute stats."""
    groups = defaultdict(list)
    for h in scored_headlines:
        groups[h[key]].append(h)

    result = {}
    for name, items in groups.items():
        polarities = [i["polarity"] for i in items]
        subjectivities = [i["subjectivity"] for i in items]
        result[name] = {
            "avg_polarity": round(sum(polarities) / len(polarities), 3),
            "avg_subjectivity": round(sum(subjectivities) / len(subjectivities), 3),
            "headline_count": len(items),
            "most_negative": min(items, key=lambda x: x["polarity"])["title"],
            "most_positive": max(items, key=lambda x: x["polarity"])["title"],
        }
    return result


def aggregate_by_outlet(scored_headlines):
    return aggregate_by(scored_headlines, "source")


def aggregate_by_country(scored_headlines):
    return aggregate_by(scored_headlines, "country")


def aggregate_by_region(scored_headlines):
    return aggregate_by(scored_headlines, "region")
