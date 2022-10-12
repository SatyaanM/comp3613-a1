from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def to_json(self):
        return {"id": self.id, "username": self.username}

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Reviewer(User):
    __tablename__ = "reviewer"
    reviews = db.relationship(
        "Review", backref="reviewer", lazy=True, cascade="all, delete-orphan"
    )

    def is_admin(self):
        return False


class Admin(User):
    __tablename__ = "admin"
    info = db.Column(db.String(120), nullable=True)

    def is_admin(self):
        return True
