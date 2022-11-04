import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import setup_db, Question


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
                                     difficulty=2, category=1)  # For new question creation

        self.searchTerm = {"searchTerm": "Clay"}  # For POST /questions/search.

        self.previous_questions = []
        self.quiz_category = {'type': 'Entertainment', 'id': '5'}

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

    # def test_get_questions(self):
    #     # Test that a call to GET /questions resolves to success
    #     res = self.client().get('/questions?page=2')
    #     data = json.loads(res.data)
    #
    #     print("QUESTIONS =>>>> ", len(data['questions']))
    #     self.assertEqual(res.status_code, 200)  # Status code is 200.
    #     self.assertEqual(data['success'], True)  # Response success.
    #     self.assertEqual(len(data['questions']), 10)  # Must be 10 paginated questions returned.
    #     self.assertEqual(data['totalQuestions'], 33)  # Must be 33 total questions returned.
    #
    # """FAILURE Test that a call to /questions without a page parameter resolves to a server error
    # """
    # def test_404_returned_for_get_questions_without_page_parameter(self):
    #
    #     res = self.client().get('/questions')
    #     self.assertEqual(res.status_code, 500)

    # def test_delete_question(self):
    #     # Test that a call to DELETE /questions/<id> resolves to success
    #     res = self.client().delete('/questions/37')
    #     print("DELETE => ", res)
    #     data = json.loads(res.data)
    #
    #     with self.app.app_context():
    #         question = Question.query.filter(Question.id == 37).one_or_none()
    #         print("QUESTION 37 = >>>> ", question)
    #
    #     self.assertEqual(res.status_code, 200)  # Response success.  #
    #     self.assertEqual(data['success'], True)  # Response success.
    #     self.assertEqual(data['deleted'], 37)  # Response success.
    #     self.assertEqual(question, None)  # Deleted question should not be found if queried.
    #
    # """FAILURE Test that a call to /questions without a page parameter resolves to a server error
    # """
    # def test_404_returned_for_deleting_non_existing_question(self):
    #
    #     res = self.client().delete('/questions/100')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Unprocessable entity')

    # def test_create_question(self):
    #     # Test that a call to POST /questions resolves to success  #
    #     res = self.client().post('/questions', json=self.new_question.format())
    #     data = json.loads(res.data)
    #     print("data => ", data)
    #
    #     self.assertEqual(res.status_code, 200)  # Response success.
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(len(data['questions']))
    #
    # def test_405_invalid_question_creation(self):
    #     # Test that a call to POST /questions/100 resolves to failure.
    #     res = self.client().post('/questions/100', json=self.new_question.format())
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 405)  # Method not allowed status code.
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], "Method not allowed")

    # # SUCCESS - POST /questions/search
    # def test_search_questions(self):
    #     # Test that a call to POST /questions/search resolves to success
    #     res = self.client().post('/questions/search', json=self.searchTerm)
    #     print("POST questions => ", res.get_json())
    #     data = json.loads(res.data)
    #
    #     questions_list = data['questions']
    #     question_text = data['questions'][0]['question']
    #
    #     self.assertEqual(res.status_code, 200)  # Response success.
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['totalQuestions'], 1)  # Number of questions in results returned.
    #     self.assertTrue(
    #         self.searchTerm['searchTerm'] in question_text)  # Text in question matches search term.
    #
    # def test_500_for_question_search_with_no_term(self):
    #     # Test that a call to POST /questions/search with no search term resolves to failure.
    #     res = self.client().post('/questions/search', json=None)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 500)  # Internal server error status code.
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], "Internal server error")

    # SUCCESS - GET /categories/<int: id>/questions  #
    # def test_get_questions_by_category(self):
    #     # Test that a call to GET /categories/5/questions resolves to success
    #     res = self.client().get('/categories/5/questions?id=5')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)  # Response success.
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['questions']), 3)  # 3 questions in category Entertainment.

    # FAILURE -
    # def test_405_questions_request_with_nonexistent_category(self):
    #     # Test that a call to GET /categories/50/questions fails with a server error.
    #     res = self.client().get('/categories/50/questions?id=50')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 500)  # Internal server error status code.
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], "Internal server error")

    # SUCCESS - GET /quizzes
    # def test_get_quiz_question(self):
    #     # Test that a call to POST /quizzes resolves to success.
    #     res = self.client().post('/quizzes', json={"previous_questions": self.previous_questions,
    #                                                "quiz_category": self.quiz_category})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)  # Response with success status code.
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['question']['category'], 5)

    # FAILURE  #
    # def test_405_questions_request_with_invalid_category(self):
    #     # Test that a call to POST /quizzes with an invalid category
    #     self.quiz_category = {'type': 'Entertainment', 'id': 100} # Category with invalid ID.
    #     res = self.client().post('/quizzes', json={"previous_questions": self.previous_questions,
    #                                                "quiz_category": self.quiz_category})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 500)  # Internal server error status code.
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], "Internal server error")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
