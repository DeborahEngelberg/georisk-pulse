import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Weighted risk keywords: word -> weight (higher = riskier)
RISK_KEYWORDS = {
    # Active warfare / kinetic
    "war": 10, "attack": 9, "attacks": 9, "missile": 10, "missiles": 10,
    "bomb": 9, "bombing": 9, "strike": 9, "strikes": 9, "struck": 9,
    "invasion": 10, "troops": 8, "military": 7, "combat": 9, "airstrike": 10,
    "airstrikes": 10, "drone": 7, "drones": 7, "casualties": 9, "killed": 9,
    "deaths": 8, "dead": 8, "shelling": 9, "artillery": 8, "offensive": 8,
    "ceasefire": 5, "weapons": 7, "rocket": 10, "rockets": 10, "fired": 8,
    "firing": 8, "intercept": 8, "retaliation": 9, "retaliates": 9,
    "retaliated": 9, "explosion": 8, "destroyed": 8, "siege": 8,
    "bombardment": 9, "warplane": 9, "fighter jet": 8,
    # Nuclear / WMD
    "nuclear": 10, "uranium": 9, "enrichment": 9, "warhead": 10,
    "proliferation": 8, "icbm": 10, "ballistic": 9,
    # Casualties / destruction
    "massacre": 10, "slaughter": 10, "civilian": 7, "civilians": 7,
    "wounded": 8, "injured": 7, "death toll": 9, "body count": 9,
    "destruction": 8, "devastation": 8, "rubble": 7, "crater": 7,
    "war crime": 10, "genocide": 10, "atrocity": 10,
    # Political instability
    "sanctions": 6, "coup": 9, "protest": 5, "unrest": 6, "crisis": 7,
    "tension": 5, "escalation": 9, "escalate": 9, "conflict": 8, "threat": 7,
    "assassination": 10, "detained": 5, "arrested": 4,
    # Military mobilization
    "deployment": 7, "deployed": 7, "mobilization": 8, "reinforcements": 7,
    "naval": 6, "carrier": 7, "fleet": 6, "battalion": 7, "ground operation": 9,
    # Economic risk
    "embargo": 7, "blockade": 8, "collapse": 7, "default": 6,
    # Diplomacy (lower risk - can reduce tension)
    "talks": 2, "negotiations": 3, "peace": 2, "agreement": 2, "treaty": 2,
    "diplomacy": 2, "summit": 3, "de-escalation": 2,
    # Humanitarian
    "refugees": 6, "humanitarian": 6, "famine": 7, "displacement": 6,
    "evacuate": 6, "evacuation": 6, "aid blocked": 8,
    # Cyber
    "cyber": 6, "hack": 6, "cyberattack": 8,
}

# Named entities that amplify risk (country leaders, military orgs)
ENTITY_AMPLIFIERS = {
    "NORP": 1.1,  # Nationalities, religious/political groups
    "GPE": 1.0,   # Countries, cities (neutral)
    "ORG": 1.05,  # Organizations
    "PERSON": 1.0,
}


def score_headline(title):
    """Score a single headline 0-100 based on risk keywords and NER."""
    doc = nlp(title.lower())
    raw_score = 0
    matched_keywords = 0

    # Keyword scoring
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in RISK_KEYWORDS:
            raw_score += RISK_KEYWORDS[lemma]
            matched_keywords += 1
        elif token.text.lower() in RISK_KEYWORDS:
            raw_score += RISK_KEYWORDS[token.text.lower()]
            matched_keywords += 1

    # Check bigrams for multi-word matches
    text_lower = title.lower()
    for keyword, weight in RISK_KEYWORDS.items():
        if " " in keyword and keyword in text_lower:
            raw_score += weight
            matched_keywords += 1

    # Entity-based amplification
    amplifier = 1.0
    for ent in doc.ents:
        amp = ENTITY_AMPLIFIERS.get(ent.label_, 1.0)
        if amp > amplifier:
            amplifier = amp

    raw_score *= amplifier

    # Normalize to 0-100 (cap at ~3 strong keywords hitting max)
    normalized = min(100, (raw_score / 30) * 100)
    return round(normalized, 1)


def compute_daily_score(headlines):
    """Compute aggregate daily risk score for a list of headlines.

    Uses a top-heavy weighted approach: the highest-scoring headlines
    matter most, because one "missiles hit nuclear site" headline
    shouldn't be diluted by twenty routine ones.

    Components:
    - Top-weighted average (top 30% of headlines weighted 3x)
    - Severity floor: if ANY headline scores 80+, daily score can't drop below 60
    - Volume signal: many headlines = sustained crisis, not noise
    """
    if not headlines:
        return 0.0, []

    scored = []
    for h in headlines:
        s = score_headline(h["title"])
        scored.append({**h, "score": s})

    scores = sorted([h["score"] for h in scored], reverse=True)
    n = len(scores)

    # Top-weighted average: top 30% count 3x, next 30% count 2x, rest count 1x
    top_cutoff = max(1, int(n * 0.3))
    mid_cutoff = max(top_cutoff, int(n * 0.6))

    weighted_sum = 0
    weight_total = 0
    for i, s in enumerate(scores):
        if i < top_cutoff:
            w = 3
        elif i < mid_cutoff:
            w = 2
        else:
            w = 1
        weighted_sum += s * w
        weight_total += w

    weighted_avg = weighted_sum / weight_total if weight_total else 0

    # Volume bonus: sustained coverage = real crisis (up to +15)
    volume_bonus = min(15, n * 1.5)

    # Severity floor: if top headlines are extreme, the day is high-risk
    peak = scores[0] if scores else 0
    severity_floor = 0
    if peak >= 90:
        severity_floor = 70
    elif peak >= 80:
        severity_floor = 60
    elif peak >= 60:
        severity_floor = 40

    raw = weighted_avg + volume_bonus
    final = min(100, max(raw, severity_floor))
    return round(final, 1), scored
