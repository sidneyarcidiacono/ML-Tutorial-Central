import os
import unittest

from tutorial_app import app, db, bcrypt
from tutorial_app.models import User, Tutorial, Resource

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
        self.assertIn("testuser", response_text)
        self.assertIn("New Tutorial", response_text)
        self.assertIn("New Resource", response_text)
        self.assertIn("Sign Out", response_text)
        self.assertIn("Edit Tutorial", response_text)
        self.assertIn("Delete Tutorial", response_text)

        self.assertNotIn("Sign In", response_text)
        self.assertNotIn("Sign Up", response_text)

    # Test updating a tutorial
    def test_update_tutorial(self):
        """Test updating a tutorial."""
        # Set up
        create_tutorial()
        create_user()
        signin(self.app, "testuser", "password")

        # Make POST request with data
        post_data = {
            "title": "Machine Learning Basics",
            "difficulty": "Beginner",
            "category": "Machine Learning",
            "body": "Updated body",
        }
        self.app.post("/tutorials/edit/1", data=post_data)

        # Make sure the book was updated as we'd expect
        tutorial = Tutorial.query.get(1)
        self.assertEqual(tutorial.title, "Machine Learning Basics")
        self.assertEqual(tutorial.body, "Updated body")
        self.assertEqual(tutorial.category, "Machine Learning")
        self.assertEqual(tutorial.difficulty, "Beginner")

    # Test creating a tutorial
    def test_new_tutorial(self):
        """Test creating a tutorial."""
        # Set up
        create_tutorial()
        create_user()
        signin(self.app, "testuser", "password")

        # Make POST request with data
        post_data = {
            "title": "Linear Regression",
            "category": "Machine Learning",
            "difficulty": "Intermediate",
            "body": "Testing creating a tutorial",
        }
        self.app.post("/new_tutorial", data=post_data)

        # Make sure book was updated as we'd expect
        created_tutorial = Tutorial.query.filter_by(
            title="Linear Regression"
        ).one()
        self.assertIsNotNone(created_tutorial)
        self.assertEqual(created_tutorial.body, "Testing creating a tutorial")

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
        self.assertIn("/signin?next=%2Fcreate_book", response.location)

    # Test creating a resource
    def test_new_resource(self):
        """Test creating a resource."""
        create_resource()
        create_user()
        signin(self.app, "testuser", "password")

        post_data = {
            "category": "Statistics",
            "title": "Test resource",
            "description": "A resource",
            "link": "https://stackoverflow.com",
        }
        self.app.post("/new_resource", data=post_data)

        new_resource = Resource.query.filter_by(title="Test resource").one()
        self.assertIsNotNone(new_resource)
        self.assertEqual(new_resource.link, "https://stackoverflow.com")
        self.assertEqual(new_resource.description, "A resource")
        self.assertEqual(new_resource.category, "Statistics")

    # Test deleting a resource
    def test_delete_resource(self):
        """Test deleting a resource."""
        create_resource()
        create_user()
        signin(self.app, "testuser", "password")

        self.app.post("/resources/delete/1")

        resource = Resource.query.get(1)
        self.assertIsNone(resource)
