from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re
import io

app = Flask(__name__)
CORS(app)

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route("/transcript", methods=["POST"])
def transcript():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript])
        return jsonify({"transcript": transcript_text})
    except Exception as e:
        print(f"Transcript fetch error: {e}")
        return jsonify({"error": "Transcript not available for this video."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
