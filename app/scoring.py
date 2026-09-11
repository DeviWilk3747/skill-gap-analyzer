def score_posting(posting_skills, user_skills):
    """Compare a posting's skills against a user's profile.
    
    Returns a dict with the match score, the matched skills, and the missing skills.
    """

    posting_set = set(posting_skills)
    user_set = set(user_skills)

    matched = posting_set & user_set
    missing = posting_set - user_set

    total = len(posting_set)
    if total == 0:
        return {"score": 0, "matched": [], "missing": [], "total": 0}

    score = round(len(matched) / total * 100)

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
        "total": total
    }