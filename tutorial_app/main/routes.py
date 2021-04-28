"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from tutorial_app.main.forms import TutorialForm, ResourceForm
from tutorial_app.models import Tutorial, Resource, User

# from grocery_app.models import GroceryStore, GroceryItem
# from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm
# from grocery_app import app, db

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    """Return landing page."""
    return render_template("index.html")


@main.route("/new_resource", methods=["GET", "POST"])
@login_required
def new_resource():
    """Add new tutorial or resource to the site."""
    form = ResourceForm()
    return render_template("new_resource.html", form=form)


@main.route("/new_tutorial", methods=["GET", "POST"])
@login_required
def new_tutorial():
    """Add new tutorial or resource to the site."""
    form = TutorialForm()
    return render_template("new_tutorial.html", form=form)


@main.route("/resources")
def resources():
    """See list of resources and descriptions."""
    # Resources won't have a details page
    # All resources have a short description and an external link
    return render_template("resources.html")


@main.route("/tutorials")
def all_tutorials():
    """See or search through all available tutorials."""
    # TODO: Maybe integrate this with homepage?
    # TODO: each tutorial will have a detail page where you can
    # see and work through all the content
    return render_template("tutorials_list.html")
