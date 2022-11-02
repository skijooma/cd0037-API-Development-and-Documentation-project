import os

import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432',
                                                         self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = Question(question="What was Twitter’s original name", answer="twttr",
                                     difficulty=2, category=1)

        self.searchTerm = {"searchTerm": "Clay"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for successful operation and for expected errors.
    """

    # def test_get_categories(self):
    #     # Test that a call to /categories resolves to success
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)
    #
    #     print("CATEGORIES =>>>> ", len(data['categories']))
    #     self.assertEqual(res.status_code, 200)  # Status code is 200.
    #     self.assertEqual(data['success'], True)  # Response success.
    #     self.assertEqual(len(data['categories']), 6)  # Must be 6 categories returned.
    #
    # """ FAILURE Test that a call to /cats resolves to a not found response status """
    # def test_404_returned_for_invalid_categories_url(self):
    #
    #     res = self.client().get('/cats')
    #     self.assertEqual(res.status_code, 404)


    # def test_get_questions(self):  #  #     # Test that a call to /questions resolves to success  #     res = self.client().get('/questions?page=2')  #     data = json.loads(res.data)  #  #     print("QUESTIONS = >>>> ", len(data))  #     self.assertEqual(res.status_code, 200) # Response success.  #     self.assertTrue(len(data)) # Must be 6 categories returned.  #  #     # FAILURE - Test that a call to /question resolves to a not found response status  #     res = self.client().get('/question')  #     self.assertEqual(res.status_code, 404)

    # def test_delete_question(self):  #     # Test that a call to DELETE /questions/<id> resolves to success  #     res = self.client().delete('/questions/5')  #     print("DELETE => ", res)  #     # data = json.loads(res.data)  #  #     with self.app.app_context():  #         question = Question.query.filter(Question.id == 5).one_or_none()  #  #     print("QUESTION 5 = >>>> ", question)  #     self.assertEqual(res.status_code, 200)  # Response success.  #     self.assertEqual(question, None)  # Deleted question should not be found if queried.

    # SUCCESS  # def test_create_question(self):  #     # Test that a call to POST /questions resolves to success  #     res = self.client().post('/questions', json=self.new_question.format())  #     print("POST questions => ", res.get_json())  #     # data = json.loads(res.data)  #  #     # print("data => ", data)  #  #     self.assertEqual(res.status_code, 200)  # Response success.  #     # self.assertEqual(data['success'], True)  #     # self.assertTrue(data['created'])

    # FAILURE  # def test_405_invalid_question_creation(self):  #  #     # Test that a call to POST /questions resolves to success  #     res = self.client().post('/questions/100', json=self.new_question.format())  #     print("POST questions => ", res.get_json())  #     # data = json.loads(res.data)  #  #     # print("data => ", data)  #  #     self.assertEqual(res.status_code, 405)  # Response success.  #     # self.assertEqual(data['success'], False)  #     # self.assertTrue(data['message'], "method not allowed")

    # SUCCESS - POST /questions/search  # def test_search_questions(self):  #  #     # Test that a call to POST /questions/search resolves to success  #     res = self.client().post('/questions/search', json=self.searchTerm)  #     print("POST questions => ", res.get_json())  #     data = json.loads(res.data)  #  #     questions_list = data['questions']  #     question_text = data['questions'][0]['question']  #  #     self.assertEqual(res.status_code, 200)  # Response success.  #     self.assertEqual(len(data['questions']), 1)  #     self.assertTrue(self.searchTerm['searchTerm'] in question_text)

    # FAILURE  # def test_405_invalid_question_creation(self):  #  #     # Test that a call to POST /questions/search with no search term resolves to a bad request & fails.  #     res = self.client().post('/questions/search')  #  #     self.assertEqual(res.status_code, 400)  # Response success.

    # SUCCESS - GET /categories/<int: id>/questions  # def test_get_questions_by_category(self):  #  #     # Test that a call to GET /categories/5/questions resolves to success  #     res = self.client().get('/categories/5/questions?id=5')  #     data = json.loads(res.data)  #  #     self.assertEqual(res.status_code, 200)  # Response success.  #     self.assertEqual(len(data['questions']), 3) # 3 questions in category Entertainment.

    # FAILURE  # def test_405_questions_request_with_invalid_category(self):  #  #     # Test that a call to GET /categories/50/questions fails with a server error.  #     res = self.client().get('/categories/50/questions?id=50')  #  #     self.assertEqual(res.status_code, 500)  # Response success.

    # # SUCCESS - GET /quizzes  # def test_get_quiz_question(self):  #  #     # Test that a call to POST /quizzes resolves to success  #     res = self.client().post('/quizzes')  #     # data = json.loads(res.data)  #  #     self.assertEqual(res.status_code, 200)  # Response success.  #     # self.assertEqual(len(data['questions']), 3) # 3 questions in category Entertainment.

    # FAILURE  # def test_405_questions_request_with_invalid_category(self):  #  #     # Test that a call to GET /categories/50/questions fails with a server error.  #     res = self.client().get('/categories/50/questions?id=50')  #  #     self.assertEqual(res.status_code, 500)  # Response success.


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
