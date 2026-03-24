/* GeoRisk Pulse — Translation System */
const T = {
  en: {
    // Tone words
    veryCritical: "Very critical", critical: "Critical", somewhatCritical: "Somewhat critical",
    favorable: "Favorable", somewhatFavorable: "Somewhat favorable", neutral: "Neutral",
    // Tabs
    riskScores: "Risk Scores", mediaAnalysis: "Media Analysis", publicOpinion: "Public Opinion",
    // Risk page
    situationAssessment: "Situation Assessment",
    readingGuideRisk: '<strong>How to read the scores:</strong> Each region is scored 0 to 100 based on the severity of today\'s news headlines. The number next to the score (e.g. +14) shows the change since yesterday. The small line shows the trend over the past week.',
    lowRisk: "Low risk", elevated: "Elevated", highRisk: "High risk, active conflict",
    riskTrend: "Risk Trend Over the Past 30 Days",
    riskTrendSub: "Each line shows one region. Higher = more dangerous. The shaded bands show the risk zones.",
    economicExposure: "Economic Exposure",
    euAustriaExposure: "EU & Austria Exposure Assessment",
    historicalBenchmarks: "Historical Benchmarks",
    methodology: "Methodology",
    methodologyRisk: "Scores derived from keyword-weighted NLP analysis of Reuters, AP, and Al Jazeera headlines. Top-heavy aggregation prioritizes high-severity signals; severity floors prevent dilution during active conflict. Entity amplification via spaCy NER. Headline volume contributes up to 15 points to daily score. Updated daily at 06:00 UTC.",
    refreshData: "Refresh Data", updating: "Updating...",
    high: "HIGH", elevatedLabel: "ELEVATED", low: "LOW",
    avg30d: "30d avg", avg90d: "90d avg", peak: "Peak",
    // Sentiment page
    readingGuideSentiment: '<strong>How to read this page:</strong> We analyze how 35+ news outlets from 16 countries report on each topic. Each headline gets a <strong>tone score</strong> from <strong>-1.0</strong> (very critical, hostile language) to <strong>+1.0</strong> (favorable, supportive language). A score near 0 means neutral, factual reporting.',
    negativeTone: "Negative tone (critical, hostile)", neutralTone: "Neutral tone (factual)", positiveTone: "Positive tone (favorable)",
    howMuchDisagree: "How Much Do News Outlets Disagree?",
    largeDisagreement: "Large disagreement",
    moderateDisagreement: "Moderate disagreement",
    generalConsensus: "General consensus",
    largeExplain: "Different outlets are telling very different stories about this topic. Some are highly critical while others are relatively measured.",
    moderateExplain: "There is some variation in how outlets cover this, but the overall direction is similar.",
    consensusExplain: "Most outlets are covering this topic in a similar tone.",
    mostCriticalOutlet: "Most critical outlet", leastCriticalOutlet: "Least critical outlet",
    basedOnOutlets: "Based on {n} international news outlets.",
    overallTone: "Overall Tone", headlinesAnalyzed: "Headlines Analyzed",
    mostCriticalMedia: "Most Critical Outlet", leastCriticalMedia: "Least Critical Outlet",
    acrossHeadlines: "Across all {total} headlines from {outlets} outlets",
    outletsFromCountries: "{outlets} outlets from {countries} countries",
    toneOf: "{tone} tone ({n} headlines)",
    toneByOutlet: "Tone of Coverage by News Outlet",
    toneByOutletSub: "Each bar shows one outlet's average tone. Bars extending left = more critical. Bars extending right = more favorable. The center line is neutral.",
    toneByCountry: "Tone of Coverage by Country",
    toneByCountrySub: "How each country's media as a whole frames the topic. Combines all outlets from that country.",
    toneHeatmap: "How Coverage Tone Changed Over 4 Weeks",
    toneHeatmapSub: 'Each cell represents one country on one day. <strong style="color: var(--risk-high);">Red</strong> = critical coverage that day. <strong style="color: var(--risk-low);">Green</strong> = favorable. Hover over any cell for the exact value.',
    strongestHeadlines: "Headlines With the Strongest Tone",
    strongestSub: "Sorted by strength of tone — the most opinionated headlines appear first.",
    methodologySentiment: 'Polarity scored via custom geopolitical lexicon (~200 terms) tuned for conflict, diplomacy, and political language. Scores range from -1.0 (strongly negative framing) to +1.0 (positive). Divergence measures the spread between most hawkish and most dovish outlets. Sources: 35 international outlets across 16 countries.',
    noData: "No data", loading: "Loading...",
    // Social page
    readingGuideSocial: '<strong>What this page shows:</strong> How ordinary people — not journalists — discuss these topics on Reddit, the world\'s largest English-language forum. We analyze posts from country-specific communities (e.g. r/unitedkingdom, r/india, r/Austria) to gauge public sentiment in each country.',
    readingGuideSocial2: 'The <strong>Perception Gap</strong> table below compares what the press says vs. what the public says. A large gap means the public sees things differently than the media portrays.',
    overallPublicMood: "Overall Public Mood", mostCriticalCountry: "Most Critical Country",
    leastCriticalCountry: "Least Critical Country", postsAnalyzed: "Posts Analyzed",
    acrossPosts: "Across {n} posts and comments", nCountries: "{n} countries",
    perceptionGap: "Where the Public Disagrees With the Media",
    perceptionGapSub: "Compares each country's media tone with the tone of its citizens online. A larger gap means the public sees this topic differently than the press portrays it.",
    insufficientGap: "Insufficient cross-data for gap analysis",
    gapCountry: "Country", gapMedia: "Media", gapPublic: "Public", gapGap: "Gap", gapDirection: "Direction",
    publicMoreCritical: "Public more critical", publicMoreFavorable: "Public more favorable",
    mediaFraming: "Media Framing by Country", publicSentiment: "Public Sentiment by Country",
    publicByCountry: "Public Sentiment by Country",
    publicByCountrySub: "Each bar shows the average tone of public discussion in that country. Based on posts and comments in country-specific online communities.",
    byCommunity: "Sentiment by Online Community",
    byCommunitySub: "Individual Reddit communities. Each subreddit (e.g. r/Austria, r/worldnews) represents a different audience.",
    samplePosts: "Sample Posts and Comments",
    samplePostsSub: "The most-discussed posts on this topic, sorted by engagement. Click any title to read the full discussion.",
    methodologySocial: "Public sentiment derived from country-specific Reddit communities (16 countries). Reddit skews young, male, English-speaking, and tech-literate — not representative of full populations. Country subreddits (e.g., r/iran) may reflect diaspora views. Upvote scores reflect platform dynamics, not scientific polling. Sentiment scored via the same geopolitical lexicon used in media analysis for cross-comparability.",
    fetchReddit: "Fetch Reddit Data", fetching: "Fetching...",
    methodologyCaveats: "Methodology & Caveats",
    // Months
    months: ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  },
  de: {
    veryCritical: "Sehr kritisch", critical: "Kritisch", somewhatCritical: "Eher kritisch",
    favorable: "Positiv", somewhatFavorable: "Eher positiv", neutral: "Neutral",
    riskScores: "Risikoeinschätzung", mediaAnalysis: "Medienanalyse", publicOpinion: "Öffentliche Meinung",
    situationAssessment: "Lageeinschätzung",
    readingGuideRisk: '<strong>So lesen Sie die Risikowerte:</strong> Jede Region wird auf einer Skala von 0 bis 100 bewertet, basierend auf der Schwere der aktuellen Nachrichtenlage. Die Zahl neben dem Wert (z.B. +14) zeigt die Veränderung seit gestern. Die kleine Linie zeigt den Trend der letzten Woche.',
    lowRisk: "Niedriges Risiko", elevated: "Erhöht", highRisk: "Hohes Risiko, aktiver Konflikt",
    riskTrend: "Risikotrend der letzten 30 Tage",
    riskTrendSub: "Jede Linie zeigt eine Region. Höher = gefährlicher. Die farbigen Bereiche zeigen die Risikozonen.",
    economicExposure: "Wirtschaftliche Verflechtung",
    euAustriaExposure: "EU- & Österreich-Risikoanalyse",
    historicalBenchmarks: "Historische Vergleichswerte",
    methodology: "Methodik",
    methodologyRisk: "Die Risikowerte basieren auf einer schlüsselwortgewichteten NLP-Analyse von Schlagzeilen bei Reuters, AP und Al Jazeera. Schwerwiegende Meldungen werden stärker gewichtet; bei aktiven Konflikten wird eine Mindestbewertung beibehalten. Das Nachrichtenvolumen fließt mit bis zu 15 Punkten in die Tagesbewertung ein. Aktualisierung täglich um 06:00 UTC.",
    refreshData: "Daten aktualisieren", updating: "Wird aktualisiert …",
    high: "HOCH", elevatedLabel: "ERHÖHT", low: "NIEDRIG",
    avg30d: "Ø 30 T.", avg90d: "Ø 90 T.", peak: "Höchstwert",
    readingGuideSentiment: '<strong>So lesen Sie diese Seite:</strong> Wir analysieren, wie über 35 Nachrichtenmedien aus 16 Ländern über jedes Thema berichten. Jede Schlagzeile erhält eine <strong>Tonbewertung</strong> von <strong>-1,0</strong> (sehr kritisch, feindselig) bis <strong>+1,0</strong> (positiv, unterstützend). Ein Wert nahe 0 bedeutet neutrale, sachliche Berichterstattung.',
    negativeTone: "Negativer Ton (kritisch, feindselig)", neutralTone: "Neutraler Ton (sachlich)", positiveTone: "Positiver Ton (unterstützend)",
    howMuchDisagree: "Wie stark weichen die Medien voneinander ab?",
    largeDisagreement: "Starke Abweichung",
    moderateDisagreement: "Mäßige Abweichung",
    generalConsensus: "Weitgehend einheitlich",
    largeExplain: "Verschiedene Medien berichten sehr unterschiedlich über dieses Thema. Einige sind stark kritisch, während andere eher gemäßigt sind.",
    moderateExplain: "Es gibt gewisse Unterschiede in der Berichterstattung, aber die Grundrichtung ist ähnlich.",
    consensusExplain: "Die meisten Medien berichten in einem ähnlichen Ton über dieses Thema.",
    mostCriticalOutlet: "Kritischstes Medium", leastCriticalOutlet: "Positivstes Medium",
    basedOnOutlets: "Basierend auf {n} internationalen Nachrichtenquellen.",
    overallTone: "Gesamtton", headlinesAnalyzed: "Analysierte Schlagzeilen",
    mostCriticalMedia: "Kritischstes Medium", leastCriticalMedia: "Positivstes Medium",
    acrossHeadlines: "Insgesamt {total} Schlagzeilen aus {outlets} Medien",
    outletsFromCountries: "{outlets} Medien aus {countries} Ländern",
    toneOf: "{tone} ({n} Schlagzeilen)",
    toneByOutlet: "Medienton nach Nachrichtenquelle",
    toneByOutletSub: "Jeder Balken zeigt den durchschnittlichen Ton einer Nachrichtenquelle. Balken nach links = kritischer. Balken nach rechts = positiver. Die Mittellinie ist neutral.",
    toneByCountry: "Medienton nach Land",
    toneByCountrySub: "Wie die Medien eines Landes insgesamt über das Thema berichten. Fasst alle Nachrichtenquellen des jeweiligen Landes zusammen.",
    toneHeatmap: "Entwicklung des Medientons über 4 Wochen",
    toneHeatmapSub: 'Jede Zelle zeigt ein Land an einem Tag. <strong style="color: var(--risk-high);">Rot</strong> = kritische Berichterstattung. <strong style="color: var(--risk-low);">Grün</strong> = positive Berichterstattung. Bewegen Sie die Maus über eine Zelle für den genauen Wert.',
    strongestHeadlines: "Schlagzeilen mit dem stärksten Ton",
    strongestSub: "Sortiert nach Stärke der Bewertung — die meinungsstärksten Schlagzeilen zuerst.",
    methodologySentiment: 'Tonanalyse mittels eines geopolitischen Lexikons (~200 Begriffe), optimiert für Konflikt-, Diplomatie- und politische Sprache. Werte von -1,0 (stark negative Darstellung) bis +1,0 (positiv). Die Divergenz misst die Spannweite zwischen den kritischsten und positivsten Medien. Quellen: 35 internationale Medien aus 16 Ländern.',
    noData: "Keine Daten", loading: "Laden …",
    readingGuideSocial: '<strong>Was diese Seite zeigt:</strong> Wie Bürgerinnen und Bürger — keine Journalistinnen und Journalisten — diese Themen auf Reddit diskutieren, dem weltweit größten englischsprachigen Forum. Wir analysieren Beiträge aus länderspezifischen Communities (z.B. r/unitedkingdom, r/india, r/Austria), um die öffentliche Stimmung in jedem Land zu erfassen.',
    readingGuideSocial2: 'Die Tabelle <strong>Wahrnehmungskluft</strong> unten vergleicht den Medienton mit der öffentlichen Meinung. Eine große Kluft bedeutet, dass die Bevölkerung das Thema anders sieht, als die Medien es darstellen.',
    overallPublicMood: "Öffentliche Gesamtstimmung", mostCriticalCountry: "Kritischstes Land",
    leastCriticalCountry: "Positivstes Land", postsAnalyzed: "Analysierte Beiträge",
    acrossPosts: "Insgesamt {n} Beiträge und Kommentare", nCountries: "{n} Länder",
    perceptionGap: "Wo die öffentliche Meinung von der Medienberichterstattung abweicht",
    perceptionGapSub: "Vergleicht den Medienton jedes Landes mit der Meinung seiner Bürgerinnen und Bürger im Internet. Eine größere Kluft bedeutet, dass die Öffentlichkeit das Thema anders sieht, als die Presse es darstellt.",
    insufficientGap: "Nicht genügend Daten für eine Vergleichsanalyse",
    gapCountry: "Land", gapMedia: "Medien", gapPublic: "Öffentlichkeit", gapGap: "Differenz", gapDirection: "Richtung",
    publicMoreCritical: "Öffentlichkeit kritischer", publicMoreFavorable: "Öffentlichkeit positiver",
    mediaFraming: "Medienton nach Land", publicSentiment: "Öffentliche Stimmung nach Land",
    publicByCountry: "Öffentliche Stimmung nach Land",
    publicByCountrySub: "Jeder Balken zeigt den durchschnittlichen Ton der öffentlichen Diskussion in diesem Land, basierend auf Beiträgen in länderspezifischen Online-Communities.",
    byCommunity: "Stimmung nach Online-Community",
    byCommunitySub: "Einzelne Reddit-Communities. Jedes Subreddit (z.B. r/Austria, r/worldnews) steht für ein anderes Publikum.",
    samplePosts: "Beispielbeiträge und Kommentare",
    samplePostsSub: "Die meistdiskutierten Beiträge zu diesem Thema, sortiert nach Resonanz. Klicken Sie auf einen Titel, um die gesamte Diskussion zu lesen.",
    methodologySocial: "Öffentliche Stimmung abgeleitet aus länderspezifischen Reddit-Communities (16 Länder). Reddit-Nutzerinnen und -Nutzer sind überproportional jung, männlich, englischsprachig und technikaffin — nicht repräsentativ für die Gesamtbevölkerung. Länderspezifische Subreddits (z.B. r/iran) spiegeln möglicherweise eher Diaspora-Perspektiven wider. Stimmungsbewertung mittels desselben geopolitischen Lexikons wie in der Medienanalyse, um Vergleichbarkeit zu gewährleisten.",
    fetchReddit: "Reddit-Daten abrufen", fetching: "Wird abgerufen …",
    methodologyCaveats: "Methodik & Einschränkungen",
    months: ['','Jän','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'],
  }
};

const LANG = new URLSearchParams(window.location.search).get('lang') === 'de' ? 'de' : 'en';
function t(key) { return (T[LANG] && T[LANG][key]) || T['en'][key] || key; }
function tf(key, vars) {
  let s = t(key);
  if (vars) for (const [k, v] of Object.entries(vars)) s = s.replaceAll(`{${k}}`, v);
  return s;
}
function toneWord(p) {
    if (p <= -0.4) return t('veryCritical');
    if (p <= -0.2) return t('critical');
    if (p <= -0.05) return t('somewhatCritical');
    if (p >= 0.2) return t('favorable');
    if (p >= 0.05) return t('somewhatFavorable');
    return t('neutral');
}
function toggleLang() {
    const url = new URL(window.location);
    url.searchParams.set('lang', LANG === 'en' ? 'de' : 'en');
    window.location = url;
}

// Theme: light/dark mode — light is default
const THEME = localStorage.getItem('georisk-theme') || 'light';
if (THEME === 'dark') document.body.classList.add('dark');
// Note: no class needed for light — it's the default via CSS

// Set initial button text once DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const isDark = document.body.classList.contains('dark');
    document.querySelectorAll('.theme-toggle').forEach(btn => {
        btn.textContent = isDark ? '☀' : '☾';
    });
});

function _applyThemeToCharts() {
    const isDark = document.body.classList.contains('dark');
    const newBg = isDark ? '#12151A' : '#FFFFFF';
    const newGrid = isDark ? '#1A1D22' : '#E8E8EC';
    const newFont = isDark ? '#A0A6AF' : '#555555';
    const newZero = isDark ? '#333333' : '#CCCCCC';
    document.querySelectorAll('.js-plotly-plot').forEach(el => {
        try {
            Plotly.relayout(el, {
                'paper_bgcolor': newBg, 'plot_bgcolor': newBg,
                'font.color': newFont,
                'xaxis.gridcolor': newGrid, 'yaxis.gridcolor': newGrid,
                'xaxis.zerolinecolor': newZero, 'yaxis.zerolinecolor': newZero,
            });
        } catch(e) {}
    });
}

function toggleTheme() {
    const isDark = document.body.classList.toggle('dark');
    localStorage.setItem('georisk-theme', isDark ? 'dark' : 'light');
    _applyThemeToCharts();
    document.querySelectorAll('.theme-toggle').forEach(btn => {
        btn.textContent = isDark ? '☀' : '☾';
    });
}
