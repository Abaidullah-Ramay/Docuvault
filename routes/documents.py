import requests
from flask import Blueprint, g, jsonify, request

from app import db
from models import Document
from routes.auth import token_required

documents_bp = Blueprint("documents", __name__)


def _doc_json(doc):
    return {
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "owner_id": doc.owner_id,
        "created_at": doc.created_at.isoformat(),
    }


@documents_bp.route("", methods=["POST"])
@token_required
def create_document():
    data = request.get_json()
    doc = Document(
        title=data["title"],
        content=data["content"],
        owner_id=g.current_user.id,
    )
    db.session.add(doc)
    db.session.commit()
    return jsonify(_doc_json(doc)), 201


@documents_bp.route("", methods=["GET"])
@token_required
def list_documents():
    docs = Document.query.filter_by(owner_id=g.current_user.id).all()
    return jsonify([_doc_json(d) for d in docs]), 200


@documents_bp.route("/<int:id>", methods=["GET"])
@token_required
def get_document(id):
    doc = Document.query.get(id)
    if not doc:
        return jsonify({"error": "not found"}), 404
    return jsonify(_doc_json(doc)), 200


@documents_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_document(id):
    doc = Document.query.get(id)
    if not doc:
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    doc.title = data["title"]
    doc.content = data["content"]
    db.session.commit()
    return jsonify(_doc_json(doc)), 200


@documents_bp.route("/search", methods=["GET"])
@token_required
def search_documents():
    keyword = request.args.get("q", "")
    sql = "SELECT * FROM document WHERE title LIKE '%" + keyword + "%' OR content LIKE '%" + keyword + "%'"
    results = db.engine.execute(sql)
    docs = [{"id": r[0], "title": r[1], "content": r[2], "owner_id": r[3], "created_at": str(r[4])} for r in results]
    return jsonify(docs), 200


@documents_bp.route("/import", methods=["POST"])
@token_required
def import_document():
    data = request.get_json()
    url = data["url"]
    title = data.get("title", url)
    response = requests.get(url, timeout=10)
    content = response.text
    doc = Document(title=title, content=content, owner_id=g.current_user.id)
    db.session.add(doc)
    db.session.commit()
    return jsonify(_doc_json(doc)), 201


@documents_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_document(id):
    doc = Document.query.get(id)
    if not doc:
        return jsonify({"error": "not found"}), 404
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200
