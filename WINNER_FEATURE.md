# Gewinner-Feature für Spiele

## Übersicht

Für jedes Spiel gibt es nun einen neuen "Moderator-Bereich" mit der Möglichkeit, den Spielgewinner festzulegen und automatisch die entsprechenden Punkte zum Scoreboard hinzuzufügen.

## Neue Funktionen

### 1. **Gewinner-Buttons im Moderator-Bereich**

Auf jeder Spielseite (z.B. "Lets Dance") befindet sich nun der Moderator-Bereich mit zwei neuen Buttons:

- **✅ David gewinnt (X Punkte)** - David gewinnt das Spiel
- **✅ Gäste gewinnen (X Punkte)** - Die Gäste gewinnen das Spiel

Beispiel bei "Lets Dance" (6 Punkte):
- Wenn "David gewinnt" geklickt wird: 6 Punkte werden automatisch zu Davids Score addiert
- Wenn "Gäste gewinnen" geklickt wird: 6 Punkte werden automatisch zu den Gäste-Punkten addiert

### 2. **Automatische Punktvergabe**

- Der Moderator muss nur auf einen der Gewinner-Buttons klicken
- Ein Bestätigungs-Dialog zeigt die vergebenen Punkte
- Die Punkte werden sofort zum Scoreboard hinzugefügt
- Der Score kann jederzeit auf dem Scoreboard überprüft werden

### 3. **Layout der Moderator-Controls**

Der Moderator-Bereich ist nun strukturiert in:

1. **Gewinner festlegen:** Zwei große Buttons für David vs. Gäste
2. **Abstimmungen zurücksetzen:** Separate Sektion für das Reset-Button

## Technische Implementierung

### Backend (app.py)

Neue Route hinzugefügt:
```python
@app.route('/set_game_winner/<game_id>/<winner>', methods=['POST'])
def set_game_winner(game_id, winner):
    # Setzt den Gewinner und addiert Punkte automatisch
```

### Frontend (spiel.html)

- Neue HTML-Buttons mit Emoji-Icons
- Neue JavaScript-Funktion `setGameWinner()` für die API-Anfrage
- Bestätigungs-Dialog für Benutzerbestätigung

### Styling (style.css)

Neue CSS-Klassen für besseres Layout:
- `.moderator-control-group` - Gruppiert verwandte Controls
- Flexbox-Layout für responsive Anordnung
- Subtile Hintergrundfarben und Trennung der Kontrollen

## Ablauf während der Party

1. **Spiel wird gespielt**
2. **Gäste stimmen ab** (bestehend aus Voting-Buttons)
3. **Moderator sieht Abstimmungsergebnisse**
4. **Moderator klickt auf "David gewinnt" oder "Gäste gewinnen"**
5. **Punkte werden automatisch zu Scoreboard addiert**
6. ✅ **Fertig! Das Spiel ist abgeschlossen**

## Punkte pro Spiel

| Spiel | Punkte |
|-------|--------|
| Lets Dance | 6 |
| Lach doch mal! | 5 |
| Blind Artist | 4 |
| Wissensduell | 3 |
| Den Song kenn ich | 2 |
| Was kostet der Spaß? | 1 |

## Hinweise für den Moderator

- Die Punkte werden sofort addiert - keine zusätzliche Bestätigung nötig
- Ein Dialog zeigt die erfolgreiche Aktion
- Punkte können später im Scoreboard manuell angepasst werden (falls nötig)
- Abstimmungen können zurückgesetzt werden, um nochmal abzustimmen
