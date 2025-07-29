import os
import uuid
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Carga la API Key de la variable de entorno
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "API estilo PDF.co activa"

@app.route("/v1/pdf/extract/text", methods=["POST"])
def extract_text():
    # 1) Verificar API Key
    user_key = request.headers.get("x-api-key")
    if not user_key or user_key != API_KEY:
        return jsonify({"status": "error", "message": "Invalid or missing API key"}), 403

    # 2) Validación de archivo
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    # 3) Extraer texto
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Cannot open PDF: {str(e)}"}), 500

    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""  
        pages.append({"page": i, "text": text})
    doc.close()
    page_count = len(pages)


    # 4) Responder igual que PDF.co
    return jsonify({
        "status": "success",
        "pageCount": page_count,
        "body": pages,
        "url": ""
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
