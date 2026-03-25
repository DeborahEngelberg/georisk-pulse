"""Known-answer test suite for sentiment analysis accuracy.

55 headlines with expected directions: negative, positive, or neutral.
Covers English, German, tricky edge cases, and real-world examples.
Run with: python test_sentiment.py
"""

from sentiment import analyze_headline

TESTS = [
    # === CLEARLY NEGATIVE — war, death, destruction (15) ===
    ("Israel bombs Gaza hospital killing 50 civilians", "neg"),
    ("Iran launches 300 missiles at Israeli cities", "neg"),
    ("Russia invades Ukraine, thousands dead", "neg"),
    ("Massacre in refugee camp leaves hundreds dead", "neg"),
    ("US airstrikes destroy Iranian nuclear facility", "neg"),
    ("Suicide bomber kills 30 in Baghdad market", "neg"),
    ("Hezbollah rockets kill 12 in northern Israel", "neg"),
    ("Chemical weapons used against civilian population", "neg"),
    ("Genocide charges filed at International Criminal Court", "neg"),
    ("City under siege, humanitarian crisis worsens", "neg"),
    ("Assassination of military commander sparks retaliation fears", "neg"),
    ("Hundreds of civilians wounded in artillery barrage", "neg"),
    ("War crimes investigation launched after mass graves discovered", "neg"),
    ("Drone strike kills entire family including children", "neg"),
    ("Nuclear threat escalates as enrichment reaches 90%", "neg"),

    # === CLEARLY POSITIVE — peace, diplomacy, de-escalation (10) ===
    ("Peace deal signed, ceasefire holds across region", "pos"),
    ("Hostages released as part of negotiated agreement", "pos"),
    ("Historic peace treaty ends decades of conflict", "pos"),
    ("Ceasefire agreement reached after marathon negotiations", "pos"),
    ("Diplomatic breakthrough as leaders meet for peace summit", "pos"),
    ("UN mediators achieve de-escalation, troops withdraw", "pos"),
    ("Refugees return home as stability restored", "pos"),
    ("Aid convoys reach besieged areas after blockade lifted", "pos"),
    ("Nations sign cooperation agreement on regional security", "pos"),
    ("Prisoner exchange brings hope for lasting peace", "pos"),

    # === NEUTRAL — factual, no strong framing (5) ===
    ("UN Security Council meets to discuss Middle East situation", "neutral"),
    ("Foreign minister arrives in Washington for scheduled talks", "neutral"),
    ("Parliament debates new foreign policy resolution", "neutral"),
    ("Oil prices steady as markets await developments", "neutral"),
    ("Election results certified by electoral commission", "neutral"),

    # === GERMAN NEGATIVE (5) ===
    ("Raketen treffen Wohngebiet, dutzende Tote und Verletzte", "neg"),
    ("Schwere Angriffe auf zivile Infrastruktur in Gaza", "neg"),
    ("Krieg eskaliert weiter, Sanktionen verschärft", "neg"),
    ("Bombardierung fordert zahlreiche Opfer unter Zivilisten", "neg"),
    ("Flüchtlingskrise verschärft sich, Tausende Vertriebene", "neg"),

    # === GERMAN POSITIVE (3) ===
    ("Waffenstillstand vereinbart, Hoffnung auf Frieden", "pos"),
    ("Verhandlungen bringen Durchbruch, Abkommen unterzeichnet", "pos"),
    ("Freilassung der Geiseln als Zeichen der Deeskalation", "pos"),

    # === GERMAN NEUTRAL (1) ===
    ("Außenminister reist zu Gesprächen nach Washington", "neutral"),

    # === TRICKY — positive words in negative context (6) ===
    ("High-level assassinations form core of military strategy", "neg"),
    ("Top general killed in precision drone strike", "neg"),
    ("Unprecedented massive strikes devastate infrastructure", "neg"),
    ("Productive talks fail to prevent escalation of bombing campaign", "neg"),
    ("Iran confirms death of top security official in strikes", "neg"),
    ("BBC accused of misleading coverage of civilian casualties", "neg"),

    # === ADDITIONAL EDGE CASES (10) ===
    ("Trump threatens to obliterate Iranian power plants", "neg"),
    ("Sanctions cripple economy as inflation soars", "neg"),
    ("Cyber attack disrupts critical infrastructure across country", "neg"),
    ("Emergency evacuation ordered as shelling intensifies", "neg"),
    ("Blockade cuts off food and medicine to 2 million people", "neg"),
    ("Both sides agree to extend humanitarian corridor", "pos"),
    ("International donors pledge reconstruction aid", "pos"),
    ("Trade agreement opens new economic cooperation", "pos"),
    ("Energy minister discusses pipeline at bilateral meeting", "neutral"),
    ("Census data shows population shift in border regions", "neutral"),
]


def run_tests():
    passed = 0
    failed = 0
    failures = []

    for headline, expected in TESTS:
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
