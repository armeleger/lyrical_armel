from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")
GENIUS_API_URL = "https://api.genius.com"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/lyrics", methods=["GET"])
def get_lyrics():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    if not GENIUS_API_KEY:
        return jsonify({"error": "Server misconfiguration: Missing API key"}), 500

    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": query}

    try:
        response = requests.get(f"{GENIUS_API_URL}/search", headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        hits = data.get("response", {}).get("hits", [])
        if not hits:
            return jsonify({"error": "No lyrics found for your query"}), 404

        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({"error": "External API timeout"}), 504
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Genius API call failed: {e}")
        return jsonify({"error": "Failed to fetch from Genius"}), 500

if __name__ == "__main__":
    import sys
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port argument, using default 8080")
    app.run(host="0.0.0.0", port=port)