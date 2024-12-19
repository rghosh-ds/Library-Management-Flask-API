from flask import Flask
from library_management_app.routes import main
from library_management_app.extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['JWT_SECRET_KEY'] = 'Better'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
