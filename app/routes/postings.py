from flask import Blueprint, jsonify, request, session

from app import db
from app.models import Posting, PostingSkill
from app.auth_helpers import api_login_required
from app.extraction import extract_skills

postings_bp = Blueprint("postings", __name__)

def posting_to_dict(posting):
    return{
        "id": posting.id,
        "title": posting.title,
        "company": posting.company,
        "raw_text": posting.raw_text,
        "created_at": posting.created_at.isoformat()
    }

def posting_skill_to_dict(posting_skill):
    return{
        "id": posting_skill.id,
        "skill_name": posting_skill.skill_name,
        "is_required": posting_skill.is_required
    }

@postings_bp.route("/api/postings", methods=["POST"])
@api_login_required
def create_posting():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title", "").strip()
    company = data.get("company", "").strip()
    raw_text = data.get("raw_text", "").strip()

    if not title or not company or not raw_text:
        return jsonify({"error": "title, company, and raw_text is required"}), 400

    # Create the posting, owned by logged-in user
    posting = Posting(
        title=title,
        company=company,
        raw_text=raw_text,
        user_id=session["user_id"]
    )

    db.session.add(posting)
    db.session.commit()

    skill_names = extract_skills(raw_text)

    for name in skill_names:
        posting_skill = PostingSkill(
            posting_id=posting.id,
            skill_name=name,
            is_required=False
        )
        db.session.add(posting_skill)
    db.session.commit()

    return jsonify({
        "id": posting.id,
        "title": posting.title,
        "company": posting.company,
        "skills": skill_names
    }), 201

@postings_bp.route("/api/postings", methods=["GET"])
@api_login_required
def list_postings():
    postings = Posting.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([posting_to_dict(a) for a in postings])

@postings_bp.route("/api/postings/<int:posting_id>", methods=["GET"])
@api_login_required
def single_posting(posting_id):
    posting = Posting.query.filter_by(
        id=posting_id,
        user_id=session["user_id"]
    ).first()

    if posting is None:
            return jsonify({"error": "Posting not found"}), 404

    skills = PostingSkill.query.filter_by(posting_id=posting.id).all()


    result = posting_to_dict(posting)
    result["skills"] = [posting_skill_to_dict(s) for s in skills]
    return jsonify(result)