"""Main forms."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    FloatField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, URL
from tutorial_app.models import (
    Tutorial,
    Resource,
    TutorialCategory,
    Difficulty,
)


class TutorialForm(FlaskForm):
    """Form for adding/updating a Tutorial."""

    category = SelectField(
        "Category",
        choices=TutorialCategory.choices(),
        validators=[DataRequired()],
    )
    title = StringField("Title", validators=[DataRequired(), Length(max=80)])
    difficulty = SelectField(
        "Difficulty",
        choices=Difficulty.choices(),
        validators=[DataRequired()],
    )
    body = TextAreaField(
        "Content", validators=[DataRequired(), Length(min=5)]
    )
    submit = SubmitField("Submit")


class ResourceForm(FlaskForm):
    """Form for adding/updating a Resource."""

    category = SelectField(
        "Category",
        choices=TutorialCategory.choices(),
        validators=[DataRequired()],
    )
    title = StringField("Title", validators=[DataRequired(), Length(max=80)])
    description = TextAreaField("Description", validators=[Length(max=350)])
    link = StringField(
        "Link", validators=[DataRequired(), URL(), Length(max=300)]
    )
    submit = SubmitField("Submit")
