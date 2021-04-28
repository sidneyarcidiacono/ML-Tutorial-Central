"""Database models for SQLAlchemy."""
from flask_login import UserMixin
from tutorial_app import db


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(160), nullable=False)
