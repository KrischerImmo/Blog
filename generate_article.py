import json
import datetime
import random
import os
import urllib.request

ARTIKEL_DATEI = 'articles.json'

MONATE_DE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}

STADTTEILE = [
    "Oberkassel", "Pempelfort", "Bilk", "Flingern", "Gerresheim",
    "Benrath", "Golzheim", "Niederkassel", "Unterbilk", "Derendorf",
    "Eller", "Volmerswerth", "Hafen", "Heerdt", "Stockum"
]

def datum_de(d):
    return f"{d.day}. {MONATE_DE[d.month]} {d.year}"

BASE = "https://krischerimmo.github.io/Blog/"

LOKALE_BILDER = {
    "Marktbericht": [BASE + "images/marktbericht.jpg"],
    "Kaufen":       [BASE + "images/kaufen.jpg"],
    "Verkaufen":    [BASE + "images/verkaufen.jpg"],
    "Stadtteile":   [BASE + "images/stadtteile.jpg"],
    "Finanzierung": [BASE + "images/finanzierung.jpg"],
    "Ratgeber":     [BASE + "images/ratgeber.jpg"],
    "Vermietung":   [BASE + "images/vermietung.jpg"],
}

def lokales_bild(kategorie):
    optionen = LOKALE_BILDER.get(kategorie, ["images/marktbericht.jpg"])
    return random.choice(optionen)

def bild_url(suchbegriff, kategorie):
    api_key = os.environ.get('PEXELS_API_KEY', '')
    if api_key:
        try:
            url = f"https://api.pexels.com/v1/search?query={urllib.request.quote(suchbegriff)}&per_page=1&orientation=landscape"
            req = urllib.request.Request(url, headers={"Authorization": api_key})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            fotos = data.get("photos", [])
            if fotos:
                return fotos[0]["src"]["large2x"]
        except Exception as e:
            print(f"Pexels Fehler: {e}")
    return lokales_bild(kategorie)

TEMPLATES = [

    # ── MARKTBERICHT ──────────────────────────────────────────────
    {
        "category": "Marktbericht",
        "emoji": "🏙️",
        "bild": "aerial view city residential buildings",
        "title": "Immobilienmarkt Düsseldorf {JAHR}: Trends und Ausblick für Käufer",
        "excerpt": "Wie entwickeln sich Preise und Nachfrage in Düsseldorf {JAHR}? Ein aktueller Überblick von Krischer Immobilien.",
        "content": (
            "Der Düsseldorfer Immobilienmarkt zeigt sich {JAHR} von einer stabilen Seite. "
            "Trotz veränderter Rahmenbedingungen bleibt die Nachfrage nach Wohnimmobilien in der Landeshauptstadt hoch – "
            "insbesondere in gefragten Lagen wie {STADTTEIL1} und {STADTTEIL2}.\n\n"
            "Besonders hervorzuheben ist die Entwicklung im Segment der Eigentumswohnungen: "
            "Hier zeigt sich eine stabile Nachfrage, getragen von Eigennutzern und langfristig orientierten Kapitalanlegern. "
            "Einfamilienhäuser im Stadtgebiet sind weiterhin knapp und erzielen entsprechend solide Preise.\n\n"
            "Interessant ist der Blick auf aufstrebende Stadtteile wie {STADTTEIL3}: "
            "Junge Familien und Berufstätige entdecken diese Lagen zunehmend und schätzen das gute Preis-Leistungs-Verhältnis "
            "bei gleichzeitig guter Infrastruktur und Nahverkehrsanbindung.\n\n"
            "Für Verkäufer gilt: Qualitätsobjekte in guten Lagen finden nach wie vor schnell Abnehmer. "
            "Entscheidend ist jedoch eine realistische Preisfindung auf Basis aktueller Marktdaten – "
            "überhöhte Angebotspreise führen zu langen Vermarktungszeiten und im Zweifel zu Preisabschlägen.\n\n"
            "Käufer sollten sich nicht unter Zeitdruck setzen lassen. Eine solide Finanzierungsplanung "
            "und ein klares Anforderungsprofil sind die besten Voraussetzungen für eine erfolgreiche Suche.\n\n"
            "Krischer Immobilien begleitet Sie als erfahrener Partner auf dem Düsseldorfer Immobilienmarkt – "
            "von der ersten Beratung bis zur Schlüsselübergabe. Sprechen Sie uns gerne an."
        )
    },
    {
        "category": "Marktbericht",
        "emoji": "🏙️",
        "bild": "modern apartment building exterior facade",
        "title": "Wohnungsmarkt Düsseldorf {JAHR}: Was sich Käufer jetzt merken sollten",
        "excerpt": "Der Düsseldorfer Wohnungsmarkt {JAHR} im Überblick – Chancen, Risiken und aktuelle Entwicklungen.",
        "content": (
            "Düsseldorf gehört zu den wirtschaftsstärksten Städten Deutschlands – "
            "und das spiegelt sich auch auf dem Immobilienmarkt wider. "
            "Die Nachfrage nach Wohnraum übersteigt das Angebot in vielen Lagen deutlich, "
            "was zu einer anhaltend stabilen Preisentwicklung führt.\n\n"
            "Besonders {STADTTEIL1} und {STADTTEIL2} verzeichnen eine hohe Nachfrage. "
            "Gute Schulen, eine exzellente Infrastruktur und die Nähe zu Arbeitgebern "
            "machen diese Lagen für Familien und Berufspendler gleichermaßen attraktiv.\n\n"
            "Wer in Düsseldorf kaufen möchte, sollte gut vorbereitet sein: "
            "Attraktive Objekte werden häufig innerhalb weniger Tage verkauft. "
            "Eine Finanzierungszusage der Bank im Vorfeld verschafft entscheidende Vorteile.\n\n"
            "Für Investoren bleibt Düsseldorf ein interessanter Standort. "
            "Die Mietrenditen sind solide, die Leerstandsquote gering und die Bevölkerungsprognose positiv.\n\n"
            "Möchten Sie wissen, was Ihre Immobilie aktuell wert ist oder suchen Sie "
            "das passende Objekt in Düsseldorf? Krischer Immobilien steht Ihnen mit "
            "fundierter Marktkenntnis und persönlicher Beratung zur Seite. Kontaktieren Sie uns noch heute."
        )
    },

    # ── KAUFEN ──────────────────────────────────────────────────
    {
        "category": "Kaufen",
        "emoji": "🔑",
        "bild": "house keys front door real estate",
        "title": "Immobilie kaufen in Düsseldorf: {ANZAHL} Tipps für Ihren Erfolg",
        "excerpt": "Wer in Düsseldorf eine Immobilie kaufen möchte, sollte diese {ANZAHL} wichtigen Punkte kennen.",
        "content": (
            "Der Kauf einer Immobilie ist eine der bedeutendsten Entscheidungen im Leben. "
            "Gerade in einer gefragten Stadt wie Düsseldorf lohnt es sich, gut vorbereitet zu sein. "
            "Wir von Krischer Immobilien haben die wichtigsten Tipps für Sie zusammengestellt.\n\n"
            "1. Finanzierung klären: Bevor Sie auf Besichtigungen gehen, sollten Sie wissen, "
            "was Sie sich leisten können. Eine Finanzierungszusage Ihrer Bank gibt Ihnen Sicherheit "
            "und macht Sie als Käufer glaubwürdiger.\n\n"
            "2. Lage priorisieren: In Düsseldorf gilt: Lage, Lage, Lage. "
            "Stadtteile wie {STADTTEIL1} und {STADTTEIL2} bieten unterschiedliche Vorzüge – "
            "von Rheinlage bis Szene-Viertel. Definieren Sie Ihre Prioritäten im Vorfeld.\n\n"
            "3. Nebenkosten einplanen: Grunderwerbsteuer, Notarkosten und eventuelle Maklergebühren "
            "können zusammen rund 10–12 Prozent des Kaufpreises ausmachen. "
            "Diese Summe sollte idealerweise aus Eigenkapital stammen.\n\n"
            "4. Objektzustand prüfen: Lassen Sie eine Immobilie vor dem Kauf von einem Sachverständigen "
            "begutachten – besonders bei Altbauten. Versteckte Mängel können teuer werden.\n\n"
            "5. Schnell entscheiden: Gute Objekte in Düsseldorf sind begehrt. "
            "Wer vorbereitet ist, kann schneller handeln und erhält den Zuschlag.\n\n"
            "Sprechen Sie uns an – Krischer Immobilien begleitet Sie auf dem Weg zu Ihrer Traumimmobilie in Düsseldorf."
        )
    },

    # ── VERKAUFEN ──────────────────────────────────────────────────
    {
        "category": "Verkaufen",
        "emoji": "📋",
        "bild": "house with garden for sale sunny",
        "title": "Immobilie verkaufen in Düsseldorf: So erzielen Sie den besten Preis",
        "excerpt": "Mit der richtigen Strategie erzielen Sie beim Immobilienverkauf in Düsseldorf den bestmöglichen Preis.",
        "content": (
            "Der Verkauf einer Immobilie in Düsseldorf kann – richtig angegangen – "
            "ein sehr erfolgreiches Vorhaben sein. Doch wie bei vielen Dingen im Leben "
            "liegt der Unterschied zwischen einem guten und einem sehr guten Ergebnis in der Vorbereitung.\n\n"
            "Der erste und wichtigste Schritt ist eine realistische Wertermittlung. "
            "Viele Eigentümer tendieren dazu, den Wert ihrer Immobilie zu überschätzen – "
            "sei es aus emotionalen Gründen oder aufgrund veralteter Vergleichswerte. "
            "Ein zu hoher Angebotspreis schreckt Interessenten ab und verlängert die Vermarktungsdauer erheblich.\n\n"
            "Investieren Sie in eine professionelle Präsentation: Hochwertige Fotos, "
            "ein ansprechendes Exposé und ein gepflegter Ersteindruck beim Besichtigungstermin "
            "machen einen entscheidenden Unterschied. In {STADTTEIL1} und {STADTTEIL2} "
            "können gut präsentierte Objekte deutlich höhere Preise erzielen.\n\n"
            "Stellen Sie alle notwendigen Unterlagen rechtzeitig zusammen: "
            "Energieausweis, Grundbuchauszug, Baupläne und Nebenkostenabrechnungen "
            "sollten beim ersten Interessentengespräch verfügbar sein.\n\n"
            "Krischer Immobilien übernimmt für Sie die professionelle Vermarktung Ihrer Immobilie in Düsseldorf – "
            "von der Wertermittlung über die Besichtigungen bis zum notariellen Abschluss. "
            "Nehmen Sie jetzt Kontakt auf und lassen Sie sich unverbindlich beraten."
        )
    },

    # ── STADTTEILE ──────────────────────────────────────────────────
    {
        "category": "Stadtteile",
        "emoji": "🏘️",
        "bild": "suburban street houses neighborhood",
        "title": "{STADTTEIL1}: Wohnen und Leben in Düsseldorf im Überblick",
        "excerpt": "{STADTTEIL1} gehört zu den beliebtesten Stadtteilen Düsseldorfs – Wohnqualität, Infrastruktur und Immobilienpreise.",
        "content": (
            "{STADTTEIL1} ist einer der vielseitigsten Stadtteile Düsseldorfs und zieht "
            "Familien, Berufstätige und Kapitalanleger gleichermaßen an. "
            "Was macht diesen Stadtteil so besonders?\n\n"
            "Die Infrastruktur in {STADTTEIL1} ist hervorragend: "
            "Einkaufsmöglichkeiten, Schulen, Kindergärten und medizinische Versorgung "
            "sind gut erreichbar. Die Anbindung an den öffentlichen Nahverkehr ermöglicht "
            "eine schnelle Verbindung in die Innenstadt und zu wichtigen Arbeitgebern.\n\n"
            "Das Wohnungsangebot in {STADTTEIL1} ist vielfältig: "
            "Vom klassischen Gründerzeithaus bis zum modernen Neubau findet sich hier "
            "für unterschiedliche Ansprüche und Budgets das passende Objekt. "
            "Besonders beliebt sind Eigentumswohnungen mit Balkon oder Terrasse.\n\n"
            "Im Vergleich zu Toplagen wie Oberkassel bietet {STADTTEIL1} oft noch "
            "attraktivere Preise bei vergleichbarer Lebensqualität – "
            "ein Vorteil, den immer mehr Käufer für sich entdecken.\n\n"
            "Benachbarte Stadtteile wie {STADTTEIL2} und {STADTTEIL3} ergänzen das Angebot "
            "und machen den Bereich zu einem der interessantesten Wohngebiete Düsseldorfs.\n\n"
            "Sie interessieren sich für eine Immobilie in {STADTTEIL1} oder möchten "
            "Ihre dortige Immobilie verkaufen? Krischer Immobilien kennt diesen Markt "
            "und berät Sie gerne persönlich. Sprechen Sie uns an!"
        )
    },

    # ── FINANZIERUNG ──────────────────────────────────────────────────
    {
        "category": "Finanzierung",
        "emoji": "💶",
        "bild": "house coins money investment property",
        "title": "Baufinanzierung in Düsseldorf {JAHR}: Was Sie jetzt wissen müssen",
        "excerpt": "Aktuelle Tipps zur Immobilienfinanzierung in Düsseldorf – Zinsen, Eigenkapital und Förderprogramme {JAHR}.",
        "content": (
            "Die Finanzierung ist das Fundament jedes Immobilienkaufs. "
            "Wer in Düsseldorf kaufen möchte, sollte sich frühzeitig mit den "
            "aktuellen Konditionen und Fördermöglichkeiten auseinandersetzen.\n\n"
            "Eigenkapital ist nach wie vor der wichtigste Faktor: "
            "Experten empfehlen, mindestens 20 Prozent des Kaufpreises zuzüglich der Nebenkosten "
            "aus eigenen Mitteln einzubringen. Wer mehr Eigenkapital mitbringt, "
            "profitiert in der Regel von günstigeren Zinsen und besseren Konditionen.\n\n"
            "Die KfW-Bank bietet verschiedene Förderprogramme an, die beim Immobilienkauf "
            "in Düsseldorf genutzt werden können. Besonders das Programm "
            "Wohneigentum für Familien ist für Familien mit Kindern interessant "
            "und ermöglicht zinsgünstige Darlehen für Erstkäufer.\n\n"
            "Vergleichen Sie immer mehrere Angebote: Die Unterschiede zwischen den Konditionen "
            "verschiedener Banken können über die Laufzeit eines Darlehens erheblich sein. "
            "Ein unabhängiger Finanzierungsberater kann Ihnen helfen, das beste Angebot zu finden.\n\n"
            "Planen Sie realistisch: Neben der monatlichen Rate sollten Sie auch "
            "Rücklagen für Instandhaltung und unvorhergesehene Ausgaben einkalkulieren.\n\n"
            "Krischer Immobilien unterstützt Sie nicht nur bei der Suche nach der passenden "
            "Immobilie in Düsseldorf, sondern vermittelt Ihnen auch Kontakte zu erfahrenen "
            "Finanzierungspartnern. Nehmen Sie jetzt Kontakt auf!"
        )
    },

    # ── RATGEBER ──────────────────────────────────────────────────
    {
        "category": "Ratgeber",
        "emoji": "📊",
        "bild": "eco house solar panels green energy home",
        "title": "Energieausweis beim Immobilienverkauf in Düsseldorf: Was ist zu beachten?",
        "excerpt": "Der Energieausweis ist Pflicht beim Immobilienverkauf – was Eigentümer in Düsseldorf wissen müssen.",
        "content": (
            "Wer seine Immobilie in Düsseldorf verkaufen oder vermieten möchte, "
            "kommt am Energieausweis nicht vorbei. Dieses Dokument ist gesetzlich vorgeschrieben "
            "und muss Interessenten spätestens bei der Besichtigung vorgelegt werden.\n\n"
            "Es gibt zwei Arten von Energieausweisen: den Verbrauchsausweis und den Bedarfsausweis. "
            "Der Verbrauchsausweis basiert auf dem tatsächlichen Energieverbrauch der vergangenen Jahre, "
            "der Bedarfsausweis auf einer technischen Analyse des Gebäudes. "
            "Für Gebäude mit weniger als fünf Wohneinheiten und Bauantrag vor 1977 "
            "ist in der Regel der Bedarfsausweis vorgeschrieben.\n\n"
            "Die Energieeffizienzklassen reichen von A+ (sehr effizient) bis H (wenig effizient). "
            "Ein gutes Energiezeugnis kann den Verkaufswert einer Immobilie positiv beeinflussen – "
            "Käufer achten zunehmend auf die zu erwartenden Nebenkosten.\n\n"
            "In Düsseldorf können Energieausweise bei zugelassenen Energieberatern, "
            "Architekten oder Ingenieuren beantragt werden. "
            "Die Kosten variieren je nach Art und Aufwand.\n\n"
            "Tipp: Wer energetische Sanierungsmaßnahmen plant, sollte vorab prüfen, "
            "welche Fördermittel von KfW oder BAFA in Anspruch genommen werden können.\n\n"
            "Bei Fragen rund um den Immobilienverkauf in Düsseldorf steht Ihnen "
            "Krischer Immobilien jederzeit beratend zur Seite. Sprechen Sie uns an!"
        )
    },
    {
        "category": "Ratgeber",
        "emoji": "🏗️",
        "bild": "new house construction building site workers",
        "title": "Neubau oder Bestandsimmobilie in Düsseldorf – was passt zu Ihnen?",
        "excerpt": "Neubau oder Bestand? Beide Optionen haben in Düsseldorf ihre Vor- und Nachteile – eine Entscheidungshilfe.",
        "content": (
            "Eine der grundlegenden Fragen beim Immobilienkauf in Düsseldorf lautet: "
            "Neubau oder Bestandsimmobilie? Beide Varianten haben ihre spezifischen Vor- und Nachteile "
            "und die Antwort hängt stark von Ihren persönlichen Prioritäten ab.\n\n"
            "Neubauten punkten mit moderner Ausstattung, niedrigen Energiekosten und "
            "aktuellen Sicherheitsstandards. Sie können oft individuell mitgestaltet werden "
            "und bieten in der Regel eine lange störungsfreie Nutzungszeit. "
            "Allerdings sind die Kaufpreise in Düsseldorf für Neubauten deutlich höher "
            "als für vergleichbare Bestandsimmobilien.\n\n"
            "Bestandsimmobilien hingegen bieten oft mehr Charme und Charakter – "
            "Altbauwohnungen in {STADTTEIL1} oder {STADTTEIL2} sind dafür bekannte Beispiele. "
            "Sie sind häufig günstiger, befinden sich aber möglicherweise in weniger energieeffizientem Zustand. "
            "Hier sollten Käufer potenzielle Renovierungskosten einkalkulieren.\n\n"
            "Ein wichtiger Faktor ist auch der Zeitaspekt: "
            "Beim Neubau kann es von der Vertragsunterzeichnung bis zum Einzug "
            "oft ein bis zwei Jahre dauern. Wer schnell einziehen möchte, ist mit "
            "einer Bestandsimmobilie besser bedient.\n\n"
            "Krischer Immobilien berät Sie gerne bei der Entscheidung und "
            "zeigt Ihnen passende Angebote in Düsseldorf – ob Neubau oder Bestand. "
            "Nehmen Sie jetzt Kontakt auf!"
        )
    },

    # ── VERMIETUNG ──────────────────────────────────────────────────
    {
        "category": "Vermietung",
        "emoji": "🏢",
        "bild": "apartment building balcony rental exterior",
        "title": "Wohnung vermieten in Düsseldorf: Tipps für erfolgreiche Vermietung",
        "excerpt": "Als Vermieter in Düsseldorf erfolgreich sein – mit diesen Tipps finden Sie schnell gute Mieter.",
        "content": (
            "Düsseldorf ist ein begehrter Mietmarkt: Die Nachfrage nach Mietwohnungen "
            "übersteigt in vielen Stadtteilen das Angebot. Das klingt gut für Vermieter – "
            "doch auch hier lohnt sich eine durchdachte Strategie.\n\n"
            "Setzen Sie den Mietpreis realistisch: Eine zu hohe Miete schreckt gute Mieter ab "
            "und führt zu langen Leerstandszeiten. Orientieren Sie sich am aktuellen Mietspiegel "
            "und vergleichbaren Angeboten in {STADTTEIL1} und Umgebung.\n\n"
            "Investieren Sie in die Präsentation: Gute Fotos und eine vollständige Beschreibung "
            "der Wohnung sorgen für mehr und bessere Bewerbungen. "
            "Achten Sie auf Sauberkeit und kleine Schönheitsreparaturen vor der Besichtigung.\n\n"
            "Wählen Sie Mieter sorgfältig aus: Eine Selbstauskunft, "
            "Gehaltsnachweise und eine Schufa-Auskunft sind wichtige Instrumente "
            "zur Mieterauswahl. Nehmen Sie sich die Zeit für ein persönliches Gespräch.\n\n"
            "Kennen Sie Ihre Pflichten: Als Vermieter sind Sie für die Instandhaltung "
            "der Immobilie verantwortlich. Betriebskosten müssen korrekt abgerechnet werden. "
            "Informieren Sie sich über aktuelle Mietrechtsregelungen.\n\n"
            "Krischer Immobilien unterstützt Sie bei der professionellen Vermarktung "
            "und Vermietung Ihrer Immobilie in Düsseldorf. "
            "Sprechen Sie uns an – wir finden für Sie den passenden Mieter."
        )
    },
]


def render_template(tmpl, heute):
    st = random.sample(STADTTEILE, 3)
    anzahlen = ["5", "6", "7", "8"]
    text = tmpl.copy()
    for key in ["title", "excerpt", "content"]:
        text[key] = (
            text[key]
            .replace("{STADTTEIL1}", st[0])
            .replace("{STADTTEIL2}", st[1])
            .replace("{STADTTEIL3}", st[2])
            .replace("{JAHR}", str(heute.year))
            .replace("{MONAT}", MONATE_DE[heute.month])
            .replace("{ANZAHL}", random.choice(anzahlen))
        )
    return text


def generiere_bild_url(suchbegriff, kategorie):
    return bild_url(suchbegriff, kategorie)


def generiere_artikel():
    heute = datetime.date.today()
    tmpl = random.choice(TEMPLATES)
    filled = render_template(tmpl, heute)
    artikel_id = f"{heute.strftime('%Y%m%d')}-{random.randint(100, 999)}"
    return {
        "id": artikel_id,
        "date": datum_de(heute),
        "datetime": heute.isoformat(),
        "category": tmpl["category"],
        "emoji": tmpl["emoji"],
        "imageUrl": generiere_bild_url(tmpl["bild"], tmpl["category"]),
        "title": filled["title"],
        "excerpt": filled["excerpt"],
        "content": filled["content"],
        "readTime": "4"
    }


def repariere_bilder(daten):
    for a in daten.get("articles", []):
        url = a.get("imageUrl", "")
        if not url or "picsum" in url or url.startswith("http") and "pexels" not in url:
            a["imageUrl"] = lokales_bild(a.get("category", "Marktbericht"))
            print(f"Bild repariert: {a.get('title','')[:50]}")

def aktualisiere_json(neuer_artikel):
    daten = {"articles": []}
    if os.path.exists(ARTIKEL_DATEI):
        try:
            with open(ARTIKEL_DATEI, 'r', encoding='utf-8') as f:
                daten = json.load(f)
        except (json.JSONDecodeError, ValueError):
            print("articles.json war ungültig – starte neu.")
            daten = {"articles": []}
    repariere_bilder(daten)
    daten['articles'].insert(0, neuer_artikel)
    daten['articles'] = daten['articles'][:24]
    daten['updated'] = datetime.date.today().isoformat()
    with open(ARTIKEL_DATEI, 'w', encoding='utf-8') as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
    print(f"Gespeichert: {neuer_artikel['title']}")


if __name__ == '__main__':
    print("Starte Artikel-Generierung...")
    artikel = generiere_artikel()
    aktualisiere_json(artikel)
    print("Fertig.")
