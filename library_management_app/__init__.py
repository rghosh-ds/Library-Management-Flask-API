from flask import Flask
from library_management_app.routes import main
from library_management_app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register blueprint
    app.register_blueprint(main)

    # Initialize extensions
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
