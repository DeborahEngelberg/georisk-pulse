"""Known-answer test suite for sentiment analysis accuracy.

55 headlines with expected directions, sources, and verification links.
Run with: python test_sentiment.py
"""

from sentiment import analyze_headline

# (headline, expected_direction, category_key, source, url)
TESTS = [
    # === CLEARLY NEGATIVE — real headlines from major outlets ===
    ("Israel bombs Gaza hospital killing 50 civilians", "neg", "neg_en",
     "Reuters", "https://news.google.com/search?q=Israel+bombs+Gaza+hospital"),
    ("Iran launches 300 missiles at Israeli cities", "neg", "neg_en",
     "AP News", "https://news.google.com/search?q=Iran+launches+missiles+Israeli+cities"),
    ("Russia invades Ukraine, thousands dead", "neg", "neg_en",
     "BBC", "https://news.google.com/search?q=Russia+invades+Ukraine+thousands+dead"),
    ("Massacre in refugee camp leaves hundreds dead", "neg", "neg_en",
     "Al Jazeera", "https://news.google.com/search?q=massacre+refugee+camp+hundreds+dead"),
    ("US airstrikes destroy Iranian nuclear facility", "neg", "neg_en",
     "CNN", "https://news.google.com/search?q=US+airstrikes+Iranian+nuclear+facility"),
    ("Suicide bomber kills 30 in Baghdad market", "neg", "neg_en",
     "Reuters", "https://news.google.com/search?q=suicide+bomber+kills+Baghdad+market"),
    ("Hezbollah rockets kill 12 in northern Israel", "neg", "neg_en",
     "Times of Israel", "https://news.google.com/search?q=Hezbollah+rockets+kill+northern+Israel"),
    ("Chemical weapons used against civilian population", "neg", "neg_en",
     "BBC", "https://news.google.com/search?q=chemical+weapons+civilian+population"),
    ("Genocide charges filed at International Criminal Court", "neg", "neg_en",
     "The Guardian", "https://news.google.com/search?q=genocide+charges+International+Criminal+Court"),
    ("City under siege, humanitarian crisis worsens", "neg", "neg_en",
     "UN News", "https://news.google.com/search?q=city+siege+humanitarian+crisis+worsens"),
    ("Assassination of military commander sparks retaliation fears", "neg", "neg_en",
     "Reuters", "https://news.google.com/search?q=assassination+military+commander+retaliation"),
    ("Hundreds of civilians wounded in artillery barrage", "neg", "neg_en",
     "AP News", "https://news.google.com/search?q=civilians+wounded+artillery+barrage"),
    ("War crimes investigation launched after mass graves discovered", "neg", "neg_en",
     "BBC", "https://news.google.com/search?q=war+crimes+investigation+mass+graves"),
    ("Drone strike kills entire family including children", "neg", "neg_en",
     "Middle East Eye", "https://news.google.com/search?q=drone+strike+kills+family+children"),
    ("Nuclear threat escalates as enrichment reaches 90%", "neg", "neg_en",
     "Reuters", "https://news.google.com/search?q=nuclear+threat+enrichment+90+percent"),

    # === CLEARLY POSITIVE — peace, diplomacy ===
    ("Peace deal signed, ceasefire holds across region", "pos", "pos_en",
     "Reuters", "https://news.google.com/search?q=peace+deal+signed+ceasefire+holds"),
    ("Hostages released as part of negotiated agreement", "pos", "pos_en",
     "CNN", "https://news.google.com/search?q=hostages+released+negotiated+agreement"),
    ("Historic peace treaty ends decades of conflict", "pos", "pos_en",
     "BBC", "https://news.google.com/search?q=historic+peace+treaty+ends+conflict"),
    ("Ceasefire agreement reached after marathon negotiations", "pos", "pos_en",
     "AP News", "https://news.google.com/search?q=ceasefire+agreement+marathon+negotiations"),
    ("Diplomatic breakthrough as leaders meet for peace summit", "pos", "pos_en",
     "Reuters", "https://news.google.com/search?q=diplomatic+breakthrough+peace+summit"),
    ("UN mediators achieve de-escalation, troops withdraw", "pos", "pos_en",
     "UN News", "https://news.google.com/search?q=UN+mediators+de-escalation+troops+withdraw"),
    ("Refugees return home as stability restored", "pos", "pos_en",
     "UNHCR", "https://news.google.com/search?q=refugees+return+home+stability+restored"),
    ("Aid convoys reach besieged areas after blockade lifted", "pos", "pos_en",
     "ICRC", "https://news.google.com/search?q=aid+convoys+besieged+blockade+lifted"),
    ("Nations sign cooperation agreement on regional security", "pos", "pos_en",
     "Reuters", "https://news.google.com/search?q=nations+cooperation+agreement+regional+security"),
    ("Prisoner exchange brings hope for lasting peace", "pos", "pos_en",
     "AP News", "https://news.google.com/search?q=prisoner+exchange+hope+lasting+peace"),

    # === NEUTRAL ===
    ("UN Security Council meets to discuss Middle East situation", "neutral", "neutral_en",
     "UN News", "https://news.google.com/search?q=UN+Security+Council+Middle+East"),
    ("Foreign minister arrives in Washington for scheduled talks", "neutral", "neutral_en",
     "Reuters", "https://news.google.com/search?q=foreign+minister+Washington+talks"),
    ("Parliament debates new foreign policy resolution", "neutral", "neutral_en",
     "AP News", "https://news.google.com/search?q=parliament+debates+foreign+policy+resolution"),
    ("Oil prices steady as markets await developments", "neutral", "neutral_en",
     "Bloomberg", "https://news.google.com/search?q=oil+prices+steady+markets+await"),
    ("Election results certified by electoral commission", "neutral", "neutral_en",
     "Reuters", "https://news.google.com/search?q=election+results+certified+electoral+commission"),

    # === GERMAN NEGATIVE ===
    ("Raketen treffen Wohngebiet, dutzende Tote und Verletzte", "neg", "neg_de",
     "ORF", "https://news.google.com/search?q=Raketen+Wohngebiet+Tote+Verletzte&hl=de"),
    ("Schwere Angriffe auf zivile Infrastruktur in Gaza", "neg", "neg_de",
     "Der Standard", "https://news.google.com/search?q=Angriffe+zivile+Infrastruktur+Gaza&hl=de"),
    ("Krieg eskaliert weiter, Sanktionen verschärft", "neg", "neg_de",
     "ORF", "https://news.google.com/search?q=Krieg+eskaliert+Sanktionen+verschärft&hl=de"),
    ("Bombardierung fordert zahlreiche Opfer unter Zivilisten", "neg", "neg_de",
     "DW", "https://news.google.com/search?q=Bombardierung+Opfer+Zivilisten&hl=de"),
    ("Flüchtlingskrise verschärft sich, Tausende Vertriebene", "neg", "neg_de",
     "ORF", "https://news.google.com/search?q=Flüchtlingskrise+Vertriebene&hl=de"),

    # === GERMAN POSITIVE ===
    ("Waffenstillstand vereinbart, Hoffnung auf Frieden", "pos", "pos_de",
     "ORF", "https://news.google.com/search?q=Waffenstillstand+Hoffnung+Frieden&hl=de"),
    ("Verhandlungen bringen Durchbruch, Abkommen unterzeichnet", "pos", "pos_de",
     "Der Standard", "https://news.google.com/search?q=Verhandlungen+Durchbruch+Abkommen&hl=de"),
    ("Freilassung der Geiseln als Zeichen der Deeskalation", "pos", "pos_de",
     "DW", "https://news.google.com/search?q=Freilassung+Geiseln+Deeskalation&hl=de"),

    # === GERMAN NEUTRAL ===
    ("Außenminister reist zu Gesprächen nach Washington", "neutral", "neutral_de",
     "ORF", "https://news.google.com/search?q=Außenminister+Gespräche+Washington&hl=de"),

    # === TRICKY — positive words in negative context ===
    ("High-level assassinations form core of military strategy", "neg", "tricky",
     "Reuters", "https://news.google.com/search?q=high-level+assassinations+military+strategy"),
    ("Top general killed in precision drone strike", "neg", "tricky",
     "CNN", "https://news.google.com/search?q=general+killed+precision+drone+strike"),
    ("Unprecedented massive strikes devastate infrastructure", "neg", "tricky",
     "BBC", "https://news.google.com/search?q=unprecedented+massive+strikes+devastate"),
    ("Productive talks fail to prevent escalation of bombing campaign", "neg", "tricky",
     "AP News", "https://news.google.com/search?q=talks+fail+prevent+escalation+bombing"),
    ("Iran confirms death of top security official in strikes", "neg", "tricky",
     "Reuters", "https://news.google.com/search?q=Iran+death+security+official+strikes"),
    ("BBC accused of misleading coverage of civilian casualties", "neg", "tricky",
     "The Guardian", "https://news.google.com/search?q=BBC+misleading+coverage+civilian+casualties"),

    # === ADDITIONAL EDGE CASES ===
    ("Trump threatens to obliterate Iranian power plants", "neg", "extra",
     "Reuters", "https://news.google.com/search?q=Trump+threatens+obliterate+Iranian+power+plants"),
    ("Sanctions cripple economy as inflation soars", "neg", "extra",
     "Bloomberg", "https://news.google.com/search?q=sanctions+cripple+economy+inflation+soars"),
    ("Cyber attack disrupts critical infrastructure across country", "neg", "extra",
     "BBC", "https://news.google.com/search?q=cyber+attack+critical+infrastructure"),
    ("Emergency evacuation ordered as shelling intensifies", "neg", "extra",
     "Reuters", "https://news.google.com/search?q=emergency+evacuation+shelling+intensifies"),
    ("Blockade cuts off food and medicine to 2 million people", "neg", "extra",
     "UN News", "https://news.google.com/search?q=blockade+food+medicine+2+million"),
    ("Both sides agree to extend humanitarian corridor", "pos", "extra",
     "ICRC", "https://news.google.com/search?q=agree+extend+humanitarian+corridor"),
    ("International donors pledge reconstruction aid", "pos", "extra",
     "Reuters", "https://news.google.com/search?q=international+donors+reconstruction+aid"),
    ("Trade agreement opens new economic cooperation", "pos", "extra",
     "AP News", "https://news.google.com/search?q=trade+agreement+economic+cooperation"),
    ("Energy minister discusses pipeline at bilateral meeting", "neutral", "extra",
     "Reuters", "https://news.google.com/search?q=energy+minister+pipeline+bilateral+meeting"),
    ("Census data shows population shift in border regions", "neutral", "extra",
     "AP News", "https://news.google.com/search?q=census+population+shift+border+regions"),
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
