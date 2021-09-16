from os import abort

from flask import Blueprint, jsonify

from backend.app.models import Category

category_bp = Blueprint('categories', __name__, url_prefix='/categories')


@category_bp.route("/")
def retrieve_categories():
    """ Retrieves a list of all categories.

        Returns: A json object containing whether the request was successful
            and the list of categories.
        """

    categories = Category.query.order_by(Category.id).all()

    if len(categories) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "categories": categories
        }
    )