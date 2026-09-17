def test_skills_required_login(client):
    """Unauthenticated requests are rejected with 401"""
    response = client.get("/api/skills")
    assert response.status_code == 401

def test_skills_empty_for_new_user(auth_client):
    """A user starts with empty skill list"""
    response = auth_client.get("/api/skills")
    assert response.status_code == 200
    assert response.get_json() == []

def test_adding_skill(auth_client):
    """A user is able to add a skill"""
    response = auth_client.post("/api/skills", json={
        "skill_name": "Python",
        "proficiency": "Beginner"
    })

    assert response.status_code == 201

    data = response.get_json()
    assert data["skill_name"] == "Python"
    assert data["proficiency"] == "Beginner"

def test_rejects_invalid_proficiency(auth_client):
    """Unrecognized proficiency should be rejected with 400"""

    response = auth_client.post("/api/skills", json={
        "skill_name": "JavaScript",
        "proficiency": "Expert"
    })

    assert response.status_code == 400
    assert "proficiency" in response.get_json()["error"]

def test_create_posting_extracts_skills(auth_client):
    response = auth_client.post("/api/postings", json={
        "title": "Backend Engineer",
        "company": "Acme",
        "raw_text": "We need Python and Docker"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "Python" in data["skills"]
    assert "Docker" in data["skills"]

def test_reflect_user_score_to_profile(auth_client):
    """Add a skill, create a posting that needs that skill plus others,
      fetch the single posting, and assert the score is what you expect.
      """
    response = auth_client.post("/api/skills", json={
        "skill_name": "Python",
        "proficiency": "Advanced"
    })
    assert response.status_code == 201

    data = response.get_json()

    response = auth_client.post("/api/postings", json={
        "title": "Backend Engineer",
        "company": "Amazon",
        "raw_text": "Looking for Python and Java"
    })
    posting_id = response.get_json()["id"]
    response = auth_client.get(f"/api/postings/{posting_id}")

    data = response.get_json()
    assert data["score"]["score"] == 50

def test_user_cannot_see_another_users_skills(auth_client, other_client):
    """Skills created by one user must not be visible to another."""
    response = other_client.post("/api/skills", json={
        "skill_name": "Python",
        "proficiency": "Beginner"
    })
    assert response.status_code == 201
    other_id = response.get_json()["id"]

    # The first user's list should not include it
    response = auth_client.get("/api/skills")
    assert response.status_code == 200
    assert response.get_json() == []

    # And fetching it directly should look like it doesn't exist
    response = auth_client.get(f"/api/skills/{other_id}")
    assert response.status_code == 404