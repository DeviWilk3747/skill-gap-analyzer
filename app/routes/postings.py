from flask import Blueprint, jsonify, request, session

from app import db
from app.models import Posting, PostingSkill
from app.auth_helpers import api_login_required
from app.extraction import extract_skills

postings_bp = Blueprint("postings", __name__)

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