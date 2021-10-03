from os import abort
from random import randrange, random

from flask import Blueprint, jsonify, request

from .models import db, Category, Question

category_bp = Blueprint('categories', __name__, url_prefix='/categories')
question_bp = Blueprint('questions', __name__, url_prefix='/questions')
quizzes_bp = Blueprint('quizzes', __name__, url_prefix='/quizzes')

QUESTIONS_PER_PAGE = 10


def paginate_questions(questions_request, selection):
    page = questions_request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


@category_bp.route('/')
def retrieve_categories():
    """Retrieves a list of all categories.

    Returns:
        JsonObject: A json object containing whether the request was 
        successful and the list of categories.
    """

    try:
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        # Create a dictionary from categories result
        categories_dict = dict((cat.id, cat.type) for cat in categories)

        return jsonify({
                'success': True,
                'categories': categories_dict
            })
    except:
        abort(500)


@question_bp.route('/')
def retrieve_questions():
    """Retrieves a list of all questions.

    Returns:
        JsonObject: A json object containing whether the request was
        successful, the total number of questions, list of categories and
        the list of questions.
    """

    try:
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
    except:
        abort(500)


@question_bp.route('/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    """ Deletes a question within the database.

    Args:
        question_id: The id of the question that the user wants to delete.

    Returns:
        JsonObject: A json object containing whether the request was
        successful.
    """

    try:
        question = Question.query.get_or_404(question_id)

        db.session.delete(question)
        db.session.commit()

        return jsonify({
            'success': True,
        })
    except:
        db.session.rollback()

        abort(500)


@category_bp.route("/<category_id>/questions")
def retrieve_questions_for_category(category_id):
    """Retrieves a list of all questions for a specific category.

    Args:
        category_id: The id of the category.

    Returns:
        JsonObject: A json object containing whether the request was
        successful, the total number of questions and
        the list of questions.
    """

    try:
        category = Category.query.get_or_404(category_id)

        questions = Question.query.filter_by(category=category.id)\
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
    except:
        abort(500)


@question_bp.route('/', methods=['POST'])
def post_or_search_questions():
    """Handles POST requests for creating new questions
        and searching questions.
    """

    body = request.get_json()

    search_term = body.get('searchTerm')

    if search_term:
        return search_questions(search_term)
    else:
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        return post_question(question, answer, difficulty, category)


def search_questions(search_term):
    """ Searches questions in the database for the user's query.

    Returns:
        JsonObject: A json object containing whether the request was
        successful, the total questions and the questions that match the
        user's search query.
    """

    try:
        # ilike makes the search case-insensitive
        results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%'))\
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
    except:
        abort(500)


def post_question(question, answer, difficulty, category):
    """ Creates a question within the database if the form submission is valid.

        Returns:
            JsonObject: A json object containing whether the request was
            successful, the total questions and the current page of questions.
        """

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
        abort(500)


@quizzes_bp.route('/', methods=['POST'])
def get_random_quiz_question():
    """ Gets random questions within the given category if provided,
        and that is not one of the previous questions.

        Returns:
            JsonObject: A json object containing whether the request was
            successful, the total questions and the current page of questions.
        """

    body = request.get_json()
    try:
        previous_questions = body.get('previous_questions')
        category_id = body.get('quiz_category')['id']

        if category_id == 0:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions))\
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
        current_question = questions[random_question_id]

        return jsonify({
            'success': True,
            'question': current_question,
            'total_questions': question_count
        })
    except:
        abort(500)
