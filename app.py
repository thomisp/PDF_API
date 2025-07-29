from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "API estilo PDF.co activa"

@app.route("/v1/pdf/extract/text", methods=["POST"])
def extract_text():
    # 1) Validación de archivo
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    # opcional: renombrar con UUID para evitar colisiones
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    # 2) Abrir PDF y extraer texto por página
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Cannot open PDF: {str(e)}"}), 500

    pages = []
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        pages.append({
            "page": i,
            "text": text
        })
    page_count = len(pages)
    doc.close()

    # 3) (Opcional) Si quieres subir el .txt a un storage y devolver URL,
    #    aquí podrías implementarlo; dejamos vacío para imitar PDF.co.
    return jsonify({
        "status": "success",
        "pageCount": page_count,
        "body": pages,
        "url": ""
    })

if __name__ == "__main__":
    # Render asigna el puerto con la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
