# Lyrics Finder App

A simple web app that lets users search for lyrics by entering a song title and artist name. It uses the [Genius API](https://docs.genius.com/) to fetch lyrics, and features a lightweight, responsive design with a Flask backend.

---

**Docker Hub Image:** [armeleger/lyrics-finder-app](https://hub.docker.com/r/armeleger/lyrics-finder-app)

---

## Features

- Search for lyrics by song and artist
- Fast and responsive UI
- Genius API integration
- Backend built with Flask (Python)
- CORS-handled API requests
- Error handling for failed API lookups

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **API:** Genius API

---

## Local Development (Part One)

### 1. Install Requirements
Clone this repo, then run:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Provide API Key
Copy `.env.example` to `.env` and add your [Genius API](https://genius.com/developers) key:
```
GENIUS_API_KEY=your_key_here
```

### 3. Run App Locally
```
python3 app.py
```
Go to http://localhost:8080

---

## Docker Build & Run (Local Testing)

### 1. Build Image
```
docker build -t armeleger/lyrics-finder-app:v1 .
```

### 2. Run Container Locally
```
docker run --env-file .env -p 8080:8080 armeleger/lyrics-finder-app:v1
```
Check: [http://localhost:8080](http://localhost:8080)

---

## Deployment (Three-Node Setup)

### 1. Push Image to Docker Hub
```
docker login
# Tag only if needed
docker push armeleger/lyrics-finder-app:v1
```

### 2. Deploy App on Web01 & Web02
SSH into both servers, and on each run:
```sh
docker pull armeleger/lyrics-finder-app:v1
docker run -d --name lyrics_app --restart unless-stopped \
  --env-file /path/to/.env \
  -p 8080:8080 armeleger/lyrics-finder-app:v1
```

- Confirm reachability: `curl http://web-01:8080` and `curl http://web-02:8080`

### 3. Load Balancer (Lb01)

Edit `/etc/haproxy/haproxy.cfg` and add or update:
```cfg
backend webapps
  balance roundrobin
  server web01 172.20.0.11:8080 check
  server web02 172.20.0.12:8080 check
```
Then reload HAProxy:
```
docker exec -it lb-01 sh -c 'haproxy -sf $(pidof haproxy) -f /etc/haproxy/haproxy.cfg'
```

### 4. End-to-End Test
Run this from your workstation (repeat several times):
```sh
curl http://<load-balancer-address>:<port>
```
Check that results alternate (showing both web01 and web02 responding).

#### **Sample curl output:**
```sh
$ curl http://lb-01:8080
<html> ... LYRICAL ... </html>
```

---

## Handling Secrets
- Never commit `.env` or secrets to git.
- Pass credentials using `--env-file .env` or environment variables in `docker run`.
- Example: Add `/path/to/.env` with GENIUS_API_KEY to each server!

---

## Screenshots & Logs

Below are sample `curl` outputs and screenshot instructions to include:

```
curl -v http://web-01:8080
curl -v http://web-02:8080
curl -v http://<load-balancer-address>:8080
```

Include terminal screenshots or copy the above terminal log outputs here to demonstrate the responses change between `web-01` and `web-02`. (Paste images directly below if submitting a PDF/online repo, or commit .png files in a /screenshots folder and link them here.)

---

## Project Structure
lyrical_armel/
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .env.example

---

## API & Tools Credits
- [Genius API](https://docs.genius.com/) (lyrics data)
- Flask
- Docker

**License:** MIT © Kayisire Kira Armel Leger
