from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import random

from .models import db, setup_db, Category, Question

QUESTIONS_PER_PAGE = 10


def paginate_questions(questions_request, selection):
    page = questions_request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app():
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories')
    def retrieve_categories():
        """Retrieves a list of all categories.

        Returns:
            JsonObject: A json object containing whether the request was
            successful and the list of categories.
        """

        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        # Create a dictionary from categories result
        categories_dict = dict((cat.id, cat.type) for cat in categories)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions')
    def retrieve_questions():
        """Retrieves a list of all questions.

        Returns:
            JsonObject: A json object containing whether the request was
            successful, the total number of questions, list of categories and
            the list of questions.
        """

        all_questions = Question.query.order_by(Question.id).all()
        total_questions = len(all_questions)
        current_questions = paginate_questions(request, all_questions)

        # Abort if no questions are found
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()

        # Create a dictionary from categories result
        categories_dict = dict((cat.id, cat.type) for cat in categories)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """ Deletes a question within the database.

        Args:
            question_id: The id of the question that the user wants to delete.

        Returns:
            JsonObject: A json object containing whether the request was
            successful.
        """

        question = Question.query.get_or_404(question_id)

        try:
            db.session.delete(question)
            db.session.commit()

            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_for_category(category_id):
        """Retrieves a list of all questions for a specific category.

        Args:
            category_id: The id of the category.

        Returns:
            JsonObject: A json object containing whether the request was
            successful, the total number of questions and
            the list of questions.
        """

        category = Category.query.get_or_404(category_id)

        questions = Question.query.filter_by(category=category.id) \
            .order_by(Question.id).all()
        total_questions = len(questions)
        current_questions = paginate_questions(request, questions)

        # Abort if no questions are found
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """ Searches questions in the database for the user's query.

        Returns:
            JsonObject: A json object containing whether the request was
            successful, the total questions and the questions that match the
            user's search query.
        """

        body = request.get_json()

        search_term = body.get('searchTerm')

        # ilike makes the search case-insensitive
        results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')) \
            .order_by(Question.id).all()

        # Abort if no questions are found
        if len(results) == 0:
            abort(404)

        all_questions = Question.query.order_by(Question.id).all()
        total_questions = len(all_questions)
        current_questions = paginate_questions(request, results)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions
        })

    @app.route('/questions', methods=['POST'])
    def post_question():
        """ Creates a question within the database if the form submission is valid.

            Returns:
                JsonObject: A json object containing whether the request was
                successful, the total questions and the current page of questions.
            """

        body = request.get_json()

        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        # Validate all request arguments have data
        if ((question is None) or (answer is None)
                or (difficulty is None) or (category is None)):
            abort(422)

        try:
            new_question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)

            db.session.add(new_question)
            db.session.commit()

            all_questions = Question.query.order_by(Question.id).all()
            total_questions = len(all_questions)
            current_questions = paginate_questions(request, all_questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions
            })

        except:
            db.session.rollback()

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        """ Gets random questions within the given category if provided,
            and that is not one of the previous questions.

            Returns:
                JsonObject: A json object containing whether the request was
                successful, the total questions and the current page of questions.
            """

        body = request.get_json()

        previous_questions = body.get('previous_questions')
        category_id = body.get('quiz_category')['id']

        if category_id == 0:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions)) \
                .order_by(Question.id).all()
        else:
            category = Category.query.get_or_404(category_id)

            questions = Question.query.filter_by(category=category.id) \
                .filter(Question.id.notin_(previous_questions)) \
                .order_by(Question.id).all()

        question_count = len(questions)
        if question_count == 0:
            abort(404)

        random_question_id = random.randrange(0, question_count)
        current_question = questions[random_question_id].format()

        return jsonify({
            'success': True,
            'question': current_question,
            'total_questions': question_count
        })

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error",
            "stacktrace": str(error)
        }), 500

    return app
