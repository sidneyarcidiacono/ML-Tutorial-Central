"""Tests for auth routes."""
# Thank you to Meredith Murphy for the test setup code
import os
from unittest import TestCase

from datetime import date

from tutorial_app import app, db, bcrypt
from tutorial_app.models import User, Tutorial, Resource

"""
Run these tests with the command:
python3 -m unittest tutorial_app.auth.tests
"""

#################################################
# Setup
#################################################


def create_tutorial():
    t1 = Tutorial(
        category="Machine Learning",
        title="Test Tutorial",
        difficulty="Beginner",
        body="Test body",
    )
    db.session.add(t1)
    db.session.commit()


def create_resource():
    r1 = Resource(
        category="Machine Learning",
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


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        """Test signup."""
        post_data = {
            "username": "Sid",
            "password": "password",
        }
        self.app.post("/signup", data=post_data)

        created_user = User.query.filter_by(username="Sid").one()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "Sid")

    def test_signup_existing_user(self):
        """Test that signing up an existing user won't work."""
        create_user()

        post_data = {
            "username": "testuser",
            "password": "password",
        }
        response = self.app.post("/signup", data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Sign Up", response_text)
        self.assertIn(
            "That username is taken. Please choose a different one.",
            response_text,
        )

    def test_signin_correct_password(self):
        """Test logging in with the correct password."""
        post_data = {
            "username": "testuser",
            "password": "password",
        }
        self.app.post("/signup", data=post_data)

        response = self.app.post("/signin", data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Redirecting...", response_text)
        self.assertNotIn("Sign In", response_text)

    def test_signin_nonexistent_user(self):
        """Test that signing in a nonexistent user fails."""
        post_data = {
            "username": "user1",
            "password": "password",
        }
        response = self.app.post("/signin", data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Sign In", response_text)
        self.assertIn(
            "No user with that username. Please try again.", response_text
        )
        self.assertNotIn("Sign Out", response_text)

    def test_signin_incorrect_password(self):
        """Ensure that a user cannot sign in with the incorrect password."""
        create_user()

        post_data = {
            "username": "testuser",
            "password": "passwords",
        }
        response = self.app.post("/signin", data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Sign In", response_text)
        self.assertIn(
            "Password doesn&#39;t match. Please try again", response_text
        )
        self.assertNotIn("Sign Out", response_text)

    def test_signout(self):
        """Test logout."""
        create_user()

        post_data = {
            "username": "testuser",
            "password": "password",
        }
        self.app.post("/signin", data=post_data)

        response = self.app.get("/signout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Sign In", response_text)
        self.assertNotIn("Sign Out", response_text)