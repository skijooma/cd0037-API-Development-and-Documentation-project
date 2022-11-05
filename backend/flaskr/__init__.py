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
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"*": {"origin": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def handle_cors(response):
        req = request.referrer

        return response

    """
    An endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=['GET'])
    def categories():

        all_categories = db.session.query(Category).all()  # In the database.

        if len(all_categories) == 0:
            abort(404)

        formatted_categories = [category.format() for category in
                                all_categories]
        formatted_categories = dict((cat['id'], cat['type']) for cat in
                                    formatted_categories)  # Turn this list into a dictionary.

        return jsonify({'success': True, 'categories': formatted_categories})

    """
    An endpoint that returns a list of paginated (10) questions,
    including the: number of total questions, current category, and categories.
    """

    @app.route("/questions", methods=['GET'])
    def questions(page: int = 1):

        if request.args.get('page') is None:
            abort(500)

        page = int(request.args.get('page'))
        items_per_page = QUESTIONS_PER_PAGE  # 10

        questions_total = db.session.query(Question).count()
        category_results = db.session.query(Category).all()
        serialized_category_results = [category.format() for category in
                                       category_results]
        serialized_category_results = dict((cat['id'], cat['type']) for cat in
                                           serialized_category_results)  # Turn this list into a
        # dictionary.
        paginated_questions = db.session.query(Question).filter().paginate(
            page=page, per_page=items_per_page)
        serialized_paginated_questions = [question.format() for question in
                                          paginated_questions.items]

        return jsonify({
            'success': True, 'questions': serialized_paginated_questions,
            'totalQuestions': questions_total,
            'categories': serialized_category_results,
            'currentCategory': 'History'
        })

    """
    An endpoint to DELETE question using a question ID.
    """

    @app.route("/questions/<int:id>", methods=['DELETE'])
    def delete_question(id):

        try:
            question = db.session.query(Question).filter(
                Question.id == id).first()
            if question is None:
                abort(404)
            question.delete()

            return jsonify({'success': True, 'deleted': id})
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

    """
    An endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route("/questions", methods=['POST'])
    def create_questions():

        question_text = request.get_json()['question']
        answer = request.get_json()['answer']
        difficulty = request.get_json()['difficulty']
        category = request.get_json()['category']

        question_text = question_text
        answer = answer
        difficulty = difficulty
        category = category

        try:
            question = Question(question=question_text, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()
            question_count = db.session.query(Question).count()
            all_questions = db.session.query(Question).all()
            all_questions = [question.format() for question in
                             all_questions]  # formatted questions.

            return jsonify({'success': True, 'created': question.id})
        except:
            abort(422)
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    """
    A POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """

    @app.route("/questions/search", methods=['POST'])
    def search_questions():

        try:
            search_value = ""

            if "searchTerm" in request.get_json():
                search_value = request.get_json()['searchTerm']

            number_of_questions = db.session.query(Question).filter(
                Question.question.ilike("%" + search_value + "%")).count()
            question_results = db.session.query(Question.id, Question.question,
                                                Question.answer,
                                                Question.difficulty,
                                                Question.category).filter(
                Question.question.ilike("%" + search_value + "%")).all()
            question_results = [dict(question) for question in
                                question_results]

            return jsonify({
                'success': True, 'questions': question_results,
                'totalQuestions': number_of_questions,
                'currentCategory': "History"
            })
        except:
            abort(500)
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    """
    A GET endpoint to get questions based on category.
    """

    @app.route("/categories/<int:id>/questions", methods=['GET'])
    def questions_by_category(id):

        id = int(request.args.get('id'))

        try:
            category = db.session.query(Category).filter(
                Category.id == id).first()

            if category is None:
                abort(500)

            questions = db.session.query(Question).filter(
                Question.category == id).all()
            questions_total = db.session.query(Question).filter(
                Question.id == id).count()
            serialized_questions = [question.format() for question in
                                    questions]

            return jsonify({
                'success': True, "questions": serialized_questions,
                "totalQuestions": questions_total,
                "currentCategory": category.type
            })
        except:
            abort(500)
            db.session.rollback()
            print(sys.exc_info())

    """
    A POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """

    @app.route("/quizzes", methods=['POST'])
    def get_quiz_question():

        previous_questions = request.get_json()['previous_questions']
        quiz_category = request.get_json()['quiz_category']
        quiz_category = quiz_category['id']

        random_question = {}

        try:
            category_questions = []
            if int(quiz_category) == 0:
                category_questions = db.session.query(Question).all()
            else:
                category_questions = db.session.query(Question).filter(
                    Question.category == quiz_category).all()

            if len(previous_questions) > 0:  # Filtering out previous questions.
                if len(category_questions) > 0:
                    category_questions = [q for q in category_questions if
                                          q.id not in previous_questions]

            if len(category_questions) == 0:
                abort(500)

            random_position = random.randint(0, len(category_questions) - 1)
            random_question = category_questions[random_position]
            random_question = random_question.format()

            return jsonify({'success': True, "question": random_question})
        except:
            abort(500)
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    """
    Error handlers for all expected errors
    These include 400, 404, 405, 422 and 500.
    """

    @app.errorhandler(400)
    def not_found(error):
        return jsonify(
            {"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, "error": 404, "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False, "error": 405, "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False, "error": 422, "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False, "error": 500, "message": "Internal server error"
        }), 500

    return app
