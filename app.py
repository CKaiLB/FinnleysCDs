from flask import Flask, request, jsonify, send_from_directory, send_file, Response
from flask_cors import CORS
import os
import static.SpotifyScrape as SpotifyScrape
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from flask_talisman import Talisman

load_dotenv()
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")


app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

Talisman(app, force_https= True)

limiter= Limiter(
    app=app,
    key_func= get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def check_credentials(username, password):
    return USERNAME  == username and PASSWORD == password

def authenticate():
    return Response("Could not verify your super secret credentials. Either you're not Finnley or your password is wrong", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# Configuration for production
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

@app.route("/")
def serve_index():
    return send_file('index.html')

@app.route("/api/download", methods=["POST"])
@requires_auth
@limiter.limit("2 per minute")
def download():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        url = data.get("url")
        filename = data.get("filename")
        
        if not url or not filename:
            return jsonify({"error": "Missing URL or filename"}), 400
        
        # Download the playlist
        SpotifyScrape.download_spotify_playlist(url, filename)
        return jsonify({"message": "Download completed successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)  # Too Many Requests
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": str(e.description)
    }), 429

if __name__ == "__main__":
    # In production, you'll want to use a proper WSGI server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)