from flask import Blueprint, jsonify, request
from library_management_app.extensions import db
from library_management_app.models import Book

main = Blueprint('main', __name__)


@main.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Book.query.paginate(page=page, per_page=per_page)
    books = pagination.items

    return jsonify({
        "books": [{"id": book.id, "title": book.title, "author": book.author} for book in books],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    })


@main.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author}), 201
