import json
import urllib.request
import datetime
import random
import os
import sys

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("FEHLER: GEMINI_API_KEY ist nicht gesetzt")
    sys.exit(1)

ARTIKEL_DATEI = 'articles.json'

THEMEN = [
    {
        "category": "Marktbericht",
        "emoji": "🏙️",
        "thema": "den aktuellen Immobilienmarkt in Düsseldorf – Preise, Nachfrage, Trends und Ausblick"
    },
    {
        "category": "Kaufen",
        "emoji": "🔑",
        "thema": "praktische Tipps und häufige Fehler beim Kauf einer Immobilie in Düsseldorf"
    },
    {
        "category": "Verkaufen",
        "emoji": "📋",
        "thema": "wie man eine Immobilie in Düsseldorf erfolgreich und zum besten Preis verkauft"
    },
    {
        "category": "Stadtteile",
        "emoji": "🏘️",
        "thema": "einen dieser Düsseldorfer Stadtteile: Oberkassel, Pempelfort, Bilk, Flingern, Gerresheim, Benrath, Golzheim, Niederkassel, Unterbilk oder Derendorf – Wohnqualität, Infrastruktur, Immobilienpreise"
    },
    {
        "category": "Finanzierung",
        "emoji": "💶",
        "thema": "Finanzierungsoptionen, KfW-Förderungen oder Zinsentwicklungen für Immobilienkäufer in Düsseldorf"
    },
    {
        "category": "Ratgeber",
        "emoji": "📊",
        "thema": "einen wichtigen Immobilien-Ratgeber-Tipp, z.B. zu Energieausweis, Grunderwerbsteuer, Notarkosten, Maklergebühren oder Grundbuch"
    },
    {
        "category": "Vermietung",
        "emoji": "🏢",
        "thema": "Vermietung von Wohnungen oder Häusern in Düsseldorf – Mietrecht, Mietpreise, Tipps für Vermieter"
    },
    {
        "category": "Ratgeber",
        "emoji": "🏗️",
        "thema": "Neubau vs. Bestandsimmobilien in Düsseldorf – was lohnt sich mehr und worauf man achten sollte"
    }
]

MONATE_DE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}


def datum_de(d):
    return f"{d.day}. {MONATE_DE[d.month]} {d.year}"


def generiere_artikel():
    thema = random.choice(THEMEN)
    heute = datetime.date.today()

    prompt = f"""Schreibe einen professionellen, informativen Immobilien-Blogartikel auf Deutsch für Krischer Immobilien aus Düsseldorf.

Thema: {thema['thema']}

Anforderungen:
- Länge: 380-450 Wörter
- Ton: seriös, kompetent, lokal (Düsseldorf-Bezug)
- Keinerlei konkrete Preisversprechen oder Rechtsberatung
- Erwähne "Krischer Immobilien" einmal natürlich im Text
- Vollständig origineller Text, kein Plagiat
- Schreibe Absätze, keinen Fließtext-Block
- Schließe mit einer kurzen, freundlichen Handlungsaufforderung ab (Kontakt zu Krischer Immobilien)

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt – kein Text davor oder danach, keine Erklärungen:
{{
  "title": "Artikel-Titel (max. 68 Zeichen, enthält Düsseldorf, SEO-optimiert)",
  "excerpt": "Eine Zusammenfassung als einziger Satz (max. 155 Zeichen)",
  "content": "Vollständiger Artikeltext, Absätze mit \\n\\n getrennt",
  "readTime": "4"
}}"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 1400,
            "responseMimeType": "application/json"
        }
    }).encode('utf-8')

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(req, timeout=90) as resp:
        result = json.loads(resp.read().decode('utf-8'))

    raw = result['candidates'][0]['content']['parts'][0]['text'].strip()

    # JSON-Block aus Markdown-Fence herauslösen falls vorhanden
    if raw.startswith('```'):
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]
    raw = raw.strip()

    artikel_daten = json.loads(raw)

    artikel_id = f"{heute.strftime('%Y%m%d')}-{random.randint(100, 999)}"

    return {
        "id": artikel_id,
        "date": datum_de(heute),
        "datetime": heute.isoformat(),
        "category": thema['category'],
        "emoji": thema['emoji'],
        "title": artikel_daten['title'],
        "excerpt": artikel_daten['excerpt'],
        "content": artikel_daten['content'],
        "readTime": artikel_daten.get('readTime', '4')
    }


def aktualisiere_json(neuer_artikel):
    if os.path.exists(ARTIKEL_DATEI):
        with open(ARTIKEL_DATEI, 'r', encoding='utf-8') as f:
            daten = json.load(f)
    else:
        daten = {"articles": []}

    daten['articles'].insert(0, neuer_artikel)
    daten['articles'] = daten['articles'][:24]  # max. 24 Artikel
    daten['updated'] = datetime.date.today().isoformat()

    with open(ARTIKEL_DATEI, 'w', encoding='utf-8') as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)

    print(f"Gespeichert: {neuer_artikel['title']}")


if __name__ == '__main__':
    print("Starte Artikel-Generierung...")
    artikel = generiere_artikel()
    aktualisiere_json(artikel)
    print("Fertig.")
