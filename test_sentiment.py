"""Known-answer test suite for sentiment analysis accuracy.

55 headlines with expected directions: negative, positive, or neutral.
Covers English, German, tricky edge cases, and real-world examples.
Run with: python test_sentiment.py
"""

from sentiment import analyze_headline

# (headline, expected_direction, category_key)
TESTS = [
    # === CLEARLY NEGATIVE — war, death, destruction ===
    ("Israel bombs Gaza hospital killing 50 civilians", "neg", "neg_en"),
    ("Iran launches 300 missiles at Israeli cities", "neg", "neg_en"),
    ("Russia invades Ukraine, thousands dead", "neg", "neg_en"),
    ("Massacre in refugee camp leaves hundreds dead", "neg", "neg_en"),
    ("US airstrikes destroy Iranian nuclear facility", "neg", "neg_en"),
    ("Suicide bomber kills 30 in Baghdad market", "neg", "neg_en"),
    ("Hezbollah rockets kill 12 in northern Israel", "neg", "neg_en"),
    ("Chemical weapons used against civilian population", "neg", "neg_en"),
    ("Genocide charges filed at International Criminal Court", "neg", "neg_en"),
    ("City under siege, humanitarian crisis worsens", "neg", "neg_en"),
    ("Assassination of military commander sparks retaliation fears", "neg", "neg_en"),
    ("Hundreds of civilians wounded in artillery barrage", "neg", "neg_en"),
    ("War crimes investigation launched after mass graves discovered", "neg", "neg_en"),
    ("Drone strike kills entire family including children", "neg", "neg_en"),
    ("Nuclear threat escalates as enrichment reaches 90%", "neg", "neg_en"),

    # === CLEARLY POSITIVE — peace, diplomacy, de-escalation ===
    ("Peace deal signed, ceasefire holds across region", "pos", "pos_en"),
    ("Hostages released as part of negotiated agreement", "pos", "pos_en"),
    ("Historic peace treaty ends decades of conflict", "pos", "pos_en"),
    ("Ceasefire agreement reached after marathon negotiations", "pos", "pos_en"),
    ("Diplomatic breakthrough as leaders meet for peace summit", "pos", "pos_en"),
    ("UN mediators achieve de-escalation, troops withdraw", "pos", "pos_en"),
    ("Refugees return home as stability restored", "pos", "pos_en"),
    ("Aid convoys reach besieged areas after blockade lifted", "pos", "pos_en"),
    ("Nations sign cooperation agreement on regional security", "pos", "pos_en"),
    ("Prisoner exchange brings hope for lasting peace", "pos", "pos_en"),

    # === NEUTRAL — factual, no strong framing ===
    ("UN Security Council meets to discuss Middle East situation", "neutral", "neutral_en"),
    ("Foreign minister arrives in Washington for scheduled talks", "neutral", "neutral_en"),
    ("Parliament debates new foreign policy resolution", "neutral", "neutral_en"),
    ("Oil prices steady as markets await developments", "neutral", "neutral_en"),
    ("Election results certified by electoral commission", "neutral", "neutral_en"),

    # === GERMAN NEGATIVE ===
    ("Raketen treffen Wohngebiet, dutzende Tote und Verletzte", "neg", "neg_de"),
    ("Schwere Angriffe auf zivile Infrastruktur in Gaza", "neg", "neg_de"),
    ("Krieg eskaliert weiter, Sanktionen verschärft", "neg", "neg_de"),
    ("Bombardierung fordert zahlreiche Opfer unter Zivilisten", "neg", "neg_de"),
    ("Flüchtlingskrise verschärft sich, Tausende Vertriebene", "neg", "neg_de"),

    # === GERMAN POSITIVE ===
    ("Waffenstillstand vereinbart, Hoffnung auf Frieden", "pos", "pos_de"),
    ("Verhandlungen bringen Durchbruch, Abkommen unterzeichnet", "pos", "pos_de"),
    ("Freilassung der Geiseln als Zeichen der Deeskalation", "pos", "pos_de"),

    # === GERMAN NEUTRAL ===
    ("Außenminister reist zu Gesprächen nach Washington", "neutral", "neutral_de"),

    # === TRICKY — positive words in negative context ===
    ("High-level assassinations form core of military strategy", "neg", "tricky"),
    ("Top general killed in precision drone strike", "neg", "tricky"),
    ("Unprecedented massive strikes devastate infrastructure", "neg", "tricky"),
    ("Productive talks fail to prevent escalation of bombing campaign", "neg", "tricky"),
    ("Iran confirms death of top security official in strikes", "neg", "tricky"),
    ("BBC accused of misleading coverage of civilian casualties", "neg", "tricky"),

    # === ADDITIONAL EDGE CASES ===
    ("Trump threatens to obliterate Iranian power plants", "neg", "extra"),
    ("Sanctions cripple economy as inflation soars", "neg", "extra"),
    ("Cyber attack disrupts critical infrastructure across country", "neg", "extra"),
    ("Emergency evacuation ordered as shelling intensifies", "neg", "extra"),
    ("Blockade cuts off food and medicine to 2 million people", "neg", "extra"),
    ("Both sides agree to extend humanitarian corridor", "pos", "extra"),
    ("International donors pledge reconstruction aid", "pos", "extra"),
    ("Trade agreement opens new economic cooperation", "pos", "extra"),
    ("Energy minister discusses pipeline at bilateral meeting", "neutral", "extra"),
    ("Census data shows population shift in border regions", "neutral", "extra"),
]

CATEGORIES = {
    "neg_en":     {"en": "Negative — War, Death, Destruction", "de": "Negativ — Krieg, Tod, Zerstörung"},
    "pos_en":     {"en": "Positive — Peace, Diplomacy, De-escalation", "de": "Positiv — Frieden, Diplomatie, Deeskalation"},
    "neutral_en": {"en": "Neutral — Factual Reporting", "de": "Neutral — Sachliche Berichterstattung"},
    "neg_de":     {"en": "Negative — German Language", "de": "Negativ — Deutsche Schlagzeilen"},
    "pos_de":     {"en": "Positive — German Language", "de": "Positiv — Deutsche Schlagzeilen"},
    "neutral_de": {"en": "Neutral — German Language", "de": "Neutral — Deutsche Schlagzeilen"},
    "tricky":     {"en": "Edge Cases — Tricky Headlines", "de": "Schwierige Fälle — Irreführende Formulierungen"},
    "extra":      {"en": "Additional Scenarios", "de": "Weitere Szenarien"},
}


def run_tests():
    passed = 0
    failed = 0
    failures = []

    for headline, expected, _cat in TESTS:
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
