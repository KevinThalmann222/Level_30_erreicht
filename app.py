"""
Flask Web App für David's 30. Geburtstag - Partyspiele
=====================================================
Eine interaktive Web-Anwendung für Partyspiele mit Abstimmungssystem und Scoreboard.

Ausführung:
-----------
1. Stelle sicher, dass Flask installiert ist: pip install -r requirements.txt
2. Führe aus: python app.py
3. Öffne in deinem Browser: http://localhost:5000

Die App läuft auf deinem Laptop als Moderator.
Gäste können von ihren Telefonen aus unter der gleichen IP-Adresse abstimmen.

PRODUKTION:
-----------
Für Produktionsdeployment verwende einen WSGI-Server wie Gunicorn:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
import os
from werkzeug.utils import secure_filename
from uuid import uuid4
import logging

app = Flask(__name__)

# ========== SICHERHEITSKONFIGURATION ==========
# Secret key für Session-Management
app.secret_key = os.environ.get('SECRET_KEY', 'david_wird_30_secret_key_2025')

# Session-Konfiguration
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', False)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# Logging-Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== GEWINNSPIEL KONFIGURATION ==========
# Use absolute paths to ensure they work on PythonAnywhere and locally
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Stelle sicher, dass der Upload-Ordner existiert
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Prüft, ob die Datei ein erlaubtes Format hat."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== GLOBALE DATENSTRUKTUREN ==========

# Gewinnspiel-Bilder: {id: {filename, uploader_name, votes, upload_time}}
gewinnspiel_images = {}

# Abstimmungsergebnisse für jedes Spiel
votes = {
    'spiel1': {'david': 0, 'gast': 0, 'unentschieden': 0},
    'spiel2': {'david': 0, 'gast': 0, 'unentschieden': 0},
    'spiel3': {'david': 0, 'gast': 0, 'unentschieden': 0},
    'spiel4': {'david': 0, 'team': 0},
    'spiel5': {'david': 0, 'gast': 0, 'unentschieden': 0},
    'spiel6': {'david': 0, 'gast': 0, 'unentschieden': 0},
}

# Track who has voted for each game: {'spiel1': {'user_id_1', 'user_id_2', ...}, ...}
user_votes_tracker = {
    'spiel1': set(),
    'spiel2': set(),
    'spiel3': set(),
    'spiel4': set(),
    'spiel5': set(),
    'spiel6': set(),
}

# Track who has liked each image: {'image_id': {'user_id_1', 'user_id_2', ...}, ...}
image_likes_tracker = {}

# Scoreboard: Punkte pro Team
scores = {
    'david': 0,
    'gaeste': 0
}

# ========== EBAY KLEINANZEIGEN KONFIGURATION ==========
# Use absolute path to ensure it works on PythonAnywhere and local
EBAY_FOLDER = os.path.join(APP_ROOT, 'static', 'ebay')

# Ensure ebay folder exists
os.makedirs(EBAY_FOLDER, exist_ok=True)

ebay_images = []
current_ebay_image_id = 0
show_ebay_image = False

def load_ebay_images():
    """Lädt alle eBay-Bilder aus dem ebay-Ordner."""
    global ebay_images
    
    import re
    from pathlib import Path
    
    # Ensure folder exists
    ebay_path = Path(EBAY_FOLDER)
    os.makedirs(EBAY_FOLDER, exist_ok=True)
    
    ebay_images = []
    
    try:
        logger.info(f"Attempting to load eBay images from: {ebay_path.absolute()}")
        
        # List all files in the directory
        all_files = list(ebay_path.glob('*'))
        logger.info(f"Files in {EBAY_FOLDER}: {[f.name for f in all_files]}")
        
        for image_file in sorted(all_files):
            logger.info(f"Processing file: {image_file.name}")
            
            if image_file.is_file() and image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                filename_without_ext = image_file.stem
                logger.info(f"  Filename stem: {filename_without_ext}")
                
                # Try to extract price from filename
                price_match = re.search(r'(\d+(?:[.,]\d{2})?)', filename_without_ext)
                
                if price_match:
                    price_str = price_match.group(1).replace(',', '.')
                    logger.info(f"  Found price: {price_str}")
                    try:
                        price = float(price_str)
                        ebay_images.append({
                            'id': len(ebay_images),
                            'filename': image_file.name,
                            'price': price
                        })
                        logger.info(f"  ✓ Added to ebay_images: {image_file.name} (Price: {price}€)")
                    except ValueError as e:
                        logger.warning(f"  ✗ Failed to parse price '{price_str}': {e}")
                else:
                    logger.warning(f"  ✗ No price pattern found in '{filename_without_ext}'")
        
        logger.info(f"✅ Loaded {len(ebay_images)} eBay images from {EBAY_FOLDER}")
        if ebay_images:
            logger.info(f"   Images: {[img['filename'] for img in ebay_images]}")
    except Exception as e:
        logger.error(f"❌ Error loading eBay images: {e}", exc_info=True)

def get_current_ebay_image():
    """Gibt das aktuell aktive eBay-Bild zurück."""
    global current_ebay_image_id
    if 0 <= current_ebay_image_id < len(ebay_images):
        return ebay_images[current_ebay_image_id]
    return None

# Lade eBay-Bilder beim Start
load_ebay_images()

# Spieldefinitionen mit Informationen
games = [
    {
        'id': 'spiel1',
        'number': 1,
        'name': 'Lets Dance',
        'punkte': 6,
        'beschreibung': 'David und ein Gast treten in einem Tanzduell an. Die Zuschauer entscheiden, wer besser tanzt.',
        'regeln': ['David und ein Gast tanzen 30 Sekunden lang.', 'Die Zuschauer stimmen ab: Wer hat besser getanzt?', 'Der Gewinner erhält 6 Punkte für sein Team.'],
        'voting_options': [('david', 'David gewinnt'), ('gast', 'Gast gewinnt'), ('unentschieden', 'Unentschieden')]
    },
    {
        'id': 'spiel2',
        'number': 2,
        'name': 'Lach doch mal! – Die Lach-Challenge',
        'punkte': 5,
        'beschreibung': (
            'David wählt drei Gäste aus, die er in einer 60-Sekunden-Challenge '
            'zum Lachen bringen muss. Dabei darf er selbst nicht lachen. '
            'Mindestens zwei der drei ausgewählten Personen müssen lachen – '
            'und zusätzlich muss das Publikum mehrheitlich zustimmen, dass David '
            'lustig war.'
        ),
        'regeln': [
            'David wählt drei Gäste aus, die an der Lach-Challenge teilnehmen.',
            'David hat 60 Sekunden Zeit, um diese drei Personen zum Lachen zu bringen.',
            'Mindestens zwei der drei Teilnehmer müssen lachen, damit David überhaupt eine Chance auf den Sieg hat.',
            'David darf während der gesamten Challenge nicht lachen.',
            'Nach der Zeit stimmt das Publikum ab, ob sie Davids Performance lustig fanden.',
            'Nur wenn die Mehrheit des Publikums für David stimmt UND mindestens zwei Gäste gelacht haben, gewinnt David das Spiel.',
            'Falls diese Bedingungen nicht erfüllt werden, gewinnen die Gäste.'
        ],
        'voting_options': [
            ('david', 'David gewinnt'),
            ('gaeste', 'Die Gäste gewinnen'),
            ('unentschieden', 'Unentschieden / keine klare Mehrheit')
        ]
    },
    {
        'id': 'spiel3',
        'number': 3,
        'name': 'Blind Artist – Team Battle',
        'punkte': 4,
        'beschreibung': (
            'David wählt drei Gäste aus: Einen, der mit ihm im Team zeichnet, '
            'und zwei weitere, die das gegnerische Team bilden. In jedem Team '
            'hat eine Person die Augen verbunden und zeichnet, die andere Person '
            'muss den Begriff erraten.'
        ),
        'regeln': [
            'David wählt drei Gäste: eine Person für sein Team und zwei Personen als gegnerisches Team.',
            'In jedem Team hat eine Person die Augen verbunden (der/die Zeichner*in), die andere Person ist der/die Ratende.',
            'Jedes Team erhält heimlich einen eigenen Begriff, z. B. Team David: „Katze“, gegnerisches Team: „Hund“.',
            'Nur die Person mit verbundenen Augen bekommt den Begriff gesagt und muss ihn zeichnen – ohne zu sprechen.',
            'Die ratende Person darf Fragen stellen und Vermutungen äußern, der/die Zeichner*in antwortet nur mit Gesten (z. B. Kopfnicken oder Kopfschütteln).',
            'Gewonnen hat das Team, dessen ratende Person zuerst den richtigen Begriff errät.',
            'Optional: Nach der Runde können die Kunstwerke allen Gästen gezeigt und bejubelt werden.'
        ],
        'voting_options': [
            ('team_david', 'Team David gewinnt'),
            ('gegnerteam', 'Gegnerteam gewinnt'),
            ('unentschieden', 'Unentschieden / beide zu gut oder keiner errät es')
        ]
    },
    {
        'id': 'spiel4',
        'number': 4,
        'name': 'Wissensduell',
        'punkte': 3,
        'beschreibung': 'David gegen ein 3er Team seiner Wahl im Quiz-Duell. Wer kennt die Antworten?',
        'regeln': ['Es werden 3 Fragen gestellt.', 'David antwortet allein.', 'Das Team diskutiert und gibt eine gemeinsame Antwort.', 'Wer mehr richtige Antworten hat, gewinnt.'],
        'voting_options': [('david', 'David gewinnt'), ('team', 'Team Publikum gewinnt')]
    },
    {
        'id': 'spiel5',
        'number': 5,
        'name': 'Den Song kenn ich!',
        'punkte': 2,
        'beschreibung': (
            'David wählt eine Person aus dem Publikum aus und tritt gegen sie im Musikraten an. '
            'Es werden drei Runden gespielt. Wer einen Song zuerst richtig erkennt, bekommt den Punkt.'
        ),
        'regeln': [
            'David wählt eine Person aus dem Publikum als Gegner/in.',
            'Es werden insgesamt 3 Musik-Snippets abgespielt.',
            'Sobald ein Snippet läuft, dürfen beide sofort raten.',
            'Wer zuerst den richtigen Songtitel (oder klar erkennbaren Interpreten) nennt, erhält 1 Punkt.',
            'Nach drei Runden gewinnt die Person mit den meisten Punkten.',
            'Bei Gleichstand gibt es ein kurzes Stechen mit einem vierten Snippet.'
        ],
        'voting_options': [
            ('david', 'David gewinnt'),
            ('gast', 'Gast gewinnt'),
            ('unentschieden', 'Unentschieden / Stechen nötig')
        ]
    },
    {
        'id': 'spiel6',
        'number': 6,
        'name': 'Was kostet der Spaß?',
        'punkte': 1,
        'beschreibung': 'Schätzspiel: David und Gäste raten Preise. Wer ist am nächsten dran? Alle Gäste können teilnehmen!',
        'regeln': ['Verschiedene Gegenstände werden gezeigt.', 'Beide müssen den Preis schätzen.', 'Wer am nächsten am echten Preis liegt, erhält 1 Punkt.'],
        'voting_options': [('david', 'David gewinnt'), ('gast', 'Gast gewinnt'), ('unentschieden', 'Unentschieden')]
    }
]

# ========== HILFS-FUNKTIONEN ==========

def get_user_id():
    """Generiert oder holt eine eindeutige User ID aus der Session."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid4())
    return session['user_id']

def get_game_by_id(game_id):
    """Findet ein Spiel anhand seiner ID."""
    for game in games:
        if game['id'] == game_id:
            return game
    return None

def get_next_game(current_game_id):
    """Gibt das nächste Spiel zurück."""
    for i, game in enumerate(games):
        if game['id'] == current_game_id:
            if i + 1 < len(games):
                return games[i + 1]
    return None

def reset_votes_for_game(game_id):
    """Setzt die Abstimmungen für ein Spiel zurück."""
    if game_id in votes:
        for key in votes[game_id]:
            votes[game_id][key] = 0
    # Reset user votes tracker too
    if game_id in user_votes_tracker:
        user_votes_tracker[game_id].clear()

# ========== GEWINNSPIEL HELPER FUNKTIONEN ==========

def get_all_images_sorted():
    """Gibt alle Gewinnspiel-Bilder sortiert nach Votes (absteigend) zurück."""
    images_list = []
    for image_id, image_data in gewinnspiel_images.items():
        images_list.append({
            'id': image_id,
            'filename': image_data['filename'],
            'uploader_name': image_data['uploader_name'],
            'votes': image_data['votes'],
            'upload_time': image_data.get('upload_time', '')
        })
    # Sortiere nach Votes (absteigend)
    images_list.sort(key=lambda x: x['votes'], reverse=True)
    return images_list

def get_top_image():
    """Gibt das Bild mit den meisten Votes zurück (aktueller Spitzenreiter)."""
    images = get_all_images_sorted()
    if images:
        return images[0]
    return None

# ========== ROUTES: STARTSEITE UND NAVIGATION ==========

@app.route('/')
def index():
    """Startseite: David wird 30"""
    is_moderator = session.get('moderator_authenticated', False)
    return render_template('index.html', is_moderator=is_moderator)

@app.route('/spieluebersicht')
def spieluebersicht():
    """Übersicht aller Spiele."""
    is_moderator = session.get('moderator_authenticated', False)
    return render_template('spieluebersicht.html', games=games, is_moderator=is_moderator)

# ========== ROUTES: MODERATOR AUTHENTICATION ==========

@app.route('/moderator_login', methods=['POST'])
def moderator_login():
    """Moderator Login - setzt Session für alle Spiele."""
    password = request.json.get('password', '') if request.is_json else request.form.get('password', '')
    
    if password == '123':  # Moderator-Passwort
        session['moderator_authenticated'] = True
        session['ebay_moderator'] = True
        return jsonify({'success': True, 'message': 'Authentifiziert'})
    
    return jsonify({'success': False, 'error': 'Falsches Passwort'}), 401

@app.route('/moderator_logout', methods=['POST'])
def moderator_logout():
    """Moderator Logout - löscht Session."""
    session.pop('moderator_authenticated', None)
    session.pop('ebay_moderator', None)
    return jsonify({'success': True, 'message': 'Abgemeldet'})

# ========== ROUTES: SPIEL-SEITEN ==========

@app.route('/spiel/<game_id>')
def spiel(game_id):
    """Zeigt die Seite für ein spezifisches Spiel."""
    game = get_game_by_id(game_id)
    if not game:
        return "Spiel nicht gefunden", 404
    
    is_moderator = session.get('moderator_authenticated', False)
    
    # Spiel6 (Was kostet der Spaß?) nutzt ein eigenes Template mit eBay-Bildern
    if game_id == 'spiel6':
        return render_template('was_kostet_der_spass.html',
                             game=game,
                             votes=votes.get(game_id, {}),
                             next_game=get_next_game(game_id),
                             current_image=get_current_ebay_image(),
                             show_image=show_ebay_image,
                             ebay_images=ebay_images,
                             is_moderator=is_moderator)
    
    next_game = get_next_game(game_id)
    return render_template('spiel.html', 
                         game=game, 
                         votes=votes.get(game_id, {}),
                         next_game=next_game,
                         is_moderator=is_moderator)

# ========== ROUTES: VOTING-SYSTEM ==========

@app.route('/vote/<game_id>/<option>', methods=['POST', 'GET'])
def vote(game_id, option):
    """
    Registriert eine Abstimmung.
    Beispiel: /vote/spiel1/david
    Jeden Benutzer darf nur einmal pro Spiel abstimmen.
    """
    if game_id not in votes or option not in votes[game_id]:
        return jsonify({'success': False, 'message': 'Ungültige Abstimmung'}), 400
    
    user_id = get_user_id()
    
    # Check if user already voted for this game
    if user_id in user_votes_tracker[game_id]:
        return jsonify({
            'success': False, 
            'message': 'Du hast bereits für dieses Spiel abgestimmt!'
        }), 400
    
    # Record vote
    votes[game_id][option] += 1
    user_votes_tracker[game_id].add(user_id)
    
    return jsonify({
        'success': True,
        'message': f'Danke für deine Abstimmung!',
        'votes': votes[game_id]
    })

@app.route('/get_votes/<game_id>')
def get_votes(game_id):
    """Gibt die aktuellen Abstimmungsergebnisse zurück (JSON)."""
    if game_id in votes:
        return jsonify(votes[game_id])
    return jsonify({'error': 'Spiel nicht gefunden'}), 404

@app.route('/reset_votes/<game_id>', methods=['POST'])
def reset_votes(game_id):
    """Setzt die Abstimmungen für ein Spiel zurück (nur Moderator)."""
    reset_votes_for_game(game_id)
    return jsonify({'success': True, 'message': 'Abstimmungen zurückgesetzt'})

@app.route('/set_game_winner/<game_id>/<winner>', methods=['POST'])
def set_game_winner(game_id, winner):
    """
    Setzt den Gewinner eines Spiels und addiert die Punkte automatisch.
    winner: 'david' oder 'gaeste'
    """
    game = get_game_by_id(game_id)
    if not game:
        return jsonify({'success': False, 'message': 'Spiel nicht gefunden'}), 404
    
    if winner not in ['david', 'gaeste']:
        return jsonify({'success': False, 'message': 'Ungültiger Gewinner'}), 400
    
    # Addiere die Punkte zum Gewinner
    points = game['punkte']
    if winner == 'david':
        scores['david'] += points
    else:
        scores['gaeste'] += points
    
    return jsonify({
        'success': True,
        'message': f'{winner} hat {points} Punkte gewonnen!',
        'scores': scores
    })

# ========== ROUTES: SCOREBOARD ==========

@app.route('/scoreboard')
def scoreboard():
    """Zeigt das Scoreboard mit Punktestand."""
    is_moderator = session.get('moderator_authenticated', False)
    return render_template('scoreboard.html', scores=scores, games=games, is_moderator=is_moderator)

@app.route('/get_scores')
def get_scores():
    """Gibt die aktuellen Punkte zurück (JSON)."""
    return jsonify(scores)

@app.route('/add_points/<team>/<int:punkte>', methods=['POST'])
def add_points(team, punkte):
    """
    Fügt Punkte hinzu.
    team: 'david' oder 'gaeste'
    punkte: positive oder negative Zahl
    """
    if team in scores:
        scores[team] += punkte
        if scores[team] < 0:
            scores[team] = 0
        return jsonify({
            'success': True,
            'scores': scores
        })
    return jsonify({'success': False}), 400

@app.route('/reset_scores', methods=['POST'])
def reset_scores():
    """Setzt alle Punkte zurück."""
    scores['david'] = 0
    scores['gaeste'] = 0
    return jsonify({'success': True, 'scores': scores})

# ========== HILFSFUNKTIONEN FÜR TEMPLATES ==========

@app.route('/debug_ebay_images')
def debug_ebay_images():
    """Debug endpoint to check eBay images loaded."""
    return jsonify({
        'ebay_folder': EBAY_FOLDER,
        'ebay_images_count': len(ebay_images),
        'ebay_images': ebay_images,
        'current_image': get_current_ebay_image(),
        'show_image': show_ebay_image
    })

@app.template_filter('totalpunkte')
def total_punkte_filter(game_list):
    """Berechnet die Gesamtpunkzahl aller Spiele."""
    return sum(game['punkte'] for game in game_list)

# ========== ROUTES: GEWINNSPIEL ==========

@app.route('/gewinnspiel')
def gewinnspiel():
    """Zeigt die Gewinnspiel-Seite mit Upload und Galerie."""
    is_moderator = session.get('moderator_authenticated', False)
    images = get_all_images_sorted()
    top_image = get_top_image()
    return render_template('gewinnspiel.html', 
                         images=images,
                         top_image=top_image,
                         is_moderator=is_moderator)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Verarbeitet den Image Upload.
    Erwartet: 'image' (Datei) und 'uploader_name' (Text)
    """
    try:
        # Prüfe, ob die Datei vorhanden ist
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Keine Datei ausgewählt'}), 400
        
        file = request.files['image']
        uploader_name = request.form.get('uploader_name', 'Anonym').strip()
        
        if not uploader_name:
            uploader_name = 'Anonym'
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Keine Datei ausgewählt'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Nur JPG, PNG und GIF erlaubt'}), 400
        
        # Prüfe Dateigröße
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        if file_length > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': 'Datei zu groß (Max: 5 MB)'}), 400
        
        # Generiere einen eindeutigen Dateinamen
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid4().hex}.{file_ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Speichere die Datei
        file.save(filepath)
        
        # Speichere Metadaten
        image_id = str(uuid4())
        gewinnspiel_images[image_id] = {
            'filename': unique_filename,
            'uploader_name': uploader_name,
            'votes': 0,
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'success': True,
            'message': 'Bild erfolgreich hochgeladen!',
            'image_id': image_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/vote_image/<image_id>', methods=['POST', 'GET'])
def vote_image(image_id):
    """
    Registriert eine Abstimmung für ein Bild.
    Jeden Benutzer darf nur einmal pro Bild abstimmen.
    """
    if image_id not in gewinnspiel_images:
        return jsonify({'success': False, 'error': 'Bild nicht gefunden'}), 404
    
    user_id = get_user_id()
    
    # Initialize likes tracker for this image if not exists
    if image_id not in image_likes_tracker:
        image_likes_tracker[image_id] = set()
    
    # Check if user already liked this image
    if user_id in image_likes_tracker[image_id]:
        return jsonify({
            'success': False,
            'error': 'Du hast bereits für dieses Bild abgestimmt!'
        }), 400
    
    # Record like
    gewinnspiel_images[image_id]['votes'] += 1
    image_likes_tracker[image_id].add(user_id)
    
    return jsonify({
        'success': True,
        'message': 'Danke für deine Abstimmung!',
        'votes': gewinnspiel_images[image_id]['votes']
    })

@app.route('/get_images')
def get_images():
    """Gibt alle Bilder als JSON zurück (für AJAX)."""
    images = get_all_images_sorted()
    return jsonify({
        'success': True,
        'images': images,
        'top_image': get_top_image()
    })

# ========== ERROR HANDLER ==========

@app.errorhandler(404)
def not_found(error):
    """Behandelt 404-Fehler."""
    return render_template('404.html'), 404

# ========== HAUPTPROGRAMM ==========

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   David's 30. Geburtstag - Partyspiele Web-App        ║
    ╚════════════════════════════════════════════════════════╝
    
    🎉 Die App läuft unter: http://localhost:5000
    
    Tipp: 
    - Auf dem Moderator-Laptop: http://localhost:5000
    - Für Gäste: http://<deine-ip>:5000 (z.B. http://192.168.1.100:5000)
    
    Drücke Ctrl+C zum Beenden.
    """)

# ========== ROUTES: EBAY IMAGE CONTROLS ==========

@app.route('/ebay_show_image/<int:image_id>', methods=['POST'])
def ebay_show_image(image_id):
    """Zeigt ein eBay-Bild an (nur Moderator)."""
    global current_ebay_image_id, show_ebay_image
    
    if not session.get('moderator_authenticated', False):
        return jsonify({'success': False, 'error': 'Nicht autorisiert'}), 403
    
    if 0 <= image_id < len(ebay_images):
        current_ebay_image_id = image_id
        show_ebay_image = True
        return jsonify({'success': True, 'message': 'Bild angezeigt'})
    
    return jsonify({'success': False, 'error': 'Ungültige Bild-ID'}), 400

@app.route('/ebay_hide_image', methods=['POST'])
def ebay_hide_image():
    """Versteckt das eBay-Bild (nur Moderator)."""
    global show_ebay_image
    
    if not session.get('moderator_authenticated', False):
        return jsonify({'success': False, 'error': 'Nicht autorisiert'}), 403
    
    show_ebay_image = False
    return jsonify({'success': True, 'message': 'Bild versteckt'})

# ========== MAIN ==========

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   David's 30. Geburtstag - Partyspiele Web-App        ║
    ╚════════════════════════════════════════════════════════╝
    
    🎉 Die App läuft unter: http://localhost:5000
    
    Tipp: 
    - Auf dem Moderator-Laptop: http://localhost:5000
    - Für Gäste: http://<deine-ip>:5000 (z.B. http://192.168.1.100:5000)
    
    Drücke Ctrl+C zum Beenden.
    
    PRODUKTIONSHINWEIS:
    - Für Production verwende: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    """)
    
    # Development vs Production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    debug_mode = not is_production and os.environ.get('FLASK_DEBUG', True)
    
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Flask App Start - Production: {is_production}, Debug: {debug_mode}")
    
    # Starte den Flask Development Server
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        threaded=True
    )
