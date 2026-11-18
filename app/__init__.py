
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-key-change-later"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prompt_lab.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Apply test settings BEFORE initializing SQLAlchemy.
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.auth import auth
    app.register_blueprint(auth)

    from app.experiments import experiments
    app.register_blueprint(experiments)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
