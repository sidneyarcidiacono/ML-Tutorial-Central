"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# from grocery_app.models import GroceryStore, GroceryItem
# from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm
# from grocery_app import app, db

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    """Return landing page."""
    return render_template("index.html")


@main.route("/")
def contribute():
    """Add new tutorial or resource to the site."""
    return render_template("contribute.html")
