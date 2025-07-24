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

    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": query}

    response = requests.get(f"{GENIUS_API_URL}/search", headers=headers, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch from Genius"}), 500

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)