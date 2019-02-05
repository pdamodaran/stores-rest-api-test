"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # runs once
    @classmethod
    def setUpClass(cls):
        # Make sure database exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():
            db.init_app(app)

    # runs before a single test
    def setUp(self):
        with app.app_context():
            db.create_all()
        # Get a test client
        # https://stackoverflow.com/questions/32129064/what-are-the-parentheses-for-at-the-end-of-python-method-names
        # In Python, functions and methods are first-order objects.
        # You can store the method for later use without calling it, for example:
        # upper() is a command asking the upper method to run, while upper is a reference to the method itself.
        # For example,
        # upper2 = 'Michael'.upper
        # upper2() # does the same thing as 'Michael'.upper() !
        self.app = app.test_client
        self.app_context = app.app_context

    # runs after a single test
    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
