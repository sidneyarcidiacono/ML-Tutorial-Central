"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from tutorial_app.main.forms import TutorialForm, ResourceForm
from tutorial_app.models import Tutorial, Resource, User

from tutorial_app import db

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
            description=form.description.data,
        )
        db.session.add(resource)
        db.session.commit()
        flash("Thank you for sharing your new resource!")
        return redirect(url_for("main.resources"))
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
        return redirect(
            url_for("main.tutorial_details", tutorial_id=tutorial.id)
        )
    return render_template("new_tutorial.html", form=form)


@main.route("/resources")
def resources():
    """See list of resources."""
    # Resources won't have a details page
    # All resources have a short description and an external link
    resources = Resource.query.all()
    return render_template("resources.html", resources=resources)


@main.route("/resources/delete/<resource_id>")
@login_required
def delete_resource(resource_id):
    """Delete resource by id."""
    # We also have the poor "real world" case of anyone logged in
    # being able to delete a resource, but for our MVP that's fine
    resource = Resource.query.get(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash("Resource successfully deleted!")
    return redirect(url_for("main.resources"))


@main.route("/tutorials/<tutorial_id>")
def tutorial_details(tutorial_id):
    """View tutorial content."""
    # In the future it would be nice if users could track their progress!
    tutorial = Tutorial.query.get(tutorial_id)
    return render_template("tutorial_detail.html", tutorial=tutorial)


@main.route("/tutorials/edit/<tutorial_id>", methods=["GET", "POST"])
@login_required
def edit_tutorial(tutorial_id):
    """Edit tutorial details."""
    # Even though this isn't a perfect "real world" approach, for now anyone can
    # edit a tutorial
    tutorial = Tutorial.query.get(tutorial_id)
    form = TutorialForm(obj=tutorial)
    if form.validate_on_submit():
        tutorial.title = form.title.data
        tutorial.category = form.category.data
        tutorial.difficulty = form.difficulty.data
        tutorial.body = form.body.data
        db.session.commit()
        flash("Tutorial has been successfully updated.")
        return redirect(
            url_for("main.tutorial_details", tutorial_id=tutorial.id)
        )
    return render_template("edit_tutorial.html", form=form, tutorial=tutorial)


@main.route("/tutorials/delete/<tutorial_id>")
@login_required
def delete_tutorial(tutorial_id):
    """Delete tutorial."""
    # We also have the poor "real world" case of anyone logged in
    # being able to delete a tutorial, but for our MVP that's fine
    tutorial = Tutorial.query.get(tutorial_id)
    db.session.delete(tutorial)
    db.session.commit()
    flash("Tutorial successfully deleted!")
    return redirect(url_for("main.homepage"))
