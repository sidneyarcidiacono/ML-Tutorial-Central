"""Database models for SQLAlchemy."""
from flask_login import UserMixin
from tutorial_app import db

from tutorial_app.utils import FormEnum


class TutorialCategory(FormEnum):
    """Categories of grocery items."""

    ML = "Machine Learning"
    STATS = "Statistics"
    DL = "Deep Learning"
    RL = "Reinforcement Learning"
    OTHER = "Other"


class Difficulty(FormEnum):
    """Categories of grocery items."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(160), nullable=False)
    saved_tutorials = db.relationship(
        "Tutorial", secondary="saved_tutorials", back_populates="saved_by"
    )


class Tutorial(db.Model):
    """Tutorial model."""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(
        db.Enum(TutorialCategory), default=TutorialCategory.OTHER
    )
    title = db.Column(db.String(40), nullable=False)
    difficulty = db.Column(
        db.Enum(Difficulty), default=Difficulty.INTERMEDIATE
    )
    body = db.Column(db.String(10000), nullable=False)
    saved_by = db.relationship(
        "User",
        secondary="saved_tutorials",
        back_populates="saved_tutorials",
    )


class Resource(db.Model):
    """Resource model."""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(
        db.Enum(TutorialCategory), default=TutorialCategory.OTHER
    )
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    link = db.Column(db.String(120), nullable=False)


saved_tutorial_table = db.Table(
    "saved_tutorials",
    db.Column("tutorial_id", db.Integer, db.ForeignKey("tutorial.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)
