import unittest
from app import (qet_questions, get_question)


class TestEndPoints(unittest.TestCase):
    def test_getQuestions_endPoint(self):
        