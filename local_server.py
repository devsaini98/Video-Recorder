from flask import Flask, request, jsonify, render_template
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Videos folder
VIDEO_FOLDER = Path(r"C:\Users\saanu\Desktop\Video Recorder\videos")

# Folder automatically create hoga
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"video_{timestamp}.webm"

    filepath = VIDEO_FOLDER / filename

    # Save video
    video.save(filepath)

    print(f"✅ Video saved: {filepath}")

    return jsonify({
        "success": True,
        "message": "Video successfully PC mein save ho gayi.",
        "filename": filename
    })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print("===================================")
    print("🎥 LOCAL VIDEO RECORDER")
    print("===================================")
    print(f"Saving videos to: {VIDEO_FOLDER}")
    print("Server: http://127.0.0.1:5001")
    print("===================================")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )