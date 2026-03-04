# Python HTTP Browser

Ein leichtgewichtiger HTTP Browser der über das Terminal bedient wird. Das Programm ermöglicht das Scrapen von HTML-Tags, das Senden von GET- und POST-Requests sowie das Anzeigen von Cookies einer Webseite.

Der Browser basiert auf **Selenium** mit einem **Firefox** Treiber im Headless-Modus. Damit läuft alles im Hintergrund ohne ein Browserfenster zu öffnen. Die Steuerung erfolgt vollständig über **CLI-Argumente** im POSIX-Standard (`--flag value`).

---

## Voraussetzungen

Python 3.x, Firefox und die benötigten Python-Pakete:

    pip install selenium

---

## Verwendung

In das Verzeichnis des Projekts wechseln und folgende Befehle verwenden:

### HTML-Tag scrapen

Gibt den Textinhalt eines bestimmten HTML-Tags einer Webseite aus.

    python browser.py scrape --url <url> --tag <tag>

**Beispiel:**

    python browser.py scrape --url https://example.com --tag h1

---

### GET Request mit Parametern

Sendet einen GET-Request mit einem Query-Parameter und gibt die Antwort aus.

    python browser.py get --url <url> --param <key=value>

**Beispiel:**

    python browser.py get --url https://httpbin.org/get --param name=johndoe

---

### POST Request (Formular)

Füllt ein Formular auf einer Webseite aus und sendet es ab.

    python browser.py post --url <url> --param <key=value> --param <key=value>

**Beispiel:**

    python browser.py post \
      --url https://httpbin.org/forms/post \
      --param custname=johndoe \
      --param custtel=0777777 \
      ...

---

### Cookies anzeigen

Zeigt alle Cookies einer Webseite an.

    python browser.py list-cookies --url <url>

**Beispiel:**

    python browser.py list-cookies --url https://google.com

---

## Befehlsliste

| Befehl         | Beschreibung                                      |
|----------------|---------------------------------------------------|
| `scrape`       | Textinhalt eines HTML-Tags ausgeben               |
| `get`          | GET-Request mit Query-Parameter senden            |
| `post`         | Formular ausfüllen und absenden (POST-Request)    |
| `list-cookies` | Alle Cookies einer Webseite anzeigen              |

---

## Feature Dokumentation

| Feature        | Datei       | Zeile |
|----------------|-------------|-------|
| scrape         | browser.py  | 49    |
| get            | browser.py  | 53    |
| post           | browser.py  | 57    |
| list-cookies   | browser.py  | 71    |
