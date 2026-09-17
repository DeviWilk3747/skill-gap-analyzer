import pytest 

from app import create_app, db
from app.models import User
from config import TestConfig

@pytest.fixture
def app():
    """Create an application instance backed by test database.
    
    Tables are created and dropped in their own app contexts so no session
    is holding a connection DROP TABLE runs.
    """
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client that can make requests without running server."""
    return app.test_client()

@pytest.fixture
def user(app):
    """Create a user in the test database and return its id."""
    with app.app_context():
        u = User(email="test@example.com")
        u.set_password("TestPass123")
        db.session.add(u)
        db.session.commit()
        return u.id

@pytest.fixture
def auth_client(client, user):
    """A test client that is already logged in as the test user.
    
    The 'user' fixture is required so the account exists before we log in,
    even though its return value isn't used here.
    """
    client.post("/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    return client

@pytest.fixture
def other_user(app):
    """A second user, for testing that data is isolated between accounts."""
    with app.app_context():
        user = User(email="other@example.com")
        user.set_password("OtherPass123")
        db.session.add(user)
        db.session.commit()
        return user.id

@pytest.fixture
def other_client(app, other_user):
    """A seperate test client logged in as the second user."""
    client = app.test_client()
    client.post("/login", json={
        "email": "other@example.com",
        "password": "OtherPass123"
    })

    return client