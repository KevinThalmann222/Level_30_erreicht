# 🎉 David's 30. Geburtstag - Interaktive Partyspiele Web-App

Eine Flask-basierte Web-Anwendung für interaktive Partyspiele zum 30. Geburtstag von David. Moderator auf dem Laptop, Gäste stimmen von ihren Handys ab!

## 📋 Inhaltsverzeichnis

- [Features](#features)
- [Installation & Ausführung](#installation--ausführung)
- [Projektstruktur](#projektstruktur)
- [Benutzung](#benutzung)
- [Spiele-Übersicht](#spiele-übersicht)
- [Anpassungen](#anpassungen)

## ✨ Features

✅ **6 interaktive Partyspiele** mit individuellen Regeln  
✅ **Live-Abstimmungssystem** - Gäste stimmen von ihren Handys ab  
✅ **Echtzeit-Ergebnisanzeige** mit Live-Updates  
✅ **Scoreboard** - Verwalte Punkte für David vs. Gäste  
✅ **Responsive Design** - Funktioniert auf Laptop, Tablet und Smartphone  
✅ **Beamer-freundlich** - Große Schriften und klare Buttons  
✅ **Vollständig auf Deutsch** - Alle Texte in deutscher Sprache  
✅ **Ohne externe Abhängigkeiten** - Nur Flask, keine Datenbank nötig  

## 🚀 Installation & Ausführung

### Schritt 1: Python und Flask

Stelle sicher, dass Python 3.8+ installiert ist. Flask wurde bereits installiert.

### Schritt 2: App starten

Öffne ein Terminal/PowerShell im Projektordner und führe aus:

```powershell
python app.py
```

Du solltest eine Ausgabe wie diese sehen:

```
╔════════════════════════════════════════════════════════╗
║   David's 30. Geburtstag - Partyspiele Web-App        ║
╚════════════════════════════════════════════════════════╝

🎉 Die App läuft unter: http://localhost:5000

Tipp: 
- Auf dem Moderator-Laptop: http://localhost:5000
- Für Gäste: http://<deine-ip>:5000 (z.B. http://192.168.1.100:5000)

Drücke Ctrl+C zum Beenden.
```

### Schritt 3: Im Browser öffnen

- **Moderator (Laptop):** Öffne `http://localhost:5000`
- **Gäste (Handys):** Öffne `http://192.168.1.XX:5000` (ersetze XX mit deiner IP-Adresse)

Um deine IP-Adresse zu finden:
```powershell
ipconfig
# Suche nach "IPv4-Adresse" in der Ausgabe (z.B. 192.168.1.100)
```

## 📁 Projektstruktur

```
Level_30_erreicht/
├── app.py                          # Haupt-Flask-App mit allen Routes
├── templates/                       # HTML-Templates (Jinja2)
│   ├── base.html                   # Basis-Template mit Navigation
│   ├── index.html                  # Startseite
│   ├── spieluebersicht.html        # Übersicht aller Spiele
│   ├── spiel.html                  # Template für jedes Spiel
│   ├── scoreboard.html             # Scoreboard & Punkteverwaltung
│   └── 404.html                    # Fehlerseite
├── static/                          # Statische Dateien
│   └── style.css                   # Responsive CSS-Styling
├── pptx_extracted/                 # Extrahierte PPT-Dateien (optional)
└── README.md                        # Diese Datei
```

## 🎮 Benutzung

### Für den Moderator (Laptop)

1. **Startseite** (`/`) - Navigiere zu "Alle Spiele anschauen"
2. **Spielübersicht** (`/spieluebersicht`) - Wähle ein Spiel aus
3. **Spiel-Seite** (`/spiel/<game_id>`) 
   - Lies die Regeln vor
   - Starte das Spiel mit den Gästen
   - Sehe die **Live-Abstimmungsergebnisse** in Echtzeit
   - Klicke "🔄 Abstimmungen zurücksetzen" um eine neue Runde zu starten
4. **Scoreboard** (`/scoreboard`)
   - Verwalte die Punkte nach jedem Spiel
   - Nutze die Buttons um Punkte zu vergeben
   - Zeige den aktuellen Spielstand auf dem Beamer

### Für die Gäste (Handys)

1. Öffne die gleiche URL auf deinem Handy
2. Navigiere zu einem Spiel
3. Drücke einen der Abstimmungs-Buttons: "David gewinnt", "Gast gewinnt" oder "Unentschieden"
4. Die Ergebnisse werden live angezeigt!

## 🎮 Spiele-Übersicht

### Spiel 1: Lets Dance 🕺 (6 Punkte)
- **Beschreibung:** David und ein Gast tanzen gegeneinander
- **Abstimmung:** Wer tanzt besser?
- **Regeln:** 30 Sekunden Tanzduell, Publikum entscheidet

### Spiel 2: Lach doch mal! 😂 (5 Punkte)
- **Beschreibung:** David versucht, einen Gast zum Lachen zu bringen
- **Abstimmung:** Wer gewinnt?
- **Regeln:** David darf nicht selbst lachen, 60 Sekunden Zeit

### Spiel 3: Blind Artist 🎨 (4 Punkte)
- **Beschreibung:** Blindfolded zeichnen
- **Abstimmung:** Wer malt besser?
- **Regeln:** 2 Minuten, Augen verbunden, Publikum bewertet

### Spiel 4: Wissensduell 🧠 (3 Punkte)
- **Beschreibung:** David vs. Team Publikum Quiz
- **Abstimmung:** Wer kennt die Antworten besser?
- **Regeln:** 5 Fragen, David allein vs. Publikum

### Spiel 5: Den Song kenn ich 🎵 (2 Punkte)
- **Beschreibung:** Musikraten-Duell
- **Abstimmung:** Wer ist schneller?
- **Regeln:** 5 Musik-Snippets, schneller antworter gewinnt

### Spiel 6: Was kostet der Spaß? 💰 (1 Punkt)
- **Beschreibung:** Preisschätzspiel
- **Abstimmung:** Wer schätzt am genauesten?
- **Regeln:** Gegenstände zeigen, Preise schätzen, genauester gewinnt

## ✏️ Anpassungen

### Spielregeln ändern

Öffne `app.py` und suche nach der `games`-Liste:

```python
games = [
    {
        'id': 'spiel1',
        'name': 'Lets Dance',
        'punkte': 6,
        'beschreibung': 'Hier kannst du die Beschreibung ändern',
        'regeln': [
            'Regel 1 hier ändern',
            'Regel 2 hier ändern',
        ],
        # ...
    },
    # ... weitere Spiele
]
```

### Spiele-Namen ändern

```python
'name': 'Mein neuer Spiel-Name',
```

### Punkte pro Spiel ändern

```python
'punkte': 10,  # Ändere die Zahl
```

### Abstimmungsoptionen anpassen

```python
'voting_options': [
    ('option_id', 'Anzeige-Text'),
    ('david', 'David gewinnt'),
    ('gast', 'Gast gewinnt'),
]
```

### Farben anpassen

Öffne `static/style.css` und bearbeite die `:root` Variablen:

```css
:root {
    --primary-color: #ff6b6b;      /* Rot */
    --secondary-color: #4ecdc4;    /* Türkis */
    --success-color: #51cf66;      /* Grün */
    --warning-color: #ffd93d;      /* Gelb */
    --danger-color: #ff6348;       /* Orange */
}
```

### Bilder hinzufügen

1. Speichere deine Bilder im Ordner `static/images/`
2. Bearbeite `templates/spiel.html`:

```html
<img src="{{ url_for('static', filename='images/spiel1.png') }}" alt="Spiel 1">
```

Ersetze `spiel1.png` mit deinem Dateinamen.

## 🔧 Troubleshooting

### "Port 5000 wird bereits verwendet"

Ändere den Port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Ändere 5000 zu 8080
```

### Gäste können sich nicht verbinden

1. Stelle sicher, dass Moderator-Laptop und Gäste-Handys im **gleichen Wi-Fi-Netzwerk** sind
2. Überprüfe deine IP-Adresse mit `ipconfig`
3. Nutze `http://192.168.x.x:5000` (nicht `localhost`)
4. Überprüfe die Firewall

### Template-Fehler

Stelle sicher, dass alle Dateien in den richtigen Ordnern sind:
- Templates müssen im Ordner `templates/` sein
- CSS/JS müssen im Ordner `static/` sein

## 📝 Lizenz

Dieses Projekt ist für Davids 30. Geburtstagsfest gedacht! 🎂

---

**Viel Spaß beim Feiern!** 🎉🎊

Bei Fragen oder Problemen: Einfach die Kommentare in `app.py` lesen!
