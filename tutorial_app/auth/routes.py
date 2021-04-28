"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from tutorial_app.auth.forms import SignInForm, SignUpForm

# from grocery_app.models import GroceryStore, GroceryItem
# from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm
# from grocery_app import app, db

auth = Blueprint("auth", __name__)


@auth.route("/signin")
def signin():
    """Sign in user."""
    form = SignInForm()
    return render_template("signin.html", form=form)


@auth.route("/signup")
def signup():
    """Sign up new user."""
    form = SignUpForm()
    return render_template("signup.html", form=form)
