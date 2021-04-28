"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from tutorial_app.main.forms import TutorialForm, ResourceForm
from tutorial_app.models import Tutorial, Resource, User

from tutorial_app import db

# TODO: enable user to keep a list of their saved tutorials
# TODO: enable user to track their own progress?

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    """Return landing page with list of tutorials."""
    tutorials = Tutorial.query.all()
    return render_template("index.html", tutorials=tutorials)


@main.route("/new_resource", methods=["GET", "POST"])
@login_required
def new_resource():
    """Add new tutorial or resource to the site."""
    form = ResourceForm()

    if form.validate_on_submit():
        resource = Resource(
            category=form.category.data,
            title=form.title.data,
            link=form.link.data,
        )
        db.session.add(resource)
        db.session.commit()
        flash("Thank you for sharing your new resource!")
        redirect(url_for("main.resources"))
    return render_template("new_resource.html", form=form)


@main.route("/new_tutorial", methods=["GET", "POST"])
@login_required
def new_tutorial():
    """Add new tutorial or resource to the site."""
    form = TutorialForm()

    if form.validate_on_submit():
        tutorial = Tutorial(
            category=form.category.data,
            title=form.title.data,
            difficulty=form.difficulty.data,
            body=form.body.data,
        )
        db.session.add(tutorial)
        db.session.commit()
        flash("Thank you for adding this tutorial!")
        redirect(url_for("main.tutorial_details", tutorial_id=tutorial.id))
    return render_template("new_tutorial.html", form=form)


@main.route("/resources")
def resources():
    """See list of resources and descriptions."""
    # Resources won't have a details page
    # All resources have a short description and an external link
    resources = Resource.query.all()
    return render_template("resources.html", resources=resources)


@main.route("/tutorials/<tutorial_id>")
def tutorial_details(tutorial_id):
    """View tutorial content."""
    # In the future it would be nice if users could track their progress!
    return render_template("tutorial_detail.html")
