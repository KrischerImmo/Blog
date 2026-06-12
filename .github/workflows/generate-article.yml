import json
import urllib.request
import urllib.parse
import urllib.error
import datetime
import random
import os
import sys

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
if not GEMINI_API_KEY:
    print("FEHLER: GEMINI_API_KEY ist nicht gesetzt")
    sys.exit(1)

print(f"API Key vorhanden: {GEMINI_API_KEY[:6]}...")

ARTIKEL_DATEI = 'articles.json'

THEMEN = [
    {
        "category": "Marktbericht",
        "emoji": "🏙️",
        "thema": "den aktuellen Immobilienmarkt in Duesseldorf – Preise, Nachfrage, Trends und Ausblick",
        "bild_prompt": "Düsseldorf skyline Rhine Tower modern city architecture aerial view professional real estate photography"
    },
    {
        "category": "Kaufen",
        "emoji": "🔑",
        "thema": "praktische Tipps und haeufige Fehler beim Kauf einer Immobilie in Duesseldorf",
        "bild_prompt": "modern luxury apartment interior Düsseldorf Germany bright living room real estate photography"
    },
    {
        "category": "Verkaufen",
        "emoji": "📋",
        "thema": "wie man eine Immobilie in Duesseldorf erfolgreich und zum besten Preis verkauft",
        "bild_prompt": "beautiful detached house villa garden Düsseldorf Germany professional real estate photography sunny day"
    },
    {
        "category": "Stadtteile",
        "emoji": "🏘️",
        "thema": "einen Duesseldorfer Stadtteil: Oberkassel, Pempelfort, Bilk, Flingern oder Gerresheim",
        "bild_prompt": "Düsseldorf neighborhood street charming architecture old buildings Germany cityscape photography"
    },
    {
        "category": "Finanzierung",
        "emoji": "💶",
        "thema": "Finanzierungsoptionen und KfW-Foerderungen fuer Immobilienkaeaeufer in Duesseldorf",
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
        "thema": "Vermietung von Wohnungen in Duesseldorf – Mietrecht, Mietpreise, Tipps fuer Vermieter",
        "bild_prompt": "modern apartment building exterior Düsseldorf Germany contemporary architecture real estate"
    }
]

MONATE_DE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}

MODELLE = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro-latest",
]


def datum_de(d):
    return f"{d.day}. {MONATE_DE[d.month]} {d.year}"


def generiere_bild_url(bild_prompt):
    seed = random.randint(1, 99999)
    encoded = urllib.parse.quote(bild_prompt)
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=900&height=500&nologo=true&model=flux&seed={seed}"
    )


def api_aufruf(modell, prompt):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 1400
        }
    }).encode('utf-8')

    for version in ["v1", "v1beta"]:
        url = (
            f"https://generativelanguage.googleapis.com/{version}/models/"
            f"{modell}:generateContent?key={GEMINI_API_KEY}"
        )
        print(f"Versuche: {version}/models/{modell}")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                print(f"Erfolgreich mit {version}/models/{modell}")
                return result
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            print(f"  Fehler {e.code}: {body[:300]}")
            continue
        except Exception as e:
            print(f"  Fehler: {e}")
            continue

    return None


def generiere_artikel():
    thema = random.choice(THEMEN)
    heute = datetime.date.today()

    prompt = (
        "Schreibe einen professionellen Immobilien-Blogartikel auf Deutsch "
        "fuer Krischer Immobilien aus Duesseldorf.\n\n"
        f"Thema: {thema['thema']}\n\n"
        "Anforderungen:\n"
        "- Laenge: 350-420 Woerter\n"
        "- Ton: serioeus, kompetent, lokaler Bezug zu Duesseldorf\n"
        "- Keine konkreten Preisversprechen oder Rechtsberatung\n"
        "- Erwaehne Krischer Immobilien einmal natuerlich im Text\n"
        "- Origineller Text\n"
        "- Abschluss mit Kontaktaufforderung\n\n"
        "Antworte NUR mit einem JSON-Objekt:\n"
        '{"title": "Titel max 68 Zeichen mit Duesseldorf", '
        '"excerpt": "Zusammenfassung max 155 Zeichen", '
        '"content": "Vollstaendiger Text Absaetze mit \\n\\n getrennt", '
        '"readTime": "4"}'
    )

    result = None
    for modell in MODELLE:
        result = api_aufruf(modell, prompt)
        if result:
            break

    if not result:
        print("FEHLER: Alle Modelle fehlgeschlagen")
        sys.exit(1)

    raw = result['candidates'][0]['content']['parts'][0]['text'].strip()

    if '```' in raw:
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]
    raw = raw.strip()

    # JSON-Bereich extrahieren
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
