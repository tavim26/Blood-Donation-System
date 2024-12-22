from flask import Flask

from config import Config
from extensions import db, migrate,bcrypt
from routes import register_controllers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    register_controllers(app)

    return app
