"""
TTB-A — Minimal Flask server for processing uploads.

Endpoints:
  GET  /       -> Serves the upload form 
  POST /upload -> Receives label image + application text

Requirements:
  pip install flask pillow anthropic
"""

import os
import traceback
import anthropic
import base64
from flask import Flask, request, redirect, url_for, send_file, jsonify
from PIL import Image

from flask_limiter import Limiter


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 
client = anthropic.Anthropic() 

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png"}
ALLOWED_TEXT_EXT = {".txt"}

# rate limit: 5 uploads per minute, 100 uploads per day per IP
def get_real_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

limiter = Limiter(get_real_ip, app=app, storage_uri="memory://")

# ── Serve the HTML form ─────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))


# ── Handle uploads ──────────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
@limiter.limit("5/minute;100/day")
def upload():
    print(f"Request from IP: {get_real_ip()}")
    try:
        label_file = request.files.get("label_image")
        app_file = request.files.get("application_info")

        if not label_file or not app_file:
            return jsonify({"status": "error", "analysis": "Both files are required."}), 400

        # Validate extensions
        label_ext = os.path.splitext(label_file.filename)[1].lower()
        app_ext = os.path.splitext(app_file.filename)[1].lower()

        if label_ext not in ALLOWED_IMAGE_EXT:
            return jsonify({"status": "error", "analysis": f"Invalid image type: {label_ext}"}), 400
        if app_ext not in ALLOWED_TEXT_EXT:
            return jsonify({"status": "error", "analysis": f"Invalid text type: {app_ext}"}), 400

        # Save files
        label_path = os.path.join(UPLOAD_DIR, "label" + label_ext)
        app_path = os.path.join(UPLOAD_DIR, "application.txt")

        label_file.save(label_path)
        app_file.save(app_path)

        # Process
        result = process_files(label_path, app_path)
        return jsonify(result)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "analysis": f"Server error: {str(e)}"}), 500



# ── processing function ─────────────────────────────────
def process_files(label_path: str, app_text_path: str) -> dict:

    # read the image as base64
    with open(label_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # media type
    ext = os.path.splitext(label_path)[1].lower()
    media_type = "image/png" if ext == ".png" else "image/jpeg"

    # 2. Read the txt file
    with open(app_text_path, "r", encoding="utf-8") as f:
        text_content = f.read()


    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"""TTB label compliance review.
                                APPLICATION:
                                {text_content}

                                Verify label against application for:
                                1. The Government Warning may appear in any orientation (horizontal or vertical).
                                    Minor spacing, line breaks, or punctuation differences are acceptable.
                                        All required words and both paragraphs (1) and (2) must be present in substance.
                                2. ABV matches ABV
                                3. BRAND matches BRAND
                                4. CLASS matches CLASS
                                5. NET matches NET
                                6. Name and address present on label (city and state are sufficient)

                                If all pass, output exactly:
                                APPROVED

                                If any fail, output exactly:
                                NEEDS REVISION:
                                - Item number - reason

                                Do not explain passed items.
                                """
                                ,
                    },
                ],
            }
        ],
    )

    
    return {
        "status": "success",
        "analysis": message.content[0].text,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))