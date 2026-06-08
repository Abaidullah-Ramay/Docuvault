from flask import Blueprint, jsonify

from app import db
from models import Document, User

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/export", methods=["GET"])
def export():
    docs = db.session.query(Document, User).join(User, Document.owner_id == User.id).all()
    return jsonify([
        {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at.isoformat(),
            "owner_id": user.id,
            "owner_email": user.email,
        }
        for doc, user in docs
    ]), 200
