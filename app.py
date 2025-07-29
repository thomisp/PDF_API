import os
import uuid
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "API estilo PDF.co (con pdftotext)"

@app.route("/v1/pdf/extract/text", methods=["POST"])
def extract_text():
    user_key = request.headers.get("x-api-key")
    if not user_key or user_key != API_KEY:
        return jsonify({"status": "error", "message": "Invalid or missing API key"}), 403

    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    txt_path = filepath + ".txt"
    try:
        subprocess.run(["pdftotext", "-layout", filepath, txt_path], check=True)
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error extrayendo texto: {str(e)}"}), 500

    return jsonify({
        "status": "success",
        "pageCount": 1,
        "body": text,
        "url": ""
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
