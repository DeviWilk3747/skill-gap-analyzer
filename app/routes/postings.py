from flask import Blueprint, jsonify, request, session

from app import db
from app.models import Posting, PostingSkill, UserSkill
from app.auth_helpers import api_login_required
from app.extraction import extract_skills
from app.scoring import score_posting
from collections import Counter

postings_bp = Blueprint("postings", __name__)


# Converters turn SQLAlchemy objects into plain dicts so jsonify can serialize
# them — jsonify only handles dicts, lists, and primitives, not model instances.
def posting_to_dict(posting):
    return {
        "id": posting.id,
        "title": posting.title,
        "company": posting.company,
        "raw_text": posting.raw_text,
        "created_at": posting.created_at.isoformat()  # datetime isn't JSON-safe on its own
    }


def posting_skill_to_dict(posting_skill):
    return {
        "id": posting_skill.id,
        "skill_name": posting_skill.skill_name,
        "is_required": posting_skill.is_required
    }


@postings_bp.route("/api/postings", methods=["POST"])
@api_login_required
def create_posting():
    """Create a posting, extract its skills, and store both."""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title", "").strip()
    company = data.get("company", "").strip()
    raw_text = data.get("raw_text", "").strip()

    if not title or not company or not raw_text:
        return jsonify({"error": "title, company, and raw_text are required"}), 400

    posting = Posting(
        title=title,
        company=company,
        raw_text=raw_text,
        user_id=session["user_id"]  # stamp ownership with the logged-in user
    )

    # Commit first so the database assigns posting.id — the skill rows below
    # need that id as their foreign key.
    db.session.add(posting)
    db.session.commit()

    skill_names = extract_skills(raw_text)

    for name in skill_names:
        posting_skill = PostingSkill(
            posting_id=posting.id,
            skill_name=name,
            is_required=False  # required-vs-optional detection isn't built yet
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
    """List the user's postings, each with its extracted skill names.

    The 'skills' key must match the shape create_posting returns, so the
    frontend can rely on posting.skills existing either way.
    """
    postings = Posting.query.filter_by(user_id=session["user_id"]).all()

    result = []
    for posting in postings:
        skills = PostingSkill.query.filter_by(posting_id=posting.id).all()
        posting_skill_names = [s.skill_name for s in skills]

        posting_dict = posting_to_dict(posting)
        posting_dict["skills"] = posting_skill_names
        result.append(posting_dict)

    return jsonify(result)


@postings_bp.route("/api/postings/<int:posting_id>", methods=["GET"])
@api_login_required
def single_posting(posting_id):
    """Return one posting with its skills and a match score for the user."""
    # Scoped by user_id so a user can't read someone else's posting by guessing
    # the id. 404 (not 403) so we don't reveal that the id exists.
    posting = Posting.query.filter_by(
        id=posting_id,
        user_id=session["user_id"]
    ).first()

    if posting is None:
        return jsonify({"error": "Posting not found"}), 404

    skills = PostingSkill.query.filter_by(posting_id=posting.id).all()
    user_skills = UserSkill.query.filter_by(user_id=session["user_id"]).all()

    posting_skill_names = [s.skill_name for s in skills]
    user_skill_names = [s.skill_name for s in user_skills]

    result = posting_to_dict(posting)
    result["skills"] = [posting_skill_to_dict(s) for s in skills]
    result["score"] = score_posting(posting_skill_names, user_skill_names)
    return jsonify(result)

@postings_bp.route("/api/postings/<int:posting_id>", methods=["DELETE"])
@api_login_required
def delete_posting(posting_id):
    """Delete posting by id"""
    posting = Posting.query.filter_by(
        id=posting_id,
        user_id=session["user_id"]
    ).first()

    if posting is None:
        return jsonify({"error": "Posting not found"}), 404

    # Delete the child skill rows first — the foreign key constraint blocks
    # deleting a posting while PostingSkill rows still reference it.
    PostingSkill.query.filter_by(posting_id=posting.id).delete()
    
    db.session.delete(posting)
    db.session.commit()

    return "", 204

@postings_bp.route("/api/gaps", methods=["GET"])
@api_login_required
def get_gaps():
    """Across all the user's postings, count the skills they're missing.

    Answers: which skills come up most often in jobs I want but don't have?
    """
    postings = Posting.query.filter_by(user_id=session["user_id"]).all()
    posting_ids = [p.id for p in postings]

    # One query for every skill across all the user's postings, rather than
    # querying per-posting in a loop.
    posting_skills = PostingSkill.query.filter(
        PostingSkill.posting_id.in_(posting_ids)
    ).all()

    # A set for O(1) membership checks when filtering out what the user has.
    user_skills = UserSkill.query.filter_by(user_id=session["user_id"]).all()
    user_skill_set = {s.skill_name for s in user_skills}

    missing = []
    for ps in posting_skills:
        if ps.skill_name not in user_skill_set:
            missing.append(ps.skill_name)

    # Counter tallies occurrences; most_common() returns them sorted, high to low.
    counts = Counter(missing)

    result = [
        {"skill": name, "count": count}
        for name, count in counts.most_common()
    ]

    return jsonify(result)