from flask import Blueprint, request, jsonify, send_file, current_app
from . import db
from .models import Document
from .utils import allowed_file, jwt_required, generate_token
import os
from werkzeug.utils import secure_filename
import uuid
from .cache import get_cached_documents, set_cached_documents, clear_document_cache

bp = Blueprint("api", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "admin":
        token = generate_token("admin_user")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/documents/upload", methods=["POST"])
@jwt_required
def upload():
    file = request.files.get("file")
    patient_id = request.form.get("patient_id")
    print(file)
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{file_id}.pdf")

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(path)

    doc = Document(
        id=file_id,
        filename=filename,
        file_path=path,
        size=os.path.getsize(path),
        patient_id=patient_id,
    )
    db.session.add(doc)
    db.session.commit()

    docs = Document.query.all()
    result = [{
        "id": d.id,
        "filename": d.filename,
        "size": d.size,
        "patient_id": d.patient_id,
        "created_at": d.created_at.isoformat()
    } for d in docs]

    set_cached_documents(result)

    return jsonify({"success": True, "id": file_id})


@bp.route("/documents", methods=["GET"])
@jwt_required
def list_docs():
    cached = get_cached_documents()
    if cached:
        return jsonify(cached)

    docs = Document.query.all()
    result = [{
        "id": d.id,
        "filename": d.filename,
        "size": d.size,
        "patient_id": d.patient_id,
        "created_at": d.created_at.isoformat()
    } for d in docs]

    set_cached_documents(result)
    return jsonify(result)


@bp.route("/documents/<id>/download", methods=["GET"])
@jwt_required
def download(id):
    doc = Document.query.get(id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404

    if not os.path.exists(doc.file_path):
        return jsonify({"error": "File not found on server"}), 404

    return send_file(
        doc.file_path,
        as_attachment=True,
        download_name=doc.filename
    )


@bp.route("/documents/<id>", methods=["DELETE"])
@jwt_required
def delete_doc(id):
    doc = Document.query.get(id)
    if not doc:
        return jsonify({"error": "Not found"}), 404

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.session.delete(doc)
    db.session.commit()

    docs = Document.query.all()
    result = [{
        "id": d.id,
        "filename": d.filename,
        "size": d.size,
        "patient_id": d.patient_id,
        "created_at": d.created_at.isoformat()
    } for d in docs]
    set_cached_documents(result)

    return jsonify({"success": True})
