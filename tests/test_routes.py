import os
import tempfile

import pytest

from tutorial_app import app
from tutorial_app.models import User, Resource, Tutorial


@pytest.fixture
def client():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def signin(client, username, password):
    return client.post(
        "/signin",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def signout(client):
    return client.get("/signout", follow_redirects=True)


# Update these:


def test_homepage(client):
    """Assert string time is converted to epoch time."""
    res = app.client.get("/")
    assert res.status_code == 200
    # assert expected_json == result_json


def test_signup(client):
    """Test that a new user is created."""
    form_data = {"username": "mynewuser", "password": "password"}
    res = app.client.post("/signup", data=form_data)
    assert User.query.filter_by(username="mynewuser") != None
    assert res.status_code == 200


def test_add_resource(client):
    """Test that a new resource is created."""
    # Sign in
    signin(client, "Sid", "test")
    form_data = {
        "category": "Machine Learning",
        "title": "testresource",
        "description": "checkitout",
        "link": "https://medium.com",
    }
    res = app.client.post("/new_resource", data=form_data)
    assert Resource.query.filter_by(title="testresource") != None
    assert res.status_code == 200
