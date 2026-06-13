import json
import urllib.request
import urllib.parse
import urllib.error
import datetime
import random
import os
import sys

ARTIKEL_DATEI = 'articles.json'

THEMEN = [
    {
        "category": "Marktbericht",
        "emoji": "🏙️",
        "thema": "den aktuellen Immobilienmarkt in Düsseldorf – Preise, Nachfrage, Trends und Ausblick",
        "bild_prompt": "Düsseldorf skyline Rhine Tower modern city architecture aerial view professional real estate photography"
    },
    {
        "category": "Kaufen",
        "emoji": "🔑",
        "thema": "praktische Tipps und häufige Fehler beim Kauf einer Immobilie in Düsseldorf",
        "bild_prompt": "modern luxury apartment interior Düsseldorf Germany bright living room real estate photography"
    },
    {
        "category": "Verkaufen",
        "emoji": "📋",
        "thema": "wie man eine Immobilie in Düsseldorf erfolgreich und zum besten Preis verkauft",
        "bild_prompt": "beautiful detached house villa garden Düsseldorf Germany professional real estate photography sunny day"
    },
    {
        "category": "Stadtteile",
        "emoji": "🏘️",
        "thema": "einen Düsseldorfer Stadtteil: Oberkassel, Pempelfort, Bilk, Flingern oder Gerresheim – Wohnqualität und Immobilienpreise",
        "bild_prompt": "Düsseldorf neighborhood street charming architecture old buildings Germany cityscape photography"
    },
    {
        "category": "Finanzierung",
        "emoji": "💶",
        "thema": "Finanzierungsoptionen und KfW-Förderungen für Immobilienkäufer in Düsseldorf",
        "bild_prompt": "modern office building glass facade Düsseldorf Germany architecture business district photography"
    },
    {
        "category": "Ratgeber",
        "emoji": "📊",
        "thema": "einen wichtigen Immobilien-Ratgeber-Tipp zu Energieausweis, Grunderwerbsteuer oder Notarkosten",
        "bild_prompt": "Düsseldorf Altstadt old town Rhine river waterfront architecture Germany photography golden hour"
    },
    {
        "category": "Vermietung",
        "emoji": "🏢",
        "thema": "Vermietung von Wohnungen in Düsseldorf – Mietrecht, Mietpreise, Tipps für Vermieter",
        "bild_prompt": "modern apartment building exterior Düsseldorf Germany contemporary architecture real estate"
    },
    {
        "category": "Ratgeber",
        "emoji": "🏗️",
        "thema": "Neubau vs. Bestandsimmobilien in Düsseldorf – was lohnt sich mehr",
        "bild_prompt": "new construction modern residential building Düsseldorf Germany architecture sunny day real estate"
    }
]

MONATE_DE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}


def datum_de(d):
    return f"{d.day}. {MONATE_DE[d.month]} {d.year}"


def generiere_bild_url(bild_prompt):
    seed = random.randint(1, 99999)
    encoded = urllib.parse.quote(bild_prompt)
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=900&height=500&nologo=true&model=flux&seed={seed}"
    )


def api_aufruf(prompt):
    # Pollinations Text API – kostenlos, kein API Key, kein Blocking
    encoded = urllib.parse.quote(prompt, safe='')
    seed = random.randint(1, 99999)
    url = f"https://text.pollinations.ai/{encoded}?model=openai-large&seed={seed}&json=true"

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; KrischerImmoBot/1.0)'}
    )

    print("Sende Anfrage an Pollinations Text API...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        text = resp.read().decode('utf-8').strip()
        print(f"Antwort erhalten ({len(text)} Zeichen)")
        return text


def generiere_artikel():
    thema = random.choice(THEMEN)
    heute = datetime.date.today()

    prompt = (
        f"Schreibe einen professionellen Immobilien-Blogartikel auf Deutsch für Krischer Immobilien aus Düsseldorf. "
        f"Thema: {thema['thema']}. "
        "Anforderungen: 350-420 Wörter, seriöser Ton, Bezug zu Düsseldorf, keine Preisversprechen oder Rechtsberatung, "
        "erwähne Krischer Immobilien einmal, origineller Text, Absätze mit Leerzeile trennen, "
        "Abschluss mit Kontaktaufforderung. "
        "Antworte NUR mit einem JSON-Objekt ohne weiteren Text: "
        "{\"title\": \"Titel max 68 Zeichen mit Düsseldorf\", "
        "\"excerpt\": \"Zusammenfassung ein Satz max 155 Zeichen\", "
        "\"content\": \"Vollständiger Text Absätze mit \\n\\n getrennt\", "
        "\"readTime\": \"4\"}"
    )

    raw = api_aufruf(prompt)

    # JSON extrahieren
    if '```' in raw:
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]
    raw = raw.strip()
    start = raw.find('{')
    end = raw.rfind('}') + 1
    raw = raw[start:end]

    artikel_daten = json.loads(raw)
    artikel_id = f"{heute.strftime('%Y%m%d')}-{random.randint(100, 999)}"

    return {
        "id": artikel_id,
        "date": datum_de(heute),
        "datetime": heute.isoformat(),
        "category": thema['category'],
        "emoji": thema['emoji'],
        "imageUrl": generiere_bild_url(thema['bild_prompt']),
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
