import os
import unittest

from tutorial_app import app, db, bcrypt
from tutorial_app.models import (
    User,
    Tutorial,
    Resource,
    TutorialCategory,
    Difficulty,
)

"""
Run these tests with the command:
python3 -m unittest tutorial_app.main.tests
"""

#################################################
# Setup
#################################################


def signin(client, username, password):
    return client.post(
        "/signin",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def signout(client):
    return client.get("/signout", follow_redirects=True)


def create_tutorial():
    t1 = Tutorial(
        category=TutorialCategory.ML,
        title="Test Tutorial",
        difficulty=Difficulty.BEGINNER,
        body="Test body",
    )
    db.session.add(t1)
    db.session.commit()


def create_resource():
    r1 = Resource(
        category=TutorialCategory.OTHER,
        title="Test Resource",
        description="Test resource",
        link="https://medium.com",
    )
    db.session.add(r1)
    db.session.commit()


def create_user():
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="testuser", password=password_hash)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################


class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # Test that when logged out, nav options are correct and we see
    # our "Test Tutorial" on the main page
    def test_homepage_signed_out(self):
        """
        Test that the tutorials show up on the homepage.

        Test that the navigation options are correct for
        unauthorized user.
        """
        # Set up
        create_tutorial()

        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Test Tutorial", response_text)
        self.assertIn("Sign In", response_text)
        self.assertIn("Sign Up", response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to authenticated users)
        self.assertNotIn("New Tutorial", response_text)
        self.assertNotIn("New Resource", response_text)
        self.assertNotIn("Sign Out", response_text)

    # Test that when signed in, nav options are correct
    # and we see our "Test Tutorial"
    def test_homepage_signed_in(self):
        """
        Test that the tutorials show up on the homepage.

        Test that navigation options are correct
        for authorized user.
        """
        # Set up
        create_tutorial()
        create_user()
        signin(self.app, "testuser", "password")

        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Test Tutorial", response_text)
        self.assertIn("New Tutorial", response_text)
        self.assertIn("New Resource", response_text)
        self.assertIn("Sign Out", response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to signed out users)
        self.assertNotIn("Sign In", response_text)
        self.assertNotIn("Sign Up", response_text)

    # Test that the tutorial details show
    # And that the nav options are correct for our signed out user
    def test_tutorial_detail_signed_out(self):
        """Test that the tutorial appears on its detail page."""
        create_tutorial()
        create_user()

        response = self.app.get("/tutorials/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Test Tutorial", response_text)
        self.assertIn("Test body", response_text)
        self.assertIn("Beginner", response_text)
        self.assertIn("Sign Up", response_text)

        self.assertNotIn("Sign Out", response_text)
        self.assertNotIn("New Tutorial", response_text)

    # Test when logged in that the edit and delete options show
    # For our test_tutorial
    def test_tutorial_detail_signed_in(self):
        """Test that the tutorial appears on its detail page correctly."""
        create_tutorial()
        create_user()
        signin(self.app, "testuser", "password")

        response = self.app.get("/tutorials/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Test Tutorial", response_text)
        self.assertIn("Test body", response_text)
        self.assertIn("Beginner", response_text)
        self.assertIn("New Tutorial", response_text)
        self.assertIn("New Resource", response_text)
        self.assertIn("Sign Out", response_text)
        self.assertIn("Edit Tutorial", response_text)
        self.assertIn("Delete Tutorial", response_text)

        self.assertNotIn("Sign In", response_text)
        self.assertNotIn("Sign Up", response_text)

    # Test creating a tutorial when signed out
    def test_new_tutorial_signed_out(self):
        """
        Test that the user is redirected when trying to access
        the route to create a tutorial when not signed in.
        """
        # Set up
        create_tutorial()
        create_user()

        # Make GET request
        response = self.app.get("/new_tutorial")

        # Make sure that the user was redirecte to the signin page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/signin?next=%2Fnew_tutorial", response.location)
