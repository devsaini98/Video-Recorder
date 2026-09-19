from flask import Flask, render_template, request, jsonify
from pathlib import Path
from datetime import datetime
import os

app = Flask(__name__)

# ==========================================
# VIDEO STORAGE
# ==========================================
# Render par /var/data persistent disk ka path hai.
# Local PC par videos folder use hoga.

if os.path.exists("/var/data"):
    VIDEO_FOLDER = Path("/var/data/videos")
else:
    VIDEO_FOLDER = Path("videos")

VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# VIDEO UPLOAD
# ==========================================

@app.route("/upload", methods=["POST"])
def upload_video():

    if "video" not in request.files:
        return jsonify({
            "success": False,
            "message": "Video file nahi mili."
        }), 400

    video = request.files["video"]

    if video.filename == "":
        return jsonify({
            "success": False,
            "message": "Video file empty hai."
        }), 400

    # Unique filename
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    filename = f"video_{timestamp}.webm"

    filepath = VIDEO_FOLDER / filename

    # Save video
    video.save(filepath)

    print(f"✅ Video saved: {filepath}")

    return jsonify({
        "success": True,
        "message": "Video successfully save ho gayi.",
        "filename": filename
    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    print("================================")
    print("🎥 VIDEO RECORDER SERVER")
    print("================================")
    print(f"Video folder: {VIDEO_FOLDER}")
    print(f"Port: {port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )