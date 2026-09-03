from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        """Hash and store a password. The plaintext is never saved."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

class UserSkill(db.Model):
    __tablename__ = "user_skills"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_name = db.Column(db.String(255), nullable=False)
    proficiency = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.CheckConstraint (
            "proficiency IN ('Beginner', 'Intermediate', 'Advanced')",
            name="proficiency_check"
        ),
    )
class Posting(db.Model):
    __tablename__ = "postings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class PostingSkill(db.Model):
    __tablename__ = "posting_skills"
    id = db.Column(db.Integer, primary_key=True)
    posting_id = db.Column(db.Integer, db.ForeignKey("postings.id"), nullable=False)
    skill_name = db.Column(db.String(255), nullable=False)
    is_required = db.Column(db.Boolean, nullable=False, default=False)