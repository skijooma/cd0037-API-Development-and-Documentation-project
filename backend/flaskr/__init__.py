import json
import random
import sys

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from ..models import db, Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    with app.app_context():
        setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # cors = CORS(app, resources={r"*": {"origin": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # @app.after_request()
    # def handle_cors(response):
    #     req = request.referrer
    #
    #     return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=['GET'])
    def categories():

        all_categories = db.session.query(Category).all()

        if len(all_categories) == 0:
            abort(404)

        formatted_categories = [category.format() for category in all_categories]
        formatted_categories = dict((cat['id'], cat['type']) for cat in
                                    formatted_categories)  # Turn this list into a dictionary.

        print("All categories", formatted_categories)

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=['GET'])
    def questions(page: int = 1):

        page = int(request.args.get('page'))
        items_per_page = 10

        if request.method == "GET":
            questions_total = db.session.query(Question).count()
            print("Questions total => ", questions_total)

            category_results = db.session.query(Category).all()
            serialized_category_results = [category.format() for category in category_results]
            serialized_category_results = dict((cat['id'], cat['type']) for cat in
                                               serialized_category_results)  # Turn this list into a dictionary.
            print("All categories => ", serialized_category_results)

            paginated_questions = db.session.query(Question).filter().paginate(page=page,
                                                                               per_page=items_per_page)
            serialized_paginated_questions = [question.format() for question in
                                              paginated_questions.items]
            print("Serialized questions => ", serialized_paginated_questions)
            formatted_paginated_questions = {"questions": serialized_paginated_questions,
                                             "totalQuestions": questions_total,
                                             "categories": serialized_category_results,
                                             "currentCategory": "History"}

            # TODO: Find out what currentCategory really means.

            print("Formatted paginated questions => ", formatted_paginated_questions)

        return jsonify(formatted_paginated_questions)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<id>", methods=['DELETE'])
    def delete_question(id):

        id = request.values.get('id')
        print("Question ID: ", request.values.get('id'))

        error = False

        try:
            if request.method == "DELETE":
                question = db.session.query(Question).filter(Question.id == id).first()
                print("Question found: ", question)

                if question is not None:
                    question.delete()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(400)
        else:
            return ""

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=['POST'])
    def create_questions():

        error = False

        question_text = request.get_json()['question']
        answer = request.get_json()['answer']
        difficulty = request.get_json()['difficulty']
        category = request.get_json()['category']

        question_text = question_text
        answer = answer
        difficulty = difficulty
        category = category

        try:
            question = Question(question=question_text, answer=answer, difficulty=difficulty,
                                category=category)

            print("Question for insertion => ", question)

            question.insert()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(400)
        else:
            return ""

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=['POST'])
    def search_questions():

        search_value = ""

        if "searchTerm" in request.get_json():
            search_value = request.get_json()['searchTerm']

        question_results = db.session.query(Question.id, Question.question, Question.answer,
                                            Question.difficulty, Question.category).filter(
            Question.question.ilike("%" + search_value + "%")).all()
        number_of_questions = db.session.query(Question).filter(
            Question.question.ilike("%" + search_value + "%")).count()

        question_results = [dict(question) for question in question_results]
        results = {"questions": question_results, "totalQuestions": number_of_questions,
                   "currentCategory": "Entertainment"}
        print("Search results => ", results)

        return jsonify(results)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:id>/questions", methods=['GET'])
    def questions_by_category(id):

        error = False
        try:
            id = int(request.args.get('id'))

            if request.method == "GET":
                questions = db.session.query(Question).filter(Question.category == id).all()
                questions_total = db.session.query(Question).filter(Question.id == id).count()
                category = db.session.query(Category).filter(Category.id == id).first()

                print("Questions BY CAT=> ", questions)
                print("Questions total => ", questions_total)
                print("Category => ", category.type)

                serialized_questions = [question.format() for question in questions]
                print("Serialized questions => ", serialized_questions)

                formatted_questions = {"questions": serialized_questions,
                                       "totalQuestions": questions_total,
                                       "currentCategory": category.type}

                print("Formatted questions => ", formatted_questions)
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        if error:
            abort(500)
        else:
            return ""

        return jsonify(formatted_questions)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=['POST'])
    def get_quiz_question():

        error = False

        previous_questions = request.get_json()['previous_questions']
        quiz_category = request.get_json()['quiz_category']
        quiz_category = quiz_category['id']
        print("Quiz req **********************", quiz_category)
        random_question = {}

        try:
            category_questions = []
            if int(quiz_category) == 0:
                category_questions = db.session.query(Question).all()
                print("Quiz request [0] **********************", category_questions)
            else:
                category_questions = db.session.query(Question).filter(
                    Question.category == quiz_category).all()
                print("Quiz request **********************", category_questions)

            print("<<<<<<<< PRE. ", previous_questions, " = ", len(category_questions))
            if len(previous_questions) > 0:  # Filtering out previous questions.
                if len(category_questions) > 0:
                    category_questions = [q for q in category_questions if q.id not in previous_questions]
                    print("<<<<<<<< FILTERED. ", previous_questions, " = ", len(category_questions))

            if len(category_questions) > 0:
                random_position = random.randint(0, len(category_questions) - 1)
                print("******* RANDOM POS => ", random_position, " [", len(category_questions),
                      " [", category_questions[random_position])
                random_question = category_questions[random_position]
                random_question = random_question.format()
                print("******* RANDOM QUESTION => ", random_question)

            return random_question
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(400)
        else:
            return ""

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500




    return app
