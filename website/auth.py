from flask import Blueprint, request, session, jsonify
from .models import db, User
import logging

from . import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user_exist = User.query.filter_by(email=email).first() is not None

    if user_exist:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Incorrect password"}), 401

        session["user_id"] = user.id

        return jsonify({
            "id": user.id,
            "email": user.email
        }), 200

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({"error": "An error occurred during login"}), 500
