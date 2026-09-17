from flask import Blueprint, jsonify, request, session

from app import db
from app.models import UserSkill
from app.auth_helpers import api_login_required

skills_bp = Blueprint("skills", __name__)
VALID_PROFICIENCIES = ["Beginner", "Intermediate", "Advanced"]

def skill_to_dict(skill):
    """Convert a Skill object into a JSON-serializable dictionary."""
    return{
        "id": skill.id,
        "skill_name": skill.skill_name,
        "proficiency": skill.proficiency
    }

@skills_bp.route("/api/skills", methods=["GET"])
@api_login_required
def list_skills():
    """Return every skill as a JSON array."""
    skills = UserSkill.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([skill_to_dict(a) for a in skills])

@skills_bp.route("/api/skills", methods=["POST"])
@api_login_required
def add_skill():
    data = request.get_json()

    # Reject anything that isn't JSON - get_json() returnes None for non-JSON
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Pull the fields, defaulting to "" so .strip() never hits None
    skill_name = data.get("skill_name", "").strip()
    proficiency = data.get("proficiency", "").strip()

    if not skill_name or not proficiency:
        return jsonify({"error": "skill_name and proficiency are required"}), 400

    # Proficiency must be one of the allowed values - catch it here so the
    # client gets a clean 400 instead of the database raising a 500
    if proficiency not in VALID_PROFICIENCIES:
        return jsonify({"error": f"proficiency must be one of: {', '.join(VALID_PROFICIENCIES)}"}), 400

    # Create the skill, owned by the logged-in user
    skill = UserSkill(
        skill_name=skill_name,
        proficiency=proficiency,
        user_id=session["user_id"]
    )

    db.session.add(skill)
    db.session.commit()

    return jsonify(skill_to_dict(skill)), 201

@skills_bp.route("/api/skills/<int:skill_id>", methods=["GET"])
@api_login_required
def get_skill(skill_id):
    """Fetch a single skill by id, ensuring it belongs to the logged-in user."""
    skill = UserSkill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first()

    if skill is None:
        return jsonify({"error": "Skill not found"}), 404

    return jsonify(skill_to_dict(skill)), 200


@skills_bp.route("/api/skills/<int:skill_id>", methods=["DELETE"])
@api_login_required
def delete_skill(skill_id):
    """Delete skill by id"""
    skill = UserSkill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first()

    if skill is None:
        return jsonify({"error": "Skill not found"}), 404

    db.session.delete(skill)
    db.session.commit()

    return "", 204