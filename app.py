from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")
GENIUS_API_URL = "https://api.genius.com"

@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")

    if not artist or not song:
        return jsonify({"error": "Missing artist or song parameter"}), 400

    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    search_url = f"{GENIUS_API_URL}/search"
    params = {"q": f"{artist} {song}"}

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to connect to Genius API"}), 500

    data = response.json()
    hits = data["response"]["hits"]
    if not hits:
        return jsonify({"error": "No results found"}), 404

    # Get the first result
    song_data = hits[0]["result"]
    song_url = song_data["url"]

    return jsonify({
        "title": song_data["title"],
        "artist": song_data["primary_artist"]["name"],
        "url": song_url
    })

if __name__ == "__main__":
    app.run(debug=True)