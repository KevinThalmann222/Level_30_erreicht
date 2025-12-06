I have a finished PowerPoint in German for a 30th birthday party with several mini-games for the guest of honor “David”. I now want to turn this PowerPoint into an interactive Python Flask web app.

Please generate a complete Flask project structure and example code that does the following:

1. General requirements
- Use Python + Flask (no Django).
- Use Jinja2 templates and Bootstrap (or simple custom CSS) for a clean, responsive layout that works well on a laptop + beamer.
- The whole UI (buttons, headings, labels, instructions) must be in German.
- Keep the code well structured: `app.py`, a `templates/` folder, a `static/` folder for CSS/JS/images.

2. Pages / routes
Create routes and templates for:
- A **Startseite** (`/`) with the title “David wird 30” and a navigation to all games.
- A **Spielübersicht** page listing all games with short descriptions.
- One separate page per game:
  - Spiel 1: „Lets Dance“ – 6 Punkte
  - Spiel 2: Lach doch mal!“ – 5 Punkte
  - Spiel 3: „Blind Artist“´– 4 Punkte
  - Spiel 4: „Wissensduell“ – 3 Punkte
  - Spiel 5: „Den Song kenn ich“ – 2 Punkte
  - Spiel 6: „Was kostet der Spaß?“ – 1 Punkt

Each game page should:
- Show the game title and the rules (in German) as text blocks.
- Display an image placeholder (I will later replace these with my own images).
- Have controls for the moderator (me) and interactive elements for the audience.

3. Interactivity / voting
I want the audience to be able to participate with simple voting from their phones.

Implement a minimal voting system using Flask + JavaScript (no external backend):
- Provide a route like `/vote/<game>/<option>` that accepts POST requests (or GET for simplicity).
- Provide buttons on each game page for the audience to vote, e.g.:
  - “David gewinnt”
  - “Gast gewinnt”
  - or “Unentschieden”
- For “Let’s Dance”, “Lach doch mal!”, “Den Song kenn ich!” and “Was kostet der Spaß?” the main interaction is audience voting who won.
- For “Wissensduell” the audience can vote which Seite (David vs. Team Publikum) they glauben, dass sie die aktuelle Runde gewonnen hat.
- The votes should be counted in memory (a simple in-memory dictionary is enough).
- On each game page show the **current vote results** live or after pressing a “Ergebnisse aktualisieren” button (you can use JS fetch/AJAX to reload the counts without reloading the full page).

4. Scoreboard
- Implement a simple global scoreboard (e.g. for David vs. Gäste).
- Store scores in a global structure or a simple `session`/in-memory store.
- Add a separate route `/scoreboard` with a big, clearly visible Anzeige:
  - Gesamtpunkte David
  - Gesamtpunkte Gäste
- Provide buttons to:
  - Add points to David or the guests after each game.
  - Reset all scores (with a confirmation).

5. Game flow helper
- Add a small “Nächste Runde / Nächstes Spiel” button on every game page that links to the next game’s route.
- The app should be easy to control by a single moderator on a laptop while the audience only uses their phones for voting.

6. Implementation hints
- Use German text for all labels, headings, buttons and game rules.
- Use clear, readable fonts and big buttons (party + beamer friendly).
- Comment the code so I can easily adapt the rules and labels later.

Please generate:
- `app.py` with all routes and logic
- Example templates in `templates/` (base.html, index.html, scoreboard.html, and one template per game)
- A minimal `static/style.css` for basic styling
- Short instructions in comments how to run the app with `flask run`.

Focus on getting a working prototype first; it does not need user authentication or a database.
