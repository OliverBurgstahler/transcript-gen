from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

app = Flask(__name__)
CORS(app)

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except:
        return None

@app.route("/")
def index():
    # Serve index.html from the same folder as main.py
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), "index.html")

@app.route("/transcript", methods=["POST"])
def transcript():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    transcript_text = get_transcript(video_id)
    if not transcript_text:
        return jsonify({"error": "Transcript not found"}), 404

    return jsonify({
        "transcript": transcript_text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # for deployment platforms or default 5000
    app.run(host="0.0.0.0", port=port)
