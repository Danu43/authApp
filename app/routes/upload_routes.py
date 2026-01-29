import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.extensions.mongo import get_db

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

UPLOAD_FOLDER = "uploads/pdfs"
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"message": "No file sent"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Only PDF files allowed"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    db = get_db()
    db.uploads.insert_one({
        "filename": filename,
        "path": file_path
    })

    return jsonify({"message": "PDF uploaded successfully"}), 201
