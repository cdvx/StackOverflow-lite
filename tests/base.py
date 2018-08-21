import unittest

from flask import current_app
from flask_testing import TestCase

from app import app
from app.routes import routes
from config import Config


class APITestCase(TestCase):
    def create_app(self):
        app.config['DEBUG'] = True
        return app

    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        pass

    def post_question(self):
        pass
