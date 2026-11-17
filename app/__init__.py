from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    # Temporary placeholder until we create the User model.
    return None


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-key-change-later"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prompt_lab.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
