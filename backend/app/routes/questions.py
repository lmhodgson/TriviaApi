from os import abort

from flask import Blueprint, jsonify

from backend.app.models import Question

question_bp = Blueprint('questions', __name__, url_prefix='/questions')


# @question_bp.route("/")
# def retrieve_questions():
#     """Retrieves a list of all questions.
#
#     Returns:
#         JsonObject: A json object containing whether the request was
#         successful and the list of questions.
#     """
#
#     questions = Question.query.order_by(Question.id).all()
#
#     if len(questions) == 0:
#         abort(404)
#
#     return jsonify(
#         {
#             "success": True,
#             "categories": questions
#         }
#     )