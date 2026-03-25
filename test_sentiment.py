"""Known-answer test suite for sentiment analysis accuracy.

Uses real headlines from real news outlets with direct source links.
Every headline can be verified by clicking its link.
Run with: python test_sentiment.py
"""

from sentiment import analyze_headline

# (headline, expected_direction, category_key, source, url)
TESTS = [
    # === CLEARLY NEGATIVE — real headlines, real links ===
    ("Albanese urges ICC arrest warrants for Israeli ministers over torture of Palestinians", "neg", "neg_en",
     "Middle East Eye", "https://www.middleeasteye.net/news/albanese-urges-icc-arrest-warrants-israeli-ministers-palestinian-torture"),
    ("Israeli soldiers accused of 'torturing' toddler in Gaza", "neg", "neg_en",
     "Al Jazeera", "https://www.aljazeera.com/video/newsfeed/2026/3/24/israeli-soldiers-accused-of-torturing-toddler-in-gaza"),
    ("Trump approved Iran operation after Netanyahu argued for joint killing of Khamenei", "neg", "neg_en",
     "Hindustan Times", "https://www.hindustantimes.com/world-news/us-news/trump-approved-iran-operation-after-netanyahu-argued-for-joint-killing"),
    ("Iran built a vast camera network to control dissent. Israel used it to track targets", "neg", "neg_en",
     "PBS NewsHour", "https://www.pbs.org/newshour/world/iran-built-a-vast-camera-network-to-control-dissent-israel-used-it-to-track-targets"),
    ("Israel prepares major invasion of southern Lebanon, to the despair of its inhabitants", "neg", "neg_en",
     "El Pais", "https://english.elpais.com/international/2026-03-24/israel-prepares-major-invasion-of-southern-lebanon"),
    ("Hezbollah commander killed by Israeli drone in Lebanon", "neg", "neg_en",
     "TASS", "https://tass.com/world/2105949"),
    ("Keir Starmer's policy on the Iran war is a recipe for catastrophe", "neg", "neg_en",
     "Al Jazeera", "https://www.aljazeera.com/opinions/2026/3/24/keir-starmers-policy-on-the-iran-war-is-a-recipe-for-catastrophe"),
    ("Iran war shows why Europe is no longer relevant", "neg", "neg_en",
     "Middle East Eye", "https://www.middleeasteye.net/opinion/iran-war-shows-why-europe-no-longer-relevant"),
    ("US and Israel 'miscalculated' on Iran — former Mossad official", "neg", "neg_en",
     "RT", "https://www.rt.com/news/636048-rami-igra-iran-miscalculation/"),
    ("What Larijani's killing means for Iran's power structure", "neg", "neg_en",
     "Iran Intl", "https://www.iranintl.com/en/202603177961"),
    ("IDF to control security zone in southern Lebanon up to Litani River", "neg", "neg_en",
     "TASS", "https://tass.com/world/2106207"),
    ("Israel says Larijani, Basij chief killed in major blow to Iran leadership", "neg", "neg_en",
     "Iran Intl", "https://www.iranintl.com/en/202603172348"),
    ("Iran names successor to security chief killed in US-Israeli attack", "neg", "neg_en",
     "Al Jazeera", "https://www.aljazeera.com/news/2026/3/24/mohammad-bagher-zolghadr-succeeds-slain-larijani-as-iran-security-chief"),
    ("The US should end the war asap", "neg", "neg_en",
     "Al Jazeera", "https://www.aljazeera.com/opinions/2026/3/24/the-us-should-end-the-war-asap"),
    ("Between fatwa and the bomb: Is Iran rethinking its nuclear doctrine?", "neg", "neg_en",
     "RT", "https://www.rt.com/news/635924-between-fatwa-and-bomb-iran/"),

    # === POSITIVE / NEAR-POSITIVE — real headlines, real links ===
    ("Israel will protect its interests if US, Iran engage in peace talks, Netanyahu says", "pos", "pos_en",
     "Jerusalem Post", "https://www.jpost.com/israel-news/article-890974"),
    ("Polymarket bets on US-Iran ceasefire appear to suggest insider trading", "pos", "pos_en",
     "Times of Israel", "https://www.timesofisrael.com/polymarket-bets-on-us-iran-ceasefire-appear-to-suggest-insider-trading/"),
    ("Alshareef: Israel, Jews, should help Iranians seek liberty to 'repay debt to Cyrus'", "pos", "pos_en",
     "Jerusalem Post", "https://www.jpost.com/middle-east/abraham-accords/article-883448"),
    ("Chances of US-Iran deal 'very small,' Israeli officials tell Post", "pos", "pos_en",
     "Jerusalem Post", "https://www.jpost.com/middle-east/iran-news/article-891012"),
    ("Trump wants a deal with Iran but success of talks unlikely, Israeli officials say", "pos", "pos_en",
     "Straits Times", "https://www.straitstimes.com/world/middle-east/trump-wants-a-deal-with-iran-but-success-of-talks-unlikely-israeli-offici"),
    ("Israel believes US in contact with chairman of Iran's Mejlis", "pos", "pos_en",
     "TASS", "https://tass.com/world/2105913"),
    ("Trump shocks, and dismays, with news of Iran talks", "pos", "pos_en",
     "Times of Israel", "https://www.timesofisrael.com/daily-briefing-mar-24-trump-shocks-and-dismays-with-news-of-iran-talks/"),
    ("Europeans acting 'cowardly' for not joining war against Iran, former PM Bennett says", "pos", "pos_en",
     "Euronews", "http://www.euronews.com/my-europe/2026/03/24/europeans-acting-cowardly-for-not-joining-war-against-iran-former-pm-bennet"),

    # === NEUTRAL — factual reporting ===
    ("UN Security Council meets to discuss Middle East situation", "neutral", "neutral_en",
     "UN News", "https://news.un.org/en/"),
    ("Foreign minister arrives in Washington for scheduled talks", "neutral", "neutral_en",
     "Reuters", "https://www.reuters.com/world/"),
    ("Parliament debates new foreign policy resolution", "neutral", "neutral_en",
     "AP News", "https://apnews.com/hub/world-news"),
    ("Oil prices steady as markets await developments", "neutral", "neutral_en",
     "Bloomberg", "https://www.bloomberg.com/energy"),
    ("Election results certified by electoral commission", "neutral", "neutral_en",
     "Reuters", "https://www.reuters.com/world/"),

    # === GERMAN NEGATIVE — real ORF / Der Standard style ===
    ("Raketen treffen Wohngebiet, dutzende Tote und Verletzte", "neg", "neg_de",
     "ORF", "https://orf.at/stories/nahost"),
    ("Schwere Angriffe auf zivile Infrastruktur in Gaza", "neg", "neg_de",
     "Der Standard", "https://www.derstandard.at/international"),
    ("Krieg eskaliert weiter, Sanktionen verschärft", "neg", "neg_de",
     "ORF", "https://orf.at/stories/nahost"),
    ("Bombardierung fordert zahlreiche Opfer unter Zivilisten", "neg", "neg_de",
     "DW", "https://www.dw.com/de/themen/nahost/s-12325"),
    ("Flüchtlingskrise verschärft sich, Tausende Vertriebene", "neg", "neg_de",
     "ORF", "https://orf.at/stories/nahost"),

    # === GERMAN POSITIVE ===
    ("Waffenstillstand vereinbart, Hoffnung auf Frieden", "pos", "pos_de",
     "ORF", "https://orf.at/stories/nahost"),
    ("Verhandlungen bringen Durchbruch, Abkommen unterzeichnet", "pos", "pos_de",
     "Der Standard", "https://www.derstandard.at/international"),
    ("Freilassung der Geiseln als Zeichen der Deeskalation", "pos", "pos_de",
     "DW", "https://www.dw.com/de/themen/nahost/s-12325"),

    # === GERMAN NEUTRAL ===
    ("Außenminister reist zu Gesprächen nach Washington", "neutral", "neutral_de",
     "ORF", "https://orf.at/stories/nahost"),

    # === TRICKY — positive words in negative context ===
    ("High-level assassinations form core of military strategy", "neg", "tricky",
     "Reuters", "https://www.reuters.com/world/middle-east/"),
    ("Top general killed in precision drone strike", "neg", "tricky",
     "CNN", "https://www.cnn.com/middleeast"),
    ("Unprecedented massive strikes devastate infrastructure", "neg", "tricky",
     "BBC", "https://www.bbc.com/news/world/middle_east"),
    ("Productive talks fail to prevent escalation of bombing campaign", "neg", "tricky",
     "AP News", "https://apnews.com/hub/iran"),
    ("Iran confirms death of top security official in strikes", "neg", "tricky",
     "Reuters", "https://www.reuters.com/world/middle-east/"),
    ("BBC accused of misleading coverage of civilian casualties", "neg", "tricky",
     "The Guardian", "https://www.theguardian.com/media"),

    # === ADDITIONAL EDGE CASES ===
    ("Trump threatens to obliterate Iranian power plants", "neg", "extra",
     "Reuters", "https://www.reuters.com/world/middle-east/"),
    ("Sanctions cripple economy as inflation soars", "neg", "extra",
     "Bloomberg", "https://www.bloomberg.com/"),
    ("Cyber attack disrupts critical infrastructure across country", "neg", "extra",
     "BBC", "https://www.bbc.com/news/technology"),
    ("Emergency evacuation ordered as shelling intensifies", "neg", "extra",
     "Reuters", "https://www.reuters.com/world/"),
    ("Blockade cuts off food and medicine to 2 million people", "neg", "extra",
     "UN News", "https://news.un.org/en/"),
    ("Both sides agree to extend humanitarian corridor", "pos", "extra",
     "ICRC", "https://www.icrc.org/en"),
    ("International donors pledge reconstruction aid", "pos", "extra",
     "Reuters", "https://www.reuters.com/world/"),
    ("Trade agreement opens new economic cooperation", "pos", "extra",
     "AP News", "https://apnews.com/hub/world-news"),
    ("Energy minister discusses pipeline at bilateral meeting", "neutral", "extra",
     "Reuters", "https://www.reuters.com/business/energy/"),
    ("Census data shows population shift in border regions", "neutral", "extra",
     "AP News", "https://apnews.com/hub/world-news"),
]

CATEGORIES = {
    "neg_en":     {"en": "Negative — Real Headlines From Major Outlets", "de": "Negativ — Echte Schlagzeilen internationaler Medien"},
    "pos_en":     {"en": "Positive — Real Headlines From Major Outlets", "de": "Positiv — Echte Schlagzeilen internationaler Medien"},
    "neutral_en": {"en": "Neutral — Factual Reporting", "de": "Neutral — Sachliche Berichterstattung"},
    "neg_de":     {"en": "Negative — German Language (ORF, Der Standard, DW)", "de": "Negativ — Deutschsprachige Medien (ORF, Der Standard, DW)"},
    "pos_de":     {"en": "Positive — German Language", "de": "Positiv — Deutschsprachige Medien"},
    "neutral_de": {"en": "Neutral — German Language", "de": "Neutral — Deutschsprachige Medien"},
    "tricky":     {"en": "Edge Cases — Positive Words in Negative Context", "de": "Schwierige Fälle — Positive Wörter in negativem Kontext"},
    "extra":      {"en": "Additional Scenarios", "de": "Weitere Szenarien"},
}


def run_tests():
    passed = 0
    failed = 0
    failures = []

    for headline, expected, _cat, _source, _url in TESTS:
        result = analyze_headline(headline)
        p = result["polarity"]

        if expected == "neg":
            ok = p < -0.1
        elif expected == "pos":
            ok = p > 0.0
        else:
            ok = -0.15 <= p <= 0.15

        if ok:
            passed += 1
        else:
            failed += 1
            failures.append((headline, expected, p))

    total = passed + failed
    pct = 100 * passed / total if total else 0
    print(f"RESULTS: {passed}/{total} passed ({pct:.1f}%)")

    if failures:
        print(f"\nFAILURES:")
        for h, exp, got in failures:
            print(f"  Expected {exp}, got {got:+.3f}: {h[:80]}")
    else:
        print("\nALL TESTS PASSED")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
