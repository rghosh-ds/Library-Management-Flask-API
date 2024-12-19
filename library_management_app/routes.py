from flask import Blueprint, jsonify, request
from library_management_app.extensions import db
from library_management_app.models import Book


main = Blueprint('main', __name__)


@main.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author} for book in books])


@main.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author}), 201
