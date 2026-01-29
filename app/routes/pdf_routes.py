from flask import Blueprint, jsonify, request
from app.extensions.mongo import get_db
from bson import ObjectId
import os

pdf_bp = Blueprint("pdf", __name__, url_prefix="/pdf")

from flask import request, jsonify
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from app.extensions.mongo import get_db

db = get_db()

UPLOAD_FOLDER = "uploads"

@pdf_bp.route("/upload/pdf", methods=["POST"])
def upload_pdf():
    # 1️⃣ Validate file
    if "pdf" not in request.files:
        return jsonify({"message": "No file sent"}), 400

    file = request.files["pdf"]
    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({"message": "User ID missing"}), 400

    if file.filename == "":
        return jsonify({"message": "Empty filename"}), 400

    # 2️⃣ Save file
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 3️⃣ Save metadata to DB
    db.uploads.insert_one({
        "user_id": ObjectId(user_id),
        "filename": filename,
        "path": filepath
    })

    # 4️⃣ RETURN RESPONSE (THIS WAS MISSING)
    return jsonify({"message": "PDF uploaded successfully"}), 201


# 📌 READ – list PDFs
from bson import ObjectId
from flask import jsonify
from app.extensions.mongo import get_db

db = get_db()

@pdf_bp.route("/list/<user_id>", methods=["GET"])
def list_pdfs(user_id):
    try:
        uploads = db.uploads.find({"user_id": ObjectId(user_id)})

        result = []
        for u in uploads:
            result.append({
                "_id": str(u["_id"]),
                "filename": u.get("filename"),
                "path": u.get("path")
            })

        return jsonify(result), 200

    except Exception as e:
        print("❌ PDF LIST ERROR:", e)
        return jsonify({"message": "Failed to load PDFs"}), 500



# ✏️ UPDATE – rename PDF
@pdf_bp.route("/rename/<pdf_id>", methods=["PUT"])
def rename_pdf(pdf_id):
    data = request.get_json()
    new_name = data.get("filename")

    if not new_name:
        return jsonify({"message": "Filename required"}), 400

    db = get_db()
    db.uploads.update_one(
        {"_id": ObjectId(pdf_id)},
        {"$set": {"filename": new_name}}
    )

    return jsonify({"message": "PDF renamed successfully"}), 200


# 🗑 DELETE – delete PDF
@pdf_bp.route("/delete/<pdf_id>", methods=["DELETE"])
def delete_pdf(pdf_id):
    db = get_db()
    pdf = db.uploads.find_one({"_id": ObjectId(pdf_id)})

    if not pdf:
        return jsonify({"message": "PDF not found"}), 404

    # delete file from disk
    if os.path.exists(pdf["path"]):
        os.remove(pdf["path"])

    # delete metadata
    db.uploads.delete_one({"_id": ObjectId(pdf_id)})

    return jsonify({"message": "PDF deleted successfully"}), 200




