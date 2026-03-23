"""Static reference data for economic exposure and historical benchmarks."""

# Region name translations
REGION_NAMES_DE = {
    "Iran": "Iran",
    "Russia": "Russland",
    "Israel": "Israel",
    "Taiwan": "Taiwan",
}

# Austrian/EU-specific exposure to each region's risk
EU_AUSTRIA_EXPOSURE = {
    "Iran": {
        "EU Trade Exposure": "€3.2B EU-Iran trade (2023), Austria ~€180M",
        "Energy Impact": "Austria 80% gas-import dependent; Iran escalation → Brent +$10 → Austrian CPI +0.3%",
        "Refugee Pressure": "UNHCR est. 500K-2M displaced in full conflict; Austria on Balkan route",
        "Austrian Firms at Risk": "OMV (energy), Andritz (industrial), Voestalpine (steel inputs)",
        "EU Sanctions Burden": "Austrian banks face secondary sanctions compliance costs",
        "NATO/Neutrality": "Austria's neutrality under pressure; transit rights, airspace questions",
    },
    "Russia": {
        "EU Trade Exposure": "EU-Russia trade collapsed 60% since 2022; Austria lost €4B in exports",
        "Energy Impact": "Austria was 80% Russian gas dependent (2021); now ~50% via diversification",
        "OMV Exposure": "OMV wrote down €2.1B on Russian assets; Gazprom contracts disputed",
        "Raiffeisen Bank": "RBI €22B Russia exposure — largest Western bank in Russia",
        "Austrian GDP Impact": "OeNB estimates -0.5% GDP from Russia sanctions since 2022",
        "Refugee Flow": "380K Ukrainian refugees in Austria; integration costs €1.2B/yr",
    },
    "Israel": {
        "EU Trade Exposure": "€47B EU-Israel trade; Austria ~€1.1B bilateral",
        "Tech Dependency": "Austrian firms source cybersecurity, agritech, medtech from Israel",
        "Diplomatic Position": "Austria historically pro-Israel within EU; Kurz-era alignment",
        "BDS Pressure": "Austrian parliament rejected BDS 2020; campus activism rising",
        "Refugee Secondary Effects": "Lebanon/Gaza displacement → Turkey → Balkan route",
        "EU Voting": "Austria key swing vote in EU foreign affairs council on MidEast",
    },
    "Taiwan": {
        "Semiconductor Dependency": "EU 50% chip-import dependent; Austria's automotive/industrial sector at risk",
        "Austrian Exposure": "AT&S (substrate tech) has Taiwan supply chain ties",
        "European Chips Act": "€43B EU initiative partly driven by Taiwan contingency planning",
        "Trade Disruption": "Taiwan strait closure → €200B/yr EU trade route disruption",
        "Austrian Industry": "Infineon Austria (Villach fab) partially insulated but peer-dependent",
    },
}

ECONOMIC_EXPOSURE = {
    "Iran": {
        "Oil Production": "3.2M bpd",
        "Strait of Hormuz": "21% of global oil transit",
        "Key Exports": "Crude oil, petrochemicals, metals",
        "Sanctions Regime": "US/EU comprehensive since 2018",
        "Market Sensitivity": "Brent crude +$5-15/bbl on escalation",
        "GDP": "$388B (2024 est.)",
    },
    "Russia": {
        "Oil Production": "9.5M bpd",
        "Gas Supply": "~15% of global LNG",
        "Key Exports": "Oil, gas, wheat, palladium, fertilizer",
        "Sanctions Regime": "G7 comprehensive since Feb 2022",
        "Market Sensitivity": "EU gas futures, wheat, palladium",
        "GDP": "$2.0T (2024 est.)",
    },
    "Israel": {
        "Tech Sector": "$22B annual exports",
        "Gas Production": "Leviathan + Tamar fields",
        "Key Exports": "Semiconductors, defense tech, pharma",
        "Trade Partners": "US (26%), EU (28%), China (8%)",
        "Market Sensitivity": "TA-35 index, defense sector equities",
        "GDP": "$525B (2024 est.)",
    },
    "Taiwan": {
        "Semiconductor Share": "65% of global foundry revenue",
        "TSMC": "92% of advanced chips (<7nm)",
        "Key Exports": "Semiconductors, electronics, machinery",
        "Trade Partners": "China (26%), US (15%), Japan (7%)",
        "Market Sensitivity": "SOX index, AAPL/NVDA supply chain",
        "GDP": "$790B (2024 est.)",
    },
}

# Historical benchmark events for context
HISTORICAL_BENCHMARKS = {
    "Iran": [
        {"event": "Soleimani assassination", "date": "2020-01-03", "score": 94},
        {"event": "JCPOA withdrawal", "date": "2018-05-08", "score": 72},
        {"event": "Tanker attacks, Gulf of Oman", "date": "2019-06-13", "score": 68},
        {"event": "US-Israel strikes begin", "date": "2026-02-28", "score": 85},
    ],
    "Russia": [
        {"event": "Ukraine invasion", "date": "2022-02-24", "score": 98},
        {"event": "Crimea annexation", "date": "2014-03-18", "score": 82},
        {"event": "Wagner mutiny", "date": "2023-06-24", "score": 74},
        {"event": "Kursk counteroffensive", "date": "2024-08-06", "score": 61},
    ],
    "Israel": [
        {"event": "Oct 7 Hamas attack", "date": "2023-10-07", "score": 97},
        {"event": "2021 Gaza conflict", "date": "2021-05-10", "score": 76},
        {"event": "2006 Lebanon war", "date": "2006-07-12", "score": 88},
        {"event": "Iran retaliation escalation", "date": "2026-03-05", "score": 82},
    ],
    "Taiwan": [
        {"event": "Pelosi visit crisis", "date": "2022-08-02", "score": 78},
        {"event": "PLA exercises escalation", "date": "2023-04-08", "score": 62},
        {"event": "Election tensions", "date": "2024-01-13", "score": 45},
    ],
}

# --- German versions ---

ECONOMIC_EXPOSURE_DE = {
    "Iran": {
        "Ölproduktion": "3,2 Mio. Barrel/Tag",
        "Straße von Hormuz": "21 % des globalen Öltransits",
        "Wichtigste Exporte": "Rohöl, Petrochemie, Metalle",
        "Sanktionsregime": "US/EU umfassend seit 2018",
        "Marktreaktion": "Brent-Rohöl +5–15 USD/Barrel bei Eskalation",
        "BIP": "388 Mrd. USD (2024, geschätzt)",
    },
    "Russland": {
        "Ölproduktion": "9,5 Mio. Barrel/Tag",
        "Gasversorgung": "~15 % des globalen LNG-Volumens",
        "Wichtigste Exporte": "Öl, Gas, Weizen, Palladium, Düngemittel",
        "Sanktionsregime": "G7 umfassend seit Feb. 2022",
        "Marktreaktion": "EU-Gas-Futures, Weizen, Palladium",
        "BIP": "2,0 Bio. USD (2024, geschätzt)",
    },
    "Israel": {
        "Technologiesektor": "22 Mrd. USD jährliche Exporte",
        "Gasproduktion": "Leviathan- und Tamar-Felder",
        "Wichtigste Exporte": "Halbleiter, Rüstungstechnik, Pharma",
        "Handelspartner": "USA (26 %), EU (28 %), China (8 %)",
        "Marktreaktion": "TA-35-Index, Rüstungsaktien",
        "BIP": "525 Mrd. USD (2024, geschätzt)",
    },
    "Taiwan": {
        "Halbleiteranteil": "65 % des globalen Halbleiter-Fertigungsumsatzes",
        "TSMC": "92 % der modernsten Chips (<7 nm)",
        "Wichtigste Exporte": "Halbleiter, Elektronik, Maschinen",
        "Handelspartner": "China (26 %), USA (15 %), Japan (7 %)",
        "Marktreaktion": "Philadelphia-Halbleiterindex (SOX), Apple-/Nvidia-Lieferkette",
        "BIP": "790 Mrd. USD (2024, geschätzt)",
    },
}

EU_AUSTRIA_EXPOSURE_DE = {
    "Iran": {
        "EU-Handelsrisiko": "3,2 Mrd. € EU-Iran-Handel (2023), Österreich ~180 Mio. €",
        "Energieauswirkung": "Österreich zu 80 % von Gasimporten abhängig; Iran-Eskalation → Brent +10 USD → VPI +0,3 %",
        "Flüchtlingsdruck": "UNHCR schätzt 500.000–2 Mio. Vertriebene bei voller Eskalation; Österreich an der Balkanroute",
        "Betroffene österr. Firmen": "OMV (Energie), Andritz (Industrie), voestalpine (Stahlzulieferung)",
        "EU-Sanktionslast": "Österreichische Banken tragen Kosten der Sekundärsanktions-Einhaltung",
        "NATO/Neutralität": "Österreichs Neutralität unter Druck; Transit- und Luftraumfragen",
    },
    "Russland": {
        "EU-Handelsrisiko": "EU-Russland-Handel seit 2022 um 60 % eingebrochen; Österreich verzeichnete Exporteinbußen von 4 Mrd. €",
        "Energieauswirkung": "Österreich war zu 80 % von russischem Gas abhängig (2021); derzeit ~50 %",
        "OMV-Risikoposition": "OMV schrieb 2,1 Mrd. € auf russische Vermögenswerte ab; Gazprom-Verträge strittig",
        "Raiffeisen Bank": "RBI: 22 Mrd. € Russland-Engagement — größte westliche Bank in Russland",
        "BIP-Auswirkung": "OeNB schätzt BIP-Effekt von -0,5 % durch Russland-Sanktionen seit 2022",
        "Flüchtlingsstrom": "380.000 ukrainische Vertriebene in Österreich; Integrationskosten 1,2 Mrd. €/Jahr",
    },
    "Israel": {
        "EU-Handelsrisiko": "47 Mrd. € EU-Israel-Handel; Österreich ~1,1 Mrd. € bilateral",
        "Technologieabhängigkeit": "Österreichische Unternehmen beziehen Cybersicherheits-, Agrar- und Medizintechnik aus Israel",
        "Diplomatische Position": "Österreich historisch pro-israelisch in der EU; Positionierung der Ära Kurz",
        "BDS-Druck": "Nationalrat lehnte BDS 2020 ab; Aktivismus an Hochschulen nimmt zu",
        "Sekundäre Flüchtlingseffekte": "Libanon/Gaza-Vertreibung → Türkei → Balkanroute",
        "EU-Abstimmung": "Österreich als wichtige Stimme im Rat für Auswärtige Angelegenheiten zum Nahen Osten",
    },
    "Taiwan": {
        "Halbleiterabhängigkeit": "EU zu 50 % von Chip-Importen abhängig; Österreichs Automobil- und Industriesektor gefährdet",
        "Österr. Risikoposition": "AT&S (Substrattechnik) ist von taiwanischer Lieferkette abhängig",
        "EU-Chipgesetz": "43 Mrd. € EU-Initiative, teilweise durch Taiwan-Krisenplanung motiviert",
        "Handelsunterbrechung": "Sperrung der Taiwanstraße → 200 Mrd. €/Jahr Störung der EU-Handelsrouten",
        "Österr. Industrie": "Infineon Austria (Werk Villach) teilweise abgesichert, aber abhängig von Zulieferern",
    },
}

HISTORICAL_BENCHMARKS_DE = {
    "Iran": [
        {"event": "Tötung Soleimanis", "date": "2020-01-03", "score": 94},
        {"event": "JCPOA-Ausstieg der USA", "date": "2018-05-08", "score": 72},
        {"event": "Tankerangriffe im Golf von Oman", "date": "2019-06-13", "score": 68},
        {"event": "Beginn der US-israelischen Angriffe", "date": "2026-02-28", "score": 85},
    ],
    "Russland": [
        {"event": "Invasion der Ukraine", "date": "2022-02-24", "score": 98},
        {"event": "Annexion der Krim", "date": "2014-03-18", "score": 82},
        {"event": "Wagner-Meuterei", "date": "2023-06-24", "score": 74},
        {"event": "Gegenoffensive bei Kursk", "date": "2024-08-06", "score": 61},
    ],
    "Israel": [
        {"event": "Hamas-Angriff vom 7. Oktober", "date": "2023-10-07", "score": 97},
        {"event": "Gaza-Konflikt 2021", "date": "2021-05-10", "score": 76},
        {"event": "Libanonkrieg 2006", "date": "2006-07-12", "score": 88},
        {"event": "Iranische Vergeltungseskalation", "date": "2026-03-05", "score": 82},
    ],
    "Taiwan": [
        {"event": "Krise um den Pelosi-Besuch", "date": "2022-08-02", "score": 78},
        {"event": "Eskalation der PLA-Manöver", "date": "2023-04-08", "score": 62},
        {"event": "Wahlspannungen", "date": "2024-01-13", "score": 45},
    ],
}
