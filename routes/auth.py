from functools import wraps

import jwt
from flask import Blueprint, current_app, g, jsonify, request
from flask_bcrypt import Bcrypt

from app import db
from models import User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_bp.record_once
def on_load(state):
    bcrypt.init_app(state.app)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(email=email, password=pw_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered", "user_id": user.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "invalid credentials"}), 401

    payload = {"user_id": user.id, "email": user.email}
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({"token": token}), 200


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing or malformed token"}), 401

        token = auth_header[len("Bearer "):]
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "user not found"}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated
