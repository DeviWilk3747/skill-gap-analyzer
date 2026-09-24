from flask import Blueprint, jsonify, request, session

from app import db
from app.models import User

# Authentication routes: register, login, logout
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must be JSON"}), 400
    
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Checks whether the user's password is a valid input
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    elif not any(char.isupper() for char in password):
        return jsonify({"error": "Password must contain at least one uppercase letter"}), 400

    elif not any(char.islower() for char in password):
        return jsonify({"error": "Password must contain at least one lowercase letter."}), 400

    elif not any(char.isdigit() for char in password):
        return jsonify({"error": "Password must contain at least one number"}), 400

    # Emails are stored lowecase so the same address can't register twice under different capitalization
    email = email.lower()

    # Reject duplicate registrations
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "An account with that email already exists."}), 400

    # Create the user. set_password hashes - plaintext is never stored
    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error occured"}), 500

    # Log them in by storing their ID in the signed session cookie
    session["user_id"] = user.id

    return jsonify({"success": "Account created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request must be JSON"}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    user = User.query.filter_by(email=email.lower()).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user.id
    return jsonify({"success": "Logged in successfully."}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": "Logout successful."}), 200

@auth_bp.route("/api/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "Not logged in"}), 401

    user = db.session.get(User, user_id)
    return jsonify({"id": user.id, "email": user.email}), 200
    
