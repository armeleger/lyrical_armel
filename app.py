from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GENIUS_API_TOKEN = 'TiNR-fh7XS6EwGRmTZkznvB65LGU-DYgGAgUwVGd4JkI85m8tsN1EbH1BV5zkU0S'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    artist = data.get('artist')
    title = data.get('title')
    headers = {
        'Authorization': f'Bearer {GENIUS_API_TOKEN}'
    }
    query = f'{title} {artist}'
    url = f'https://api.genius.com/search?q={query}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        hits = json_data['response']['hits']
        if hits:
            song_info = hits[0]['result']
            return jsonify({
                'full_title': song_info['full_title'],
                'url': song_info['url'],
                'thumbnail': song_info['song_art_image_thumbnail_url']
            })
    return jsonify({'error': 'Lyrics not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)