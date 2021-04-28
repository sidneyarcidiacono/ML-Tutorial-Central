"""Main routes."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)
from flask_login import login_required, current_user, logout_user, login_user
from tutorial_app.auth.forms import SignInForm, SignUpForm
from tutorial_app.models import User

from tutorial_app import app, db, bcrypt


auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign in user."""
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(
                next_page if next_page else url_for("main.homepage")
            )
    return render_template("signin.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up new user."""
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created.")
        print("created")
        return redirect(url_for("auth.signin"))
    return render_template("signup.html", form=form)


@auth.route("/signout")
@login_required
def signout():
    """Sign out user."""
    logout_user()
    return redirect(url_for("main.homepage"))
