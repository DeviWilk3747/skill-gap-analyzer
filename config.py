import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ["DATABASE_URL"]
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cross-site cookies for the deployed frontend. Only enabled in production,
    # since SECURE cookies require HTTPS abd would break local http dev.
    if os.environ.get("PRODUCTION"):
        SESSION_COOKIE_SAMESITE = "None"
        SESSION_COOKIE_SECURE = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")
    TESTING = True