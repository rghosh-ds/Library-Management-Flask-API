from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from library_management_app.extensions import db
from library_management_app.models import Book, Member
from typing import Tuple

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/healthcheck', methods=['GET'])
def healthcheck() -> Response:
    return jsonify({"message": "Server is running"})


@main.route('/register', methods=['POST'])
def register() -> Tuple[Response, int]:
    data = request.json
    username: str = data.get('username')
    password: str = data.get('password')

    if Member.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_member = Member(username=username, password=hashed_password)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully"}), 201


@main.route('/login', methods=['POST'])
def login() -> Tuple[Response, int]:
    data = request.json
    username: str = data.get('username')
    password: str = data.get('password')

    member = Member.query.filter_by(username=username).first()
    if not member or not check_password_hash(member.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


@main.route('/books', methods=['GET'])
@jwt_required()
def get_books() -> Response:
    page: int = request.args.get('page', 1, type=int)
    per_page: int = request.args.get('per_page', 10, type=int)
    search_query: str = request.args.get('search', '', type=str)

    query = Book.query
    if search_query:
        query = query.filter((Book.title.ilike(f'%{search_query}%')) | (Book.author.ilike(f'%{search_query}%')))

    pagination = query.paginate(page=page, per_page=per_page)
    books = pagination.items

    return jsonify({
        "books": [{"id": book.id, "title": book.title, "author": book.author} for book in books],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    })


@main.route('/books', methods=['POST'])
@jwt_required()
def add_book() -> Tuple[Response, int]:
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author}), 201
