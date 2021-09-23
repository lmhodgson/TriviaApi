from os import abort

from flask import Blueprint, jsonify, request

from .models import db, Category, Question

category_bp = Blueprint('categories', __name__, url_prefix='/categories')
question_bp = Blueprint('questions', __name__, url_prefix='/questions')

QUESTIONS_PER_PAGE = 10


def paginate_questions(questions_request, selection):
    page = questions_request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


@category_bp.route("/")
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

        return jsonify(
            {
                "success": True,
                "categories": categories
            }
        )
    except:
        abort(500)


@question_bp.route("/")
def retrieve_questions():
    """Retrieves a list of all questions.

    Returns:
        JsonObject: A json object containing whether the request was
        successful, the total number of questions, list of categories and
        the list of questions.
    """

    try:
        all_questions = Question.query.all()
        total_questions = len(all_questions)
        current_questions = paginate_questions(request, all_questions)

        # Abort if no questions are found
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()

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

        questions = Question.query.filter_by(category=category.id).all()
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

